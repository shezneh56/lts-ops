# Lead Database System - Complete Documentation Index

## 📚 Start Here

New to this project? Read documents in this order:

1. **README.md** - Overview and quick start (5 min read)
2. **SETUP.md** - Step-by-step setup instructions (10 min to complete)
3. **Test with:** `./venv/bin/python test_mapping.py /root/clawd/sample_leads.csv`
4. **QUICK_REFERENCE.md** - Command cheat sheet (bookmark this!)
5. **USAGE.md** - Query examples and patterns (reference as needed)

## 📖 Documentation Files

### Getting Started
| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Project overview, features, quick start | First thing - understand what this is |
| **SETUP.md** | Complete setup guide (Supabase + Python) | Before using - one-time setup |
| **PROJECT_SUMMARY.md** | What's built, testing status, next steps | To understand project scope |
| **INDEX.md** | This file - documentation index | When you're lost |

### Usage & Reference
| File | Purpose | When to Read |
|------|---------|--------------|
| **QUICK_REFERENCE.md** | One-page command cheat sheet | Daily use - quick lookup |
| **USAGE.md** | Query examples, best practices, tips | When you need to query/export data |
| **ARCHITECTURE.md** | System design, data flow, internals | When you want to understand/extend |

### Core Files
| File | Purpose | Type |
|------|---------|------|
| **schema.sql** | Database schema for Supabase | SQL |
| **upload_leads.py** | Smart CSV import script | Python |
| **test_mapping.py** | Test column mapping without uploading | Python |
| **requirements.txt** | Python dependencies | Text |
| **.env.example** | Environment variable template | Config |
| **activate.sh** | Helper to activate venv + load env vars | Shell |

## 🎯 Common Tasks

### Setup Tasks
```bash
# 1. Create Supabase project
→ See SETUP.md "Step 1"

# 2. Run database schema
→ See SETUP.md "Step 2"

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials
source activate.sh

# 4. Test
./venv/bin/python test_mapping.py /root/clawd/sample_leads.csv
```

### Daily Tasks
```bash
# Import CSV (test mode)
./venv/bin/python upload_leads.py file.csv --test --source apollo

# Import CSV (full)
./venv/bin/python upload_leads.py file.csv --source apollo

# Check column mapping
./venv/bin/python test_mapping.py file.csv

# Activate environment (loads .env)
source activate.sh
```

### Query Tasks
```sql
-- See USAGE.md for 20+ examples
-- Quick stats
SELECT * FROM lead_stats;

-- Search
SELECT * FROM leads WHERE company_name ILIKE '%startup%';

-- Upload history
SELECT * FROM upload_stats ORDER BY started_at DESC;
```

## 🔍 Find Information

### How do I...

**...set up Supabase?**
→ SETUP.md (Steps 1-2)

**...import my first CSV?**
→ SETUP.md (Steps 4-5) or QUICK_REFERENCE.md

**...query the database?**
→ USAGE.md "Query Examples" section

**...handle different CSV formats?**
→ USAGE.md "Handling Different CSV Formats"
→ ARCHITECTURE.md "Column Mapper"

**...understand how deduplication works?**
→ ARCHITECTURE.md "Deduplication Strategy"

**...query extra data fields?**
→ USAGE.md "Querying Extra Data (JSONB)"

**...export leads?**
→ USAGE.md "Exporting Data"

**...troubleshoot errors?**
→ SETUP.md "Troubleshooting"
→ USAGE.md "Troubleshooting"

**...understand the system design?**
→ ARCHITECTURE.md (complete technical docs)

**...add custom column mappings?**
→ ARCHITECTURE.md "Extensibility"

**...check what's been built?**
→ PROJECT_SUMMARY.md

## 📁 File Structure

```
lead-database/
│
├── 📘 Documentation (you are here)
│   ├── INDEX.md                  ← This file
│   ├── README.md                 ← Start here
│   ├── SETUP.md                  ← Setup guide
│   ├── USAGE.md                  ← Query examples
│   ├── QUICK_REFERENCE.md        ← Cheat sheet
│   ├── PROJECT_SUMMARY.md        ← What's built
│   └── ARCHITECTURE.md           ← Technical design
│
├── 🔧 Core Files
│   ├── schema.sql                ← Database schema
│   ├── upload_leads.py           ← Import script
│   ├── test_mapping.py           ← Mapping test script
│   └── activate.sh               ← Helper script
│
├── ⚙️ Configuration
│   ├── .env.example              ← Environment template
│   ├── requirements.txt          ← Python deps
│   └── .env                      ← Your config (create this!)
│
└── 🐍 Virtual Environment
    └── venv/                     ← Python packages
```

## 🚀 Quick Start Paths

### Path 1: Just Want to Import CSVs
1. Read: README.md (understand what this does)
2. Follow: SETUP.md steps 1-5 (one-time setup)
3. Use: QUICK_REFERENCE.md (daily commands)
4. Done! 🎉

### Path 2: Need to Query/Export Data
1. Setup done? Skip to USAGE.md
2. Find your use case in "Query Examples"
3. Copy/modify SQL query
4. Done! 🎉

### Path 3: Want to Understand Everything
1. README.md → Overview
2. ARCHITECTURE.md → How it works
3. SETUP.md → How to set up
4. USAGE.md → How to use
5. PROJECT_SUMMARY.md → Project status
6. You're now an expert! 🎓

### Path 4: Something's Broken
1. Check error message (they're helpful!)
2. SETUP.md "Troubleshooting"
3. USAGE.md "Troubleshooting"
4. Still stuck? Check test script output:
   ```bash
   ./venv/bin/python test_mapping.py your_file.csv
   ```

## 💡 Pro Tips

**Before importing a huge CSV:**
```bash
# Always test first!
./venv/bin/python upload_leads.py huge_file.csv --test --limit 100
```

**Check column mapping before uploading:**
```bash
./venv/bin/python test_mapping.py new_file.csv
```

**Activate environment easily:**
```bash
source activate.sh  # Loads venv + .env in one command
```

**Bookmark these:**
- QUICK_REFERENCE.md for commands
- USAGE.md for SQL queries

## 📊 Sample Data

**Test CSV:** `/root/clawd/sample_leads.csv`
- 208,973 rows
- 53 columns
- Paralect Q1 data (US/Canada SaaS startups)

**Test it:**
```bash
./venv/bin/python test_mapping.py /root/clawd/sample_leads.csv
./venv/bin/python upload_leads.py /root/clawd/sample_leads.csv --test
```

## 🆘 Support

**Error Messages:** Read them! They're designed to be helpful.

**Missing something?** Check this index to find the right doc.

**Environment issues:**
```bash
# Check environment
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Reload
source activate.sh
```

**Import issues:**
```bash
# Test column mapping first
./venv/bin/python test_mapping.py your_file.csv
```

## 📝 Notes

- **All scripts use Python 3** (not python, use python3 or ./venv/bin/python)
- **Virtual environment is pre-configured** (venv/ directory)
- **Dependencies already installed** in venv
- **Documentation is complete** - everything you need is here
- **Sample CSV ready** at `/root/clawd/sample_leads.csv`

## ✅ Checklist

Before your first import:
- [ ] Read README.md
- [ ] Create Supabase project
- [ ] Run schema.sql in Supabase
- [ ] Create .env file (from .env.example)
- [ ] Test: `source activate.sh`
- [ ] Test: `./venv/bin/python test_mapping.py /root/clawd/sample_leads.csv`
- [ ] Import test: `./venv/bin/python upload_leads.py /root/clawd/sample_leads.csv --test`

---

**You have everything you need to succeed!** 🚀

Start with README.md if you haven't already.
