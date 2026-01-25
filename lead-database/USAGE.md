# Lead Database Usage Guide

How to work with your lead database after setup.

## Column Mapping Logic

The upload script automatically maps CSV columns to database fields using fuzzy matching.

### Core Fields (Always Mapped)

These fields are extracted and stored in dedicated columns:

| Database Field | Matches CSV Columns |
|----------------|-------------------|
| `email` | email, Email, EMAIL, email_address |
| `first_name` | first name, First Name, firstname, FirstName |
| `last_name` | last name, Last Name, lastname, LastName |
| `full_name` | full name, Full Name, name, Name |
| `title` | title, Title, job_title, Job Title, position |
| `company_name` | company name, Company Name, company, Company |
| `company_website` | company website, Company Website, website, domain |
| `mobile_number` | mobile number, Mobile Number, phone, Phone |
| `linkedin_url` | linkedin, LinkedIn, linkedin_url |
| `industry` | industry, Industry, sector, Sector |
| `city` | city, City |
| `state` | state, State, region, Region |
| `country` | country, Country |
| `company_employees_count` | employees count, Employees Count, employee_count |
| `company_annual_revenue` | company annual revenue clean, revenue |
| `email_validation_status` | validation status, Validation Status |

### Extra Data (Flexible Storage)

All columns that don't match core fields are stored in the `extra_data` JSONB column.

**Example from Paralect CSV:**
- "Keywords" → `extra_data->>'Keywords'`
- "Company Technologies" → `extra_data->>'Company Technologies'`
- "Person Photo" → `extra_data->>'Person Photo'`
- etc.

This means you **never lose data** - everything is preserved!

## Adding New CSV Files

### Quick Import Workflow

```bash
# 1. Always test first with a small sample
python upload_leads.py new_file.csv --test --source apollo

# 2. Review output - check mapped fields
# 3. If good, run full import
python upload_leads.py new_file.csv --source apollo

# 4. Check results in Supabase
```

### Handling Different CSV Formats

The script is smart about column variations:

**Example 1: Apollo Export**
- Columns: `First Name`, `Last Name`, `Work Email`, `Job Title`
- Script maps: `Work Email` → needs to be added to mapping

**Example 2: ZoomInfo Export**
- Columns: `first_name`, `last_name`, `email`, `title`
- Script maps: ✅ Already handled

**Example 3: Custom Export**
- Columns: `FirstName`, `Email`, `Company`
- Script maps: ✅ Already handled

### Adding Custom Mappings

If a CSV uses unusual column names, edit `upload_leads.py`:

```python
MAPPING_RULES = {
    'email': ['email', 'Email', 'work_email', 'Work Email'],  # Add your variations
    # ... rest of rules
}
```

## Query Examples

### Basic Queries

```sql
-- Get all leads from a company
SELECT * FROM leads
WHERE company_name ILIKE '%nichefire%';

-- Filter by country
SELECT email, first_name, company_name, title
FROM leads
WHERE country = 'United States'
LIMIT 100;

-- Find leads by title
SELECT email, first_name, last_name, company_name
FROM leads
WHERE title ILIKE '%founder%'
OR title ILIKE '%ceo%'
LIMIT 50;

-- Search by industry
SELECT email, company_name, title, city
FROM leads
WHERE industry ILIKE '%software%'
AND country = 'United States'
LIMIT 100;
```

### Advanced Queries

```sql
-- Leads from companies with 50-200 employees
SELECT email, first_name, company_name, company_employees_count
FROM leads
WHERE company_employees_count BETWEEN 50 AND 200
ORDER BY company_employees_count DESC;

-- Recently added leads
SELECT email, first_name, company_name, uploaded_at
FROM leads
WHERE uploaded_at > NOW() - INTERVAL '7 days'
ORDER BY uploaded_at DESC;

-- Leads with validated emails
SELECT email, first_name, company_name, email_validation_status
FROM leads
WHERE email_validation_status = 'valid'
LIMIT 100;

-- Group by company size
SELECT 
    CASE 
        WHEN company_employees_count < 50 THEN 'Small (1-49)'
        WHEN company_employees_count < 200 THEN 'Medium (50-199)'
        WHEN company_employees_count < 1000 THEN 'Large (200-999)'
        ELSE 'Enterprise (1000+)'
    END as company_size,
    COUNT(*) as lead_count
FROM leads
WHERE company_employees_count IS NOT NULL
GROUP BY company_size
ORDER BY lead_count DESC;
```

### Querying Extra Data (JSONB)

```sql
-- Access specific extra data field
SELECT 
    email,
    first_name,
    extra_data->>'Keywords' as keywords,
    extra_data->>'Company Technologies' as technologies
FROM leads
WHERE extra_data->>'Keywords' IS NOT NULL
LIMIT 10;

-- Search within extra data
SELECT email, company_name, extra_data->>'Company Technologies' as tech
FROM leads
WHERE extra_data->>'Company Technologies' ILIKE '%react%'
LIMIT 20;

-- Check if extra data contains specific key
SELECT email, first_name, extra_data
FROM leads
WHERE extra_data ? 'Company Logo'
LIMIT 10;
```

### Full-Text Search

```sql
-- Search company names
SELECT email, first_name, company_name, title
FROM leads
WHERE to_tsvector('english', company_name) @@ to_tsquery('english', 'software & startup');

-- Search person names
SELECT email, full_name, company_name
FROM leads
WHERE to_tsvector('english', COALESCE(full_name, '') || ' ' || COALESCE(first_name, '')) 
      @@ to_tsquery('english', 'john & smith');
```

### Statistics & Reporting

```sql
-- Overall stats (using view)
SELECT * FROM lead_stats;

-- Leads by source file
SELECT * FROM leads_by_source;

-- Top companies by lead count
SELECT 
    company_name,
    COUNT(*) as lead_count,
    STRING_AGG(DISTINCT country, ', ') as countries
FROM leads
WHERE company_name IS NOT NULL
GROUP BY company_name
ORDER BY lead_count DESC
LIMIT 20;

-- Leads by location
SELECT 
    country,
    state,
    city,
    COUNT(*) as leads
FROM leads
GROUP BY country, state, city
ORDER BY leads DESC
LIMIT 50;

-- Upload history
SELECT 
    source_file,
    total_rows,
    inserted,
    errors,
    started_at,
    completed_at
FROM upload_stats
ORDER BY started_at DESC;
```

## Exporting Data

### Export to CSV from Supabase

```sql
-- In Supabase SQL Editor, run query then click "Download CSV"
SELECT 
    email,
    first_name,
    last_name,
    company_name,
    title,
    city,
    country
FROM leads
WHERE country = 'United States'
AND title ILIKE '%ceo%';
```

### Export via Python

```python
from supabase import create_client
import csv
import os

# Connect
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Query
result = supabase.table('leads')\
    .select('email, first_name, last_name, company_name, title')\
    .eq('country', 'United States')\
    .execute()

# Write to CSV
with open('export.csv', 'w', newline='') as f:
    if result.data:
        writer = csv.DictWriter(f, fieldnames=result.data[0].keys())
        writer.writeheader()
        writer.writerows(result.data)

print(f"Exported {len(result.data)} leads")
```

## Deduplication Strategy

### How It Works

- **Primary Key**: `email` column (unique)
- **On Import**: If email exists, the record is **updated** (not duplicated)
- **Result**: Always have latest data per email

### Checking for Duplicates

```sql
-- Should return 0 if working correctly
SELECT email, COUNT(*) as count
FROM leads
GROUP BY email
HAVING COUNT(*) > 1;
```

### Handling Multiple Sources

When the same person appears in multiple CSVs:
- First import creates the record
- Subsequent imports update it
- All data from all sources is merged
- `source_file` shows the LATEST source
- `updated_at` shows when last modified

## Best Practices

### 1. Always Test First
```bash
# Before importing 500k rows, test 1000
python upload_leads.py huge_file.csv --test --limit 1000
```

### 2. Tag Your Sources
```bash
# Use descriptive source types
python upload_leads.py file.csv --source apollo-q1-2024
python upload_leads.py file.csv --source zoominfo-tech-companies
```

### 3. Monitor Upload Stats
```sql
-- Check recent uploads
SELECT * FROM upload_stats ORDER BY started_at DESC LIMIT 10;

-- Find failed uploads
SELECT * FROM upload_stats WHERE status = 'failed';
```

### 4. Regular Cleanup
```sql
-- Remove leads without email (shouldn't happen, but just in case)
DELETE FROM leads WHERE email IS NULL OR email = '';

-- Remove test uploads
DELETE FROM leads WHERE source_file LIKE '%test%';
```

### 5. Backup Before Major Operations
```sql
-- Supabase has automatic backups, but for safety:
-- Use "Table Editor" → Select table → "Download as CSV"
```

## Performance Tips

### Indexes Are Your Friend

Already created for you:
- Email (unique)
- Company name
- Title
- Industry
- Country
- Full-text search on company/names
- JSONB (extra_data)

### For Large Queries

```sql
-- Use LIMIT to test queries first
SELECT * FROM leads WHERE ... LIMIT 100;

-- Then remove for full results
SELECT * FROM leads WHERE ...;

-- For very large exports, use pagination
SELECT * FROM leads LIMIT 10000 OFFSET 0;
SELECT * FROM leads LIMIT 10000 OFFSET 10000;
```

### Optimize Batch Size

```bash
# Faster (more memory, higher rate limit usage)
python upload_leads.py file.csv --batch-size 1000

# Slower (less memory, safer for free tier)
python upload_leads.py file.csv --batch-size 100
```

## Common Use Cases

### 1. Find Decision Makers at Target Companies

```sql
SELECT email, first_name, last_name, title, company_name
FROM leads
WHERE company_name IN ('Nichefire', 'Guardian Owl Digital')
AND (title ILIKE '%ceo%' OR title ILIKE '%founder%' OR title ILIKE '%cto%');
```

### 2. Geographic Targeting

```sql
SELECT email, first_name, company_name, city, state
FROM leads
WHERE country = 'United States'
AND state IN ('California', 'New York', 'Texas')
AND company_employees_count > 50;
```

### 3. Industry + Role Targeting

```sql
SELECT email, first_name, company_name, title, industry
FROM leads
WHERE industry ILIKE '%software%'
AND (title ILIKE '%head of%' OR title ILIKE '%director%' OR title ILIKE '%vp%');
```

### 4. Company Size Filtering

```sql
SELECT email, first_name, company_name, company_employees_count
FROM leads
WHERE company_employees_count BETWEEN 10 AND 50
AND industry ILIKE '%saas%';
```

## Troubleshooting

### Query is slow
- Check if you're using indexed columns (email, company_name, title, etc.)
- Add LIMIT for testing
- Consider adding more indexes if needed

### Can't find a column
- Check if it's in `extra_data`: `SELECT extra_data FROM leads LIMIT 1;`
- Query it: `extra_data->>'Column Name'`

### Wrong data type
- Numeric fields might be in `extra_data` if CSV had non-numeric values
- Check and clean: `SELECT extra_data->>'field' FROM leads WHERE ...`

## Need Help?

- Check Supabase docs: https://supabase.com/docs
- SQL reference: https://www.postgresql.org/docs/
- This is PostgreSQL - any Postgres tutorial applies!
