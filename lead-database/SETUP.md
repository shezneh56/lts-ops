# Lead Database Setup Guide

Complete step-by-step instructions to get your lead database running.

## Prerequisites

- Python 3.8+ installed
- A Supabase account (free tier works great)

## Step 1: Create Supabase Project

1. **Sign up for Supabase**
   - Go to [https://supabase.com](https://supabase.com)
   - Click "Start your project" → Sign in with GitHub (recommended)

2. **Create a new project**
   - Click "New Project"
   - Organization: Create new or use existing
   - Name: `lead-database` (or whatever you prefer)
   - Database Password: Generate a strong password → **SAVE THIS**
   - Region: Choose closest to you (e.g., `US West` for California)
   - Pricing Plan: **Free** (500 MB database, 50,000 monthly active users)
   - Click "Create new project"
   - Wait ~2 minutes for provisioning

3. **Get your API credentials**
   - Once project is ready, go to Settings (⚙️) → API
   - Copy these values:
     - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
     - **anon public key**: `eyJhbGc...` (long string)

## Step 2: Set Up Database Schema

1. **Open SQL Editor**
   - In Supabase dashboard, click "SQL Editor" in left sidebar
   - Click "New Query"

2. **Run the schema**
   - Copy the entire contents of `schema.sql`
   - Paste into the SQL Editor
   - Click "Run" (or press Cmd/Ctrl + Enter)
   - You should see "Success. No rows returned"

3. **Verify tables**
   - Click "Table Editor" in left sidebar
   - You should see:
     - `leads` table
     - `upload_stats` table
   - Click on `leads` table to see the structure

## Step 3: Install Python Dependencies

```bash
cd /root/clawd/lead-database

# Install required packages
pip install supabase tqdm

# Or using requirements.txt
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

Create a `.env` file or export variables:

```bash
# Create .env file (recommended)
cat > .env << 'EOF'
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
EOF

# Or export directly (temporary, lost on shell restart)
export SUPABASE_URL='https://xxxxxxxxxxxxx.supabase.co'
export SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

**IMPORTANT**: Replace with YOUR actual Supabase URL and key!

If using `.env` file, load it before running:
```bash
export $(cat .env | xargs)
```

## Step 5: Test Upload (Recommended)

Test with first 1000 rows before full import:

```bash
# Make script executable
chmod +x upload_leads.py

# Test upload
python upload_leads.py /root/clawd/sample_leads.csv --test --source paralect
```

Expected output:
```
============================================================
Uploading: sample_leads.csv
Source Type: paralect
Test Mode: YES (first 1000 rows)
============================================================

Detected 52 columns in CSV
Mapped 22 core fields
Extra data fields: 30

Processing 1,000 rows...

Uploading leads: 100%|████████████| 1000/1000 [00:05<00:00, 180.23it/s]

============================================================
UPLOAD SUMMARY
============================================================
Total rows:    1,000
Inserted:      998
Updated:       0
Skipped:       2
Errors:        0
============================================================
```

## Step 6: Verify Data

1. **Check in Supabase**
   - Go to Table Editor → `leads`
   - You should see ~1000 rows
   - Click on a row to see all fields including `extra_data` JSONB

2. **Check upload stats**
   - Go to Table Editor → `upload_stats`
   - You should see your upload record

3. **Run a query** (SQL Editor)
   ```sql
   -- Get total counts
   SELECT * FROM lead_stats;
   
   -- View leads by source
   SELECT * FROM leads_by_source;
   
   -- Search for a company
   SELECT email, first_name, last_name, company_name, title
   FROM leads
   WHERE company_name ILIKE '%nichefire%'
   LIMIT 10;
   ```

## Step 7: Full Upload (When Ready)

Once test looks good, run full import:

```bash
# Full upload of all 208k+ leads
python upload_leads.py /root/clawd/sample_leads.csv --source paralect

# This will take ~15-20 minutes for 208k rows
```

## Step 8: Import Additional CSV Files

For new CSV files from different sources:

```bash
# Apollo export
python upload_leads.py /path/to/apollo_export.csv --source apollo

# ZoomInfo export
python upload_leads.py /path/to/zoominfo_leads.csv --source zoominfo

# Test mode first if unsure
python upload_leads.py /path/to/new_file.csv --test --source apollo
```

The script will:
- Auto-detect column names (handles variations)
- Deduplicate by email (updates existing leads)
- Store all extra columns in `extra_data` JSONB

## Troubleshooting

### "Environment variables not set"
```bash
# Check if variables are set
echo $SUPABASE_URL
echo $SUPABASE_KEY

# If empty, export them or load .env
export $(cat .env | xargs)
```

### "No email column found"
- Your CSV must have an email column
- Check CSV headers - script looks for: `email`, `Email`, `EMAIL`, `email_address`
- If different, add to `MAPPING_RULES` in script

### "SSL certificate verify failed"
```bash
# Install certificates
pip install --upgrade certifi
```

### Import is slow
- Normal for large files (208k rows ≈ 15-20 min)
- Adjust batch size: `--batch-size 1000` (larger = faster but more memory)
- Free tier has rate limits - don't worry if it slows down

### Duplicate key error
- This is normal! It means email already exists
- Script handles this automatically with upsert

## Next Steps

- Read `USAGE.md` for query examples and tips
- Set up automated imports (optional)
- Create dashboards in Supabase

## Support

Having issues? Check:
1. Supabase project is active (check dashboard)
2. Environment variables are set correctly
3. CSV file path is correct
4. You're using the anon/public key (not service role key)

Still stuck? Review error messages - they're usually helpful!
