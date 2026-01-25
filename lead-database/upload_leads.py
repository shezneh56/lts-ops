#!/usr/bin/env python3
"""
Lead Database Upload Script
Handles CSV imports to Supabase with smart column mapping and deduplication
"""

import os
import sys
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import defaultdict

try:
    from supabase import create_client, Client
    from tqdm import tqdm
except ImportError:
    print("ERROR: Missing required packages. Run: pip install supabase tqdm")
    sys.exit(1)


class ColumnMapper:
    """Smart column name mapper - handles variations across different CSV sources"""
    
    # Define mapping rules: canonical_field -> list of possible CSV column names
    MAPPING_RULES = {
        'email': ['email', 'Email', 'EMAIL', 'email_address', 'Email Address'],
        'first_name': ['first name', 'First Name', 'firstname', 'FirstName', 'first_name'],
        'last_name': ['last name', 'Last Name', 'lastname', 'LastName', 'last_name'],
        'full_name': ['full name', 'Full Name', 'fullname', 'FullName', 'full_name', 'name', 'Name'],
        'title': ['title', 'Title', 'job_title', 'Job Title', 'JobTitle', 'position', 'Position'],
        'company_name': ['company name', 'Company Name', 'company', 'Company', 'company_name', 'CompanyName'],
        'company_website': ['company website', 'Company Website', 'website', 'Website', 'company_url', 'domain'],
        'mobile_number': ['mobile number', 'Mobile Number', 'phone', 'Phone', 'mobile', 'Mobile', 'phone_number'],
        'personal_email': ['personal email', 'Personal Email', 'personal_email', 'PersonalEmail'],
        'linkedin_url': ['linkedin', 'LinkedIn', 'linkedin_url', 'LinkedIn URL', 'person_linkedin'],
        'industry': ['industry', 'Industry', 'sector', 'Sector'],
        'headline': ['headline', 'Headline', 'bio', 'Bio'],
        'seniority': ['seniority', 'Seniority', 'level', 'Level'],
        'department': ['department', 'Department', 'dept', 'Dept'],
        'city': ['city', 'City'],
        'state': ['state', 'State', 'region', 'Region'],
        'country': ['country', 'Country'],
        'company_linkedin': ['company linkedin', 'Company Linkedin', 'company_linkedin_url'],
        'company_employees_count': ['employees count', 'Employees Count', 'employee_count', 'company_size'],
        'company_annual_revenue': ['company annual revenue clean', 'Company Annual Revenue Clean', 'revenue', 'annual_revenue'],
        'company_total_funding': ['company total funding clean', 'Company Total Funding Clean', 'funding', 'total_funding'],
        'company_founded_year': ['company founded year', 'Company Founded Year', 'founded', 'founded_year'],
        'email_validation_status': ['validation status', 'Validation Status', 'email_status'],
    }
    
    def __init__(self, csv_columns: List[str]):
        """Initialize mapper with CSV column names"""
        self.csv_columns = csv_columns
        self.mapping = self._build_mapping()
        self.unmapped_columns = self._find_unmapped()
    
    def _normalize(self, name: str) -> str:
        """Normalize column name for comparison"""
        return name.lower().strip()
    
    def _build_mapping(self) -> Dict[str, str]:
        """Build mapping from canonical fields to actual CSV columns"""
        mapping = {}
        csv_normalized = {self._normalize(col): col for col in self.csv_columns}
        
        for canonical, variations in self.MAPPING_RULES.items():
            for variation in variations:
                normalized = self._normalize(variation)
                if normalized in csv_normalized:
                    mapping[canonical] = csv_normalized[normalized]
                    break
        
        return mapping
    
    def _find_unmapped(self) -> List[str]:
        """Find CSV columns that don't map to core fields"""
        mapped_csv_cols = set(self.mapping.values())
        return [col for col in self.csv_columns if col not in mapped_csv_cols]
    
    def get(self, canonical_field: str) -> Optional[str]:
        """Get the CSV column name for a canonical field"""
        return self.mapping.get(canonical_field)
    
    def map_row(self, csv_row: Dict[str, str]) -> Dict[str, Any]:
        """Map a CSV row to database schema"""
        result = {
            'core_fields': {},
            'extra_data': {}
        }
        
        # Map core fields
        for canonical, csv_col in self.mapping.items():
            value = csv_row.get(csv_col, '').strip()
            if value:
                # Handle numeric conversions
                if canonical in ['company_employees_count', 'company_annual_revenue', 
                                'company_total_funding', 'company_founded_year']:
                    try:
                        # Remove commas and parse
                        cleaned = re.sub(r'[,$]', '', value)
                        result['core_fields'][canonical] = int(float(cleaned))
                    except (ValueError, TypeError):
                        result['extra_data'][csv_col] = value
                else:
                    result['core_fields'][canonical] = value
        
        # Store unmapped columns in extra_data
        for col in self.unmapped_columns:
            value = csv_row.get(col, '').strip()
            if value:
                result['extra_data'][col] = value
        
        return result


class LeadUploader:
    """Handles uploading leads to Supabase with deduplication"""
    
    def __init__(self, supabase_url: str, supabase_key: str, batch_size: int = 500):
        """Initialize uploader with Supabase credentials"""
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.batch_size = batch_size
        self.stats = {
            'total': 0,
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0
        }
        self.error_log = []
    
    def upload_csv(self, csv_path: str, source_type: str = 'unknown', 
                   test_mode: bool = False, test_limit: int = 1000) -> Dict[str, int]:
        """
        Upload a CSV file to Supabase
        
        Args:
            csv_path: Path to CSV file
            source_type: Type of source ('apollo', 'zoominfo', 'crunchbase', etc.)
            test_mode: If True, only process first test_limit rows
            test_limit: Number of rows to process in test mode
        """
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        source_filename = csv_path.name
        
        # Create upload stats record
        upload_stat = self.supabase.table('upload_stats').insert({
            'source_file': source_filename,
            'total_rows': 0,
            'status': 'in_progress'
        }).execute()
        upload_id = upload_stat.data[0]['id']
        
        print(f"\n{'='*60}")
        print(f"Uploading: {source_filename}")
        print(f"Source Type: {source_type}")
        print(f"Test Mode: {'YES (first ' + str(test_limit) + ' rows)' if test_mode else 'NO (full file)'}")
        print(f"{'='*60}\n")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames
                
                if not columns:
                    raise ValueError("CSV has no columns")
                
                # Initialize column mapper
                mapper = ColumnMapper(columns)
                
                print(f"Detected {len(columns)} columns in CSV")
                print(f"Mapped {len(mapper.mapping)} core fields")
                print(f"Extra data fields: {len(mapper.unmapped_columns)}\n")
                
                # Check for required email field
                if 'email' not in mapper.mapping:
                    raise ValueError("No email column found! Cannot proceed without email field.")
                
                # Read all rows (or test limit)
                rows = []
                for i, row in enumerate(reader):
                    if test_mode and i >= test_limit:
                        break
                    rows.append(row)
                
                total_rows = len(rows)
                self.stats['total'] = total_rows
                
                print(f"Processing {total_rows:,} rows...\n")
                
                # Process in batches
                batch = []
                with tqdm(total=total_rows, desc="Uploading leads") as pbar:
                    for row in rows:
                        try:
                            mapped = mapper.map_row(row)
                            
                            # Skip if no email
                            if 'email' not in mapped['core_fields']:
                                self.stats['skipped'] += 1
                                pbar.update(1)
                                continue
                            
                            # Prepare record
                            record = {
                                **mapped['core_fields'],
                                'extra_data': mapped['extra_data'],
                                'source_file': source_filename,
                                'source_type': source_type
                            }
                            
                            batch.append(record)
                            
                            # Upload batch when full
                            if len(batch) >= self.batch_size:
                                self._upload_batch(batch)
                                batch = []
                            
                            pbar.update(1)
                            
                        except Exception as e:
                            self.stats['errors'] += 1
                            self.error_log.append({
                                'row': row.get(mapper.get('email'), 'unknown'),
                                'error': str(e)
                            })
                            pbar.update(1)
                    
                    # Upload remaining batch
                    if batch:
                        self._upload_batch(batch)
                
                # Update upload stats
                self.supabase.table('upload_stats').update({
                    'total_rows': total_rows,
                    'inserted': self.stats['inserted'],
                    'updated': self.stats['updated'],
                    'skipped': self.stats['skipped'],
                    'errors': self.stats['errors'],
                    'completed_at': datetime.utcnow().isoformat(),
                    'status': 'completed',
                    'error_log': self.error_log[:100]  # Store first 100 errors
                }).eq('id', upload_id).execute()
                
                self._print_summary()
                return self.stats
                
        except Exception as e:
            # Mark upload as failed
            self.supabase.table('upload_stats').update({
                'status': 'failed',
                'completed_at': datetime.utcnow().isoformat(),
                'error_log': [{'error': str(e)}]
            }).eq('id', upload_id).execute()
            raise
    
    def _upload_batch(self, batch: List[Dict[str, Any]]):
        """Upload a batch with upsert (insert or update on conflict)"""
        try:
            # Supabase upsert: insert or update if email exists
            result = self.supabase.table('leads').upsert(
                batch,
                on_conflict='email',
                returning='minimal'
            ).execute()
            
            # Estimate inserted vs updated (Supabase doesn't return this info easily)
            # We'll count as inserted for now
            self.stats['inserted'] += len(batch)
            
        except Exception as e:
            # If batch fails, try individually to identify problem records
            for record in batch:
                try:
                    self.supabase.table('leads').upsert(
                        record,
                        on_conflict='email',
                        returning='minimal'
                    ).execute()
                    self.stats['inserted'] += 1
                except Exception as row_error:
                    self.stats['errors'] += 1
                    self.error_log.append({
                        'email': record.get('email', 'unknown'),
                        'error': str(row_error)
                    })
    
    def _print_summary(self):
        """Print upload summary"""
        print(f"\n{'='*60}")
        print("UPLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"Total rows:    {self.stats['total']:,}")
        print(f"Inserted:      {self.stats['inserted']:,}")
        print(f"Updated:       {self.stats['updated']:,}")
        print(f"Skipped:       {self.stats['skipped']:,}")
        print(f"Errors:        {self.stats['errors']:,}")
        print(f"{'='*60}\n")
        
        if self.error_log:
            print(f"First 5 errors:")
            for i, err in enumerate(self.error_log[:5], 1):
                print(f"  {i}. {err}")
            print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Upload CSV leads to Supabase',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test mode (first 1000 rows)
  python upload_leads.py sample_leads.csv --test
  
  # Full upload
  python upload_leads.py sample_leads.csv --source apollo
  
  # Custom test limit
  python upload_leads.py sample_leads.csv --test --limit 500
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV file to upload')
    parser.add_argument('--source', default='unknown', 
                       help='Source type (apollo, zoominfo, crunchbase, etc.)')
    parser.add_argument('--test', action='store_true',
                       help='Test mode - only upload first 1000 rows')
    parser.add_argument('--limit', type=int, default=1000,
                       help='Number of rows to process in test mode (default: 1000)')
    parser.add_argument('--batch-size', type=int, default=500,
                       help='Batch size for uploads (default: 500)')
    
    args = parser.parse_args()
    
    # Get Supabase credentials from environment
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("ERROR: Environment variables not set!")
        print("Please set: SUPABASE_URL and SUPABASE_KEY")
        print("\nExample:")
        print("  export SUPABASE_URL='https://your-project.supabase.co'")
        print("  export SUPABASE_KEY='your-anon-key'")
        sys.exit(1)
    
    # Initialize uploader
    uploader = LeadUploader(supabase_url, supabase_key, batch_size=args.batch_size)
    
    # Upload
    try:
        uploader.upload_csv(
            args.csv_file,
            source_type=args.source,
            test_mode=args.test,
            test_limit=args.limit
        )
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
