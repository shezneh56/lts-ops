# Apollo Company Export Automation Research

**Date:** January 2026  
**Purpose:** Automate the manual process of exporting companies from Apollo.io for Clay enrichment

## Current Manual Process Pain Points
1. Search for companies with keyword/geography/employee filters
2. If results >10k, must slice by employee count ranges to get under 10k per export
3. Export each batch manually
4. Download CSVs
5. Upload to Clay for enrichment

**Current time: 1-2 days of manual work for large searches**

---

## Option 1: Apollo API (Organization Search)

### Overview
Apollo has a **REST API** with an Organization Search endpoint that can programmatically search and export companies.

**Endpoint:** `POST https://api.apollo.io/api/v1/mixed_companies/search`

### Key Details
- **Display Limit:** 50,000 records maximum (100 records per page, up to 500 pages)
- **Credits:** Consumes credits from your Apollo pricing plan
- **Filters:** Keywords, geography, employee count, industry, technology, funding, revenue, etc.

### API Features
- Organization Search (company discovery)
- Organization Enrichment (enhance existing company data)
- Bulk Organization Enrichment (batch processing)
- Job Postings lookup
- News Articles search

### Pricing
- API access varies by plan tier
- Basic API access on all plans
- Advanced API access requires higher tiers
- Credits consumed per search/enrichment call
- "Unlimited" plans have fair use limits: 10k credits/month (free) or up to 1M credits/year (paid)

### Assessment
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 8/10 |
| **Cost** | Varies by existing plan ($0-$$$ depending on credit usage) |
| **Build Time** | 1-2 days for basic script |
| **Pros** | Official API, reliable, full data access, no risk of account ban |
| **Cons** | 50k record limit per query, credit consumption, requires slicing logic for large sets |

### Recommended Approach
```python
# Pseudo-code for API automation
1. Query with broad filters to get total count
2. If >50k results, automatically slice by employee ranges
3. Paginate through each slice (100 records/page, up to 500 pages)
4. Export to CSV or directly push to Clay via HTTP API
5. Run overnight with rate limiting
```

---

## Option 2: Apify Scrapers

### Available Actors

#### 1. Leads Finder (code_crafter) - Apollo Alternative
**URL:** https://apify.com/code_crafter/leads-finder

- **Price:** $1.5 per 1,000 leads
- **Rating:** 4.3/5 (217 reviews)
- **Uses:** 16K+
- **Features:**
  - Business email, mobile number, personal email
  - LinkedIn profiles, company details
  - Filters: job title, location, industry, tech stack, revenue, funding
  - Export to JSON/CSV/XLSX
- **Limitations:** Free plan caps at 100 leads/run

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 7/10 |
| **Cost** | ~$1.50/1k leads |
| **Build Time** | 30 mins to configure |
| **Pros** | Ready-made, cheap, good filtering |
| **Cons** | Third-party data (not Apollo directly), may have data gaps |

#### 2. Apollo Scraper (scrapefull)
**URL:** https://apify.com/scrapefull/apollo-scraper

- **Method:** Scrapes Apollo.io directly using your account credentials
- **Features:**
  - Bypasses Apollo export limits
  - Gets 10k emails/month or 120k/year regardless of plan
  - Full data: emails, phone numbers, job titles
  - Multiple export formats

**Best Practices from scrapefull:**
- Set delay: 2-50 seconds between requests
- Limit: 1,000 records/day max
- Use residential proxy from same country as login
- Cookie-based auth preferred over login credentials
- Don't run multiple instances simultaneously
- Monitor email credits

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 6/10 |
| **Cost** | Apify compute costs (~$25-50/mo for regular use) |
| **Build Time** | 1 hour |
| **Pros** | Bypasses export limits, uses your Apollo data |
| **Cons** | **HIGH RISK of account ban**, ToS violation, requires careful rate limiting |

#### 3. Other Leads Scrapers
- **Leads Generator (microworlds):** $3/1k, 2.6/5 rating - less reliable
- **Leads Scraper (peakydev):** $1/1k, 2.6/5 rating - 70-90% email rate claimed

---

## Option 3: Browser Automation (Playwright/Puppeteer)

### Existing GitHub Projects

#### 1. apollo-search-scraper (maximo3k)
**URL:** https://github.com/maximo3k/apollo-search-scraper
- **Stars:** 10
- **Language:** Python
- **Features:**
  - Search list scraping with CSV export
  - Config-based (login credentials, search URL, output file)
  - Works best with paid Apollo plan
  
**Limitations:** Free accounts may only see 5 pages of results

#### 2. apollo-web-scraper (itsmikepowers)
**URL:** https://github.com/itsmikepowers/apollo-web-scraper
- **Stars:** 14
- **Language:** JavaScript (Puppeteer)
- **Features:** Basic Apollo webscraping

### Custom Automation Script Approach
```javascript
// Conceptual Playwright script
1. Login to Apollo with cookies (safer than credentials)
2. Navigate to company search with filters
3. Check result count
4. If >10k: Auto-generate employee count slices
   - 1-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+
5. For each slice:
   - Navigate to filtered search
   - Click export button
   - Wait for export to complete
   - Download CSV
6. Combine all CSVs
7. Auto-upload to Clay
```

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 7/10 |
| **Cost** | Free (self-hosted) or ~$20-50/mo (cloud VM) |
| **Build Time** | 3-5 days for robust solution |
| **Pros** | Full control, free, can run overnight |
| **Cons** | Fragile (UI changes break it), ToS risk, requires maintenance |

---

## Option 4: Clay Direct Integration

### Apollo.io Integration in Clay
Clay has a **native Apollo.io integration** with these actions:

**Available Actions:**
- Enrich Company with Apollo.io
- Enrich Person with Apollo.io
- Find People at Company by Job Title
- Find People with Apollo.io
- Find Open Jobs with Apollo.io
- Find Account by ID
- Find Contact by ID
- Find Saved Contacts
- Add contact to sequence
- Update contact

### Key Insight
**Clay can pull company/people data FROM Apollo using your API key** - this potentially eliminates the export-download-upload cycle entirely!

**Workflow:**
1. Start with a seed list in Clay (company names, domains, or criteria)
2. Use "Find People at Company" or company enrichment
3. Clay calls Apollo API directly and populates your table

**Limitations:**
- Requires you to have an initial list to enrich
- **Cannot do bulk company SEARCH/DISCOVERY from Clay** (only enrichment of known companies)
- Credits consumed from your Apollo account

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 5/10 (for discovery use case) |
| **Cost** | Clay subscription + Apollo credits |
| **Build Time** | 30 mins |
| **Pros** | No export/import needed, native integration |
| **Cons** | Works for enrichment, NOT for discovery searches |

---

## Option 5: Alternative Company Databases

### 1. LinkedIn Sales Navigator
**Status:** ❌ NOT ACCEPTING NEW API PARTNERS

> "We are not currently accepting new partners for access to the LinkedIn Sales Navigator API. We periodically review our onboarding capacity and will update this page if availability changes."

**Assessment:** Not viable for programmatic access

### 2. Crunchbase API
**Pricing:** Enterprise license required (contact sales)
**Features:**
- Company search and enrichment
- Funding data, investors, acquisitions
- 200 calls/minute rate limit
- Full company database access

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 6/10 |
| **Cost** | $$$ (Enterprise pricing, typically $10k+/year) |
| **Build Time** | 2-3 days |
| **Pros** | Excellent funding/investor data, official API |
| **Cons** | Expensive, requires sales process, different data focus |

### 3. People Data Labs
**Features:**
- Company Enrichment API
- Bulk enrichment available
- Person + Company data

**Pricing:** Usage-based, typically cheaper than Apollo
**Best for:** Enrichment of existing lists, not discovery

**Assessment:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 7/10 |
| **Cost** | $$ (usage-based, competitive) |
| **Build Time** | 1-2 days |
| **Pros** | Good API, bulk enrichment, cheaper |
| **Cons** | Different data coverage than Apollo |

### 4. ZoomInfo
**Status:** Enterprise-only, pricing not publicly available
- Requires sales call
- Typically $15k-50k+/year
- Has API access

**Assessment:** Too expensive for most use cases

---

## Option 6: RPA/Workflow Tools

### Zapier
**Apollo Integration:** ✅ Available
- Triggers: New Contact
- Actions: Create Account, Create Contact, Create Opportunity, Create Task, Create Note
- **NOT suitable for bulk search/export** - designed for record-by-record automation

### Make.com (Integromat)
**Apollo Integration:** Blocked by Cloudflare during research
- Likely similar to Zapier - record-level automation, not bulk export

### n8n
**Apollo Integration:** ❌ Not found in integrations
- Could build custom HTTP request nodes to call Apollo API

**Assessment for RPA tools:**
| Criterion | Rating |
|-----------|--------|
| **Feasibility** | 3/10 (for bulk export) |
| **Cost** | $20-100/mo |
| **Build Time** | 2-4 hours |
| **Pros** | No code, good for triggers/workflows |
| **Cons** | Not designed for bulk data extraction |

---

## Recommendations Summary

### 🏆 BEST OPTIONS (Ranked)

#### 1. Apollo API + Custom Python Script (RECOMMENDED)
**Feasibility: 8/10 | Cost: Low | Build: 1-2 days**

Build a Python script that:
- Uses Apollo Organization Search API
- Auto-slices by employee count when >50k results
- Paginates through all results
- Exports to CSV or pushes directly to Clay via HTTP API
- Runs overnight with proper rate limiting

**Why:** Official, safe, reliable, full control.

#### 2. Apify Leads Finder (Quick Alternative)
**Feasibility: 7/10 | Cost: $1.5/1k leads | Build: 30 mins**

If Apollo data coverage is similar, this is the fastest solution.

**Why:** Ready-made, cheap, no development needed.

#### 3. Custom Playwright Automation
**Feasibility: 7/10 | Cost: Free/Low | Build: 3-5 days**

Fork one of the GitHub scrapers and enhance it with:
- Cookie-based authentication
- Auto-slicing logic for >10k results
- Overnight scheduling
- Error recovery

**Why:** Full control, free, but higher maintenance.

### ⚠️ AVOID
- Apify Apollo scrapers that login to your account (ToS risk, ban risk)
- LinkedIn Sales Navigator API (not accepting partners)
- ZoomInfo (too expensive)
- Zapier/Make for bulk export (wrong tool for job)

---

## Implementation Recommendation

### Phase 1: Quick Win (This Week)
Try the **Apify Leads Finder** for a test batch to validate data quality matches your needs.

### Phase 2: Production Solution (2 Weeks)
Build a **Python script using Apollo API** with:
1. Organization Search endpoint
2. Auto-slicing by employee count ranges
3. Pagination handler (100 records/page, up to 500 pages per slice)
4. CSV export + direct Clay HTTP API integration
5. Scheduling via cron for overnight runs
6. Error handling and resume capability

### Estimated Time Savings
- **Before:** 1-2 days manual work
- **After:** ~30 minutes setup + overnight automation
- **ROI:** ~90% time reduction

---

## Resources & Links

- Apollo API Docs: https://docs.apollo.io/
- Apollo Organization Search: https://docs.apollo.io/reference/organization-search
- Apollo API Pricing: https://docs.apollo.io/docs/api-pricing
- Apify Leads Finder: https://apify.com/code_crafter/leads-finder
- GitHub apollo-search-scraper: https://github.com/maximo3k/apollo-search-scraper
- Clay Apollo Integration: https://www.clay.com/integrations/data-provider/apollo-io
- People Data Labs: https://docs.peopledatalabs.com/docs/company-enrichment-api
- Crunchbase API: https://data.crunchbase.com/docs/using-the-api
