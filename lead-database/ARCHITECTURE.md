# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CSV FILES (Data Sources)                  │
│  Apollo.csv │ ZoomInfo.csv │ Crunchbase.csv │ Custom.csv   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              upload_leads.py (Smart Importer)                │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Column Mapper                                    │   │
│  │     - Auto-detect CSV column names                   │   │
│  │     - Map to core fields (23 mappings)              │   │
│  │     - Identify extra fields for JSONB               │   │
│  └─────────────────────────────────────────────────────┘   │
│                       │                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2. Data Processor                                   │   │
│  │     - Parse and validate rows                        │   │
│  │     - Handle data types (int, text, etc.)           │   │
│  │     - Build JSONB for extra fields                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                       │                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  3. Batch Uploader                                   │   │
│  │     - Group 500 rows per batch                       │   │
│  │     - Upsert (insert or update on conflict)         │   │
│  │     - Track success/errors                           │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   SUPABASE (PostgreSQL)                      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  leads table                                         │   │
│  │  ┌─────────────────┐  ┌────────────────────────┐   │   │
│  │  │  Core Fields    │  │  Flexible Storage      │   │   │
│  │  │                 │  │                        │   │   │
│  │  │  • email  ◄──────────┐ (unique key)        │   │   │
│  │  │  • first_name   │  │  extra_data (JSONB)   │   │   │
│  │  │  • last_name    │  │  {                     │   │   │
│  │  │  • title        │  │    "Keywords": "...",  │   │   │
│  │  │  • company_name │  │    "Technologies": "..." │   │
│  │  │  • industry     │  │  }                     │   │   │
│  │  │  • city         │  │                        │   │   │
│  │  │  • country      │  │                        │   │   │
│  │  │  • ...          │  │                        │   │   │
│  │  └─────────────────┘  └────────────────────────┘   │   │
│  │                                                      │   │
│  │  Metadata:                                           │   │
│  │  • source_file, source_type                         │   │
│  │  • uploaded_at, updated_at                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  upload_stats table                                  │   │
│  │  • Track each import job                            │   │
│  │  • Success/error counts                             │   │
│  │  • Error logs                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Indexes (Fast Queries)                              │   │
│  │  • email (unique)                                    │   │
│  │  • company_name                                      │   │
│  │  • title, industry, country                         │   │
│  │  • Full-text search on names/companies              │   │
│  │  • JSONB GIN index on extra_data                    │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  QUERY & USAGE LAYER                         │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ SQL Queries  │  │ Python API   │  │ Supabase UI  │      │
│  │              │  │              │  │              │      │
│  │ • Search     │  │ • Export     │  │ • Browse     │      │
│  │ • Filter     │  │ • Analytics  │  │ • Download   │      │
│  │ • Aggregate  │  │ • Integration│  │ • Visualize  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Import Process

1. **CSV Read**
   - Load CSV file
   - Detect column headers
   - Initialize Column Mapper

2. **Column Mapping**
   - Match CSV columns to core fields
   - Example: "First Name" → `first_name`
   - Identify unmapped columns for `extra_data`

3. **Row Processing**
   - For each row:
     - Extract core field values
     - Build JSONB object with extra fields
     - Validate email (required)
     - Handle data type conversions

4. **Batch Upload**
   - Group 500 rows
   - Upsert to Supabase
   - On conflict (email exists): UPDATE
   - Track success/errors

5. **Statistics**
   - Record to `upload_stats`
   - Total rows, inserted, updated, errors
   - Error logs (first 100)

### Query Process

**SQL Direct:**
```sql
SELECT email, first_name, company_name, extra_data->>'Keywords'
FROM leads
WHERE company_name ILIKE '%startup%';
```

**Python API:**
```python
result = supabase.table('leads')\
    .select('email, first_name, company_name')\
    .ilike('company_name', '%startup%')\
    .execute()
```

**Supabase UI:**
- Table Editor → Browse/filter visually
- SQL Editor → Run custom queries
- Download as CSV

## Core Components

### 1. Column Mapper (`ColumnMapper` class)

**Purpose:** Auto-detect and map CSV columns to database schema

**Features:**
- 23 pre-defined core field mappings
- Case-insensitive matching
- Handles variations (spaces, underscores, camelCase)
- Identifies unmapped columns for JSONB storage

**Example Mappings:**
```python
'email': ['email', 'Email', 'EMAIL', 'email_address']
'first_name': ['first name', 'First Name', 'firstname', 'FirstName']
'title': ['title', 'Title', 'job_title', 'Job Title', 'position']
```

### 2. Lead Uploader (`LeadUploader` class)

**Purpose:** Handle CSV upload to Supabase with batching and error handling

**Features:**
- Batch processing (configurable size, default 500)
- Upsert logic (insert or update on email conflict)
- Progress tracking with tqdm
- Error logging and recovery
- Statistics tracking

**Methods:**
- `upload_csv()` - Main upload function
- `_upload_batch()` - Batch upsert to Supabase
- `_print_summary()` - Display upload results

### 3. Database Schema

**Tables:**

**`leads`**
- Primary data table
- 23 core fields + JSONB extra_data
- Email unique constraint
- 10+ indexes for performance
- Auto-update timestamp trigger

**`upload_stats`**
- Import job tracking
- Success/error metrics
- Error logs (JSONB array)

**Views:**
- `lead_stats` - Overall statistics
- `leads_by_source` - Breakdown by source file

## Deduplication Strategy

### Email as Primary Key

```
┌────────────────────────────────────────┐
│  First Import: user@example.com        │
│  ► INSERT new row                      │
└────────────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────┐
│  Second Import: user@example.com       │
│  ► UPDATE existing row                 │
│  ► Merge new data                      │
│  ► Update timestamp                    │
└────────────────────────────────────────┘
```

**Implementation:**
```python
supabase.table('leads').upsert(
    record,
    on_conflict='email'  # If email exists, UPDATE
)
```

**Result:**
- Always one row per email
- Latest data from most recent import
- No duplicates

## Flexible Schema Strategy

### Core Fields vs Extra Data

```
CSV Column          Database Storage
─────────────────   ─────────────────────────────
"Email"         →   email (TEXT column)
"First Name"    →   first_name (TEXT column)
"Title"         →   title (TEXT column)
"Keywords"      →   extra_data->>'Keywords' (JSONB)
"Technologies"  →   extra_data->>'Technologies' (JSONB)
"Custom Field"  →   extra_data->>'Custom Field' (JSONB)
```

**Advantages:**
- ✅ Never lose data (everything stored)
- ✅ Fast queries on common fields (indexed columns)
- ✅ Flexible for source-specific data (JSONB)
- ✅ No schema changes needed for new CSVs

**Querying Extra Data:**
```sql
-- Access JSONB field
SELECT extra_data->>'Keywords' FROM leads;

-- Search in JSONB
WHERE extra_data->>'Technologies' ILIKE '%react%';

-- Check if key exists
WHERE extra_data ? 'Company Logo';
```

## Performance Considerations

### Indexing Strategy

**B-tree indexes** (exact/range queries):
- email (unique)
- company_name
- title, industry, country
- uploaded_at

**GIN indexes** (full-text search):
- Company name full-text
- Person name full-text
- JSONB extra_data

**Impact:**
- Fast lookups on indexed columns
- Efficient full-text search
- Scalable to 500k+ leads on free tier

### Batch Upload

**Why batching:**
- Reduce API calls (1 call per 500 rows vs 500 calls)
- Faster overall upload
- Better handling of rate limits
- Lower memory usage

**Tradeoffs:**
- Batch size too large → memory issues, harder error recovery
- Batch size too small → slow uploads, more API calls
- 500 rows = good balance for most use cases

### Rate Limiting (Free Tier)

Supabase free tier limits:
- API requests: varies by endpoint
- Database connections: 60
- Storage: 500 MB

**Mitigation:**
- Batch uploads reduce request count
- Connection pooling handled by Supabase client
- Progress tracking prevents timeout issues

## Extensibility

### Adding New Column Mappings

Edit `upload_leads.py`:
```python
MAPPING_RULES = {
    'email': ['email', 'work_email', 'corporate_email'],  # Add variations
    # ... existing mappings
}
```

### Adding New Core Fields

1. Update `schema.sql`:
```sql
ALTER TABLE leads ADD COLUMN new_field TEXT;
CREATE INDEX idx_leads_new_field ON leads(new_field);
```

2. Add to `MAPPING_RULES` in `upload_leads.py`

3. Existing data unaffected (backward compatible)

### Custom Processing

Add to `LeadUploader._upload_batch()`:
```python
# Custom validation/enrichment before upload
for record in batch:
    record['custom_field'] = process(record['email'])
```

## Error Handling

### Row-Level Errors

```
Batch of 500 rows
├── Row 1-499: Success ✓
└── Row 500: ERROR (invalid email)
    ├── Logged to error_log
    └── Upload continues
```

**Recovery:**
- Individual row failures don't crash batch
- Errors logged to `upload_stats.error_log`
- Show first 100 errors in summary

### Upload-Level Errors

```
Upload job fails
├── Mark upload_stats as 'failed'
├── Log error message
└── Cleanup (no partial data)
```

## Security Considerations

### Supabase Row Level Security (RLS)

**Current setup:** Uses anon/public key (no RLS)

**For production:** Enable RLS policies:
```sql
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Only authenticated users can read
CREATE POLICY "Authenticated users can read leads"
ON leads FOR SELECT
TO authenticated
USING (true);

-- Only service role can insert/update
CREATE POLICY "Service role can manage leads"
ON leads FOR ALL
TO service_role
USING (true);
```

### Environment Variables

- Never commit `.env` to git
- Use `.env.example` as template
- Store secrets in secure location

### Data Privacy

- Supabase hosted in chosen region
- GDPR compliant
- Encryption at rest and in transit

## Monitoring & Maintenance

### Check Upload Health

```sql
SELECT * FROM upload_stats ORDER BY started_at DESC LIMIT 10;
```

### Database Size

```sql
SELECT pg_size_pretty(pg_total_relation_size('leads'));
```

### Find Duplicates (Should be 0)

```sql
SELECT email, COUNT(*)
FROM leads
GROUP BY email
HAVING COUNT(*) > 1;
```

### Clean Test Data

```sql
DELETE FROM leads WHERE source_file LIKE '%test%';
DELETE FROM upload_stats WHERE source_file LIKE '%test%';
```

## Technology Stack

- **Database:** Supabase (PostgreSQL 15)
- **Language:** Python 3.8+
- **Libraries:**
  - `supabase-py` - Supabase client
  - `tqdm` - Progress bars
  - `python-dotenv` - Environment variables
- **CSV Parsing:** Native Python `csv` module
- **Data Format:** JSONB for flexible storage

---

**Simple, scalable, and maintainable** - designed for real-world use.
