# Quick Reference Card

## Setup (One Time)

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Set environment variables
export SUPABASE_URL='https://xxxxx.supabase.co'
export SUPABASE_KEY='eyJhbGc...'

# 3. Run schema.sql in Supabase SQL Editor
```

## Upload Commands

```bash
# Test mode (first 1000 rows)
python upload_leads.py file.csv --test

# Test with custom limit
python upload_leads.py file.csv --test --limit 500

# Full upload
python upload_leads.py file.csv --source apollo

# With batch size
python upload_leads.py file.csv --source zoominfo --batch-size 1000
```

## Common Queries

```sql
-- Overall stats
SELECT * FROM lead_stats;

-- Leads by source
SELECT * FROM leads_by_source;

-- Search companies
SELECT * FROM leads WHERE company_name ILIKE '%startup%' LIMIT 100;

-- Filter by title
SELECT * FROM leads WHERE title ILIKE '%ceo%' OR title ILIKE '%founder%';

-- Geographic filter
SELECT * FROM leads WHERE country = 'United States' AND state = 'California';

-- Company size
SELECT * FROM leads WHERE company_employees_count BETWEEN 50 AND 200;

-- Recent uploads
SELECT * FROM leads WHERE uploaded_at > NOW() - INTERVAL '7 days';

-- Query extra data
SELECT email, extra_data->>'Keywords' FROM leads LIMIT 10;

-- Upload history
SELECT * FROM upload_stats ORDER BY started_at DESC;
```

## Python Query Examples

```python
from supabase import create_client
import os

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

# Simple query
result = supabase.table('leads')\
    .select('email, first_name, company_name')\
    .eq('country', 'United States')\
    .limit(100)\
    .execute()

# Filter by title
result = supabase.table('leads')\
    .select('*')\
    .ilike('title', '%founder%')\
    .execute()

# Multiple filters
result = supabase.table('leads')\
    .select('email, company_name, title')\
    .eq('country', 'United States')\
    .gte('company_employees_count', 50)\
    .lte('company_employees_count', 200)\
    .execute()

print(f"Found {len(result.data)} leads")
for lead in result.data:
    print(f"{lead['email']} - {lead['company_name']}")
```

## Troubleshooting

```bash
# Check env vars
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Load from .env file
export $(cat .env | xargs)

# Test connection
python -c "from supabase import create_client; import os; c = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')); print('Connected!')"
```

## File Structure

```
lead-database/
├── README.md              # Overview
├── SETUP.md              # Step-by-step setup
├── USAGE.md              # Detailed usage guide
├── QUICK_REFERENCE.md    # This file
├── schema.sql            # Database schema
├── upload_leads.py       # Import script
└── requirements.txt      # Python deps
```

## Column Mapping

Auto-mapped fields:
- email, first_name, last_name, full_name
- title, company_name, company_website
- mobile_number, linkedin_url
- industry, headline, seniority, department
- city, state, country
- company_linkedin, company_employees_count
- company_annual_revenue, company_total_funding
- email_validation_status

Everything else → `extra_data` JSONB column

## Tips

- Always test first: `--test`
- Tag your sources: `--source apollo-q1-2024`
- Use views: `SELECT * FROM lead_stats;`
- Query extra data: `extra_data->>'Field Name'`
- Check uploads: `SELECT * FROM upload_stats;`

## Support

- SETUP.md - Setup instructions
- USAGE.md - Query examples
- Error messages are helpful - read them!
