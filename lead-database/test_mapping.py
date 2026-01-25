#!/usr/bin/env python3
"""
Test column mapping logic without uploading to Supabase
Useful for verifying CSV compatibility before actual import
"""

import csv
import sys
from pathlib import Path

# Import the mapper class from upload script
sys.path.insert(0, str(Path(__file__).parent))
from upload_leads import ColumnMapper


def test_csv_mapping(csv_path: str, num_rows: int = 5):
    """Test column mapping on a CSV file"""
    
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"ERROR: File not found: {csv_path}")
        return
    
    print(f"\n{'='*70}")
    print(f"Testing CSV Mapping: {csv_path.name}")
    print(f"{'='*70}\n")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        
        if not columns:
            print("ERROR: No columns found in CSV")
            return
        
        # Initialize mapper
        mapper = ColumnMapper(columns)
        
        # Print mapping results
        print(f"Total CSV Columns: {len(columns)}")
        print(f"Mapped Core Fields: {len(mapper.mapping)}")
        print(f"Extra Data Fields: {len(mapper.unmapped_columns)}\n")
        
        print("CORE FIELD MAPPING:")
        print("-" * 70)
        for canonical, csv_col in sorted(mapper.mapping.items()):
            print(f"  {canonical:30s} ← {csv_col}")
        
        print(f"\nEXTRA DATA FIELDS ({len(mapper.unmapped_columns)} total):")
        print("-" * 70)
        for col in mapper.unmapped_columns[:20]:  # Show first 20
            print(f"  • {col}")
        if len(mapper.unmapped_columns) > 20:
            print(f"  ... and {len(mapper.unmapped_columns) - 20} more")
        
        # Show sample mapped rows
        print(f"\nSAMPLE MAPPED ROWS ({num_rows}):")
        print("=" * 70)
        
        for i, row in enumerate(reader):
            if i >= num_rows:
                break
            
            mapped = mapper.map_row(row)
            
            print(f"\nRow {i+1}:")
            print(f"  Email: {mapped['core_fields'].get('email', 'N/A')}")
            print(f"  Name: {mapped['core_fields'].get('first_name', '')} {mapped['core_fields'].get('last_name', '')}")
            print(f"  Company: {mapped['core_fields'].get('company_name', 'N/A')}")
            print(f"  Title: {mapped['core_fields'].get('title', 'N/A')}")
            print(f"  Extra Data Keys: {len(mapped['extra_data'])} fields")
        
        print(f"\n{'='*70}")
        print("✓ Mapping test complete!")
        print(f"{'='*70}\n")
        
        # Check for email
        if 'email' not in mapper.mapping:
            print("⚠️  WARNING: No email field detected!")
            print("   Upload will fail without an email column.")
            print("   CSV must have one of: email, Email, EMAIL, email_address\n")
        else:
            print("✓ Email field detected - ready for upload!")
            print(f"  Using CSV column: '{mapper.get('email')}'\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test CSV column mapping without uploading',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test mapping on sample CSV
  python test_mapping.py /root/clawd/sample_leads.csv
  
  # Show more sample rows
  python test_mapping.py data.csv --rows 10
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV file to test')
    parser.add_argument('--rows', type=int, default=5,
                       help='Number of sample rows to display (default: 5)')
    
    args = parser.parse_args()
    
    test_csv_mapping(args.csv_file, args.rows)


if __name__ == '__main__':
    main()
