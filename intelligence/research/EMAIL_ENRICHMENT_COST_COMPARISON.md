# Email Finding & Enrichment Cost Comparison

*Last Updated: January 2026*

## Executive Summary

This document compares the costs of different approaches to email enrichment and validation for B2B lead generation:

1. **Current Stack** (ICYPEAS → Lead Magic → Million Verifier → Bounceback)
2. **Alternative: Prospeo** (all-in-one premium solution)
3. **In-House LinkedIn Scraping** + email finding

**Key Finding:** You **cannot** scrape emails directly from LinkedIn - emails are not displayed on profiles. Any LinkedIn scraping approach still requires an email finding service on top.

---

## Tool-by-Tool Pricing Analysis

### 1. ICYPEAS (Email Finding)
**Website:** icypeas.com

**Pricing Model:** Credit-based, pay-as-you-go style
- Credits never expire
- Credits roll over (no cap on stacking)
- Claims to be "3-10x cheaper" than Wiza, Findymail, Dropcontact

**Estimated Pricing (based on market positioning):**
| Credits | Estimated Cost | Cost/1,000 |
|---------|---------------|------------|
| 5,000 | ~$25-40 | $5-8 |
| 25,000 | ~$100-150 | $4-6 |
| 100,000 | ~$300-500 | $3-5 |

**What's Included:**
- Email finding (primary feature)
- Email verification included
- Domain scanning
- GDPR compliant (no database, uses algorithms)
- Lowest bounce rate claims

**Quality Claims:**
- Lowest bounce rate on market
- High find rate (comparable to Wiza, Findymail, Dropcontact)

---

### 2. Lead Magic (Waterfall Email Finding)
**Website:** leadmagic.io

**Pricing Tiers:**

| Plan | Credits/Month | Monthly Cost | Cost/Credit | Cost/1,000 Emails |
|------|--------------|--------------|-------------|-------------------|
| Basic | 2,500 | $59.99 | $0.024 | $24.00 |
| Essential | 10,000 | $99.99 | $0.010 | $10.00 |
| Growth | 20,000 | $179.99 | $0.009 | $9.00 |
| Advanced | 30,000 | $259.99 | $0.0087 | $8.70 |
| Professional | 50,000 | $424.99 | $0.0085 | $8.50 |
| Ultimate | 100,000 | $799.99 | $0.0080 | $8.00 |

**Credit Usage:**
- 1 credit = 1 valid email (catch-all emails are FREE - no charge)
- 1 credit = 20 email validations (catch-all verification included)
- 5 credits = 1 valid mobile number (waterfall enrichment)
- 1 credit = 1 profile search
- 1 credit = 1 company search

**What's Included:**
- Email addresses
- Direct mobile numbers
- B2B profile enrichment
- B2B company enrichment
- Job posting alerts
- Full API access

**Key Advantage:** No charge for catch-all emails - only pay for valid deliverable emails.

---

### 3. Million Verifier (Email Validation)
**Website:** millionverifier.com

**Pricing Model:** Pay only for GOOD and BAD results
- **Unknown emails: FREE**
- **Catch-all emails: FREE** (unique in the market)
- Auto top-up gives 10% extra credits
- Every 5M purchased = 1M free ("Ever Green Promotion")
- 100% money-back guarantee if >4% hard bounce rate

**Estimated Pricing:**

| Emails | Estimated Cost | Cost/1,000 |
|--------|---------------|------------|
| 10,000 | ~$4-8 | $0.40-0.80 |
| 100,000 | ~$30-50 | $0.30-0.50 |
| 500,000 | ~$100-150 | $0.20-0.30 |
| 1,000,000 | ~$150-200 | $0.15-0.20 |

**What's Included:**
- Email list verification
- Bulk email verifier
- Email verifier API
- EverClean automatic verification
- Real-time verification

**Quality Claims:**
- 99%+ accuracy rate
- Best prices on market
- Only verifier not charging for catch-all

---

### 4. Bounceback (Catchall Validation)
**Website:** getbounceback.com

**Purpose:** Specialized catch-all email validation
- Validates whether catch-all emails are actually deliverable
- Complements standard email verification

**Pricing:** ⚠️ Unable to retrieve current pricing
- Likely credit-based model
- Estimated $0.01-0.03 per catch-all validation based on market comparisons

**What's Included:**
- Catch-all domain detection
- Risky email identification
- Deliverability prediction for catch-all addresses

---

### 5. Prospeo (Premium Alternative)
**Website:** prospeo.io

**Provided Pricing:**
- **$5,744/year for 530,000 credits**
- Cost per credit: **$0.0108**
- Cost per 1,000 leads: **$10.84**

**What's Included (All-in-One):**
- B2B lead database with 30+ filters
- Verified email finding
- Mobile number finding
- Chrome extension
- API access
- Real-time data synced with LinkedIn
- Email validation included
- Job change detection
- Intent signals

**Quality Claims:**
- "Bounce rate dropped by over 70%" (customer testimonial)
- Pre-validated emails (no separate verification needed)
- Premium LinkedIn-synced data

**Note:** Prospeo recently launched V2 - a complete rebuild with direct lead list building inside platform.

---

## In-House LinkedIn Scraping Analysis

### Can You Scrape Emails from LinkedIn?

**NO.** LinkedIn does not display email addresses on public profiles.

**What you CAN scrape from LinkedIn:**
- Full name
- Job title/headline
- Company name
- Location
- Work history
- Education
- Skills
- Profile URL
- Company LinkedIn URL
- Company size/industry

**What you CANNOT get from LinkedIn:**
- Email addresses (never displayed)
- Phone numbers (rarely displayed)
- Personal email
- Direct contact info

### LinkedIn Scraping Tools Pricing

#### Apify

**Platform Pricing:**

| Plan | Monthly | Compute Units | RAM | Concurrent Runs |
|------|---------|--------------|-----|-----------------|
| Free | $5/mo | $0.30/CU | 8GB | 25 |
| Starter | $29/mo | $0.30/CU | 32GB | 32 |
| Scale | $199/mo | $0.25/CU | 128GB | 128 |
| Business | $999/mo | $0.20/CU | 256GB | 256 |

**Residential Proxies:** $7-8/GB

**LinkedIn Profile Scraper (Dev Fusion):**
- No LinkedIn cookies required
- Free plan: 10 runs/day, max 10 profiles/run
- Paid: Up to 10M runs/day
- Includes email discovery attempt (separate service)
- Mobile number lookup (paying users only)

**Estimated Cost per 1,000 LinkedIn Profiles:**
- Compute: ~$1-3 (depending on scraper efficiency)
- Proxies: ~$2-5 (residential recommended for LinkedIn)
- **Total scraping only: ~$3-8 per 1,000 profiles**

#### Phantombuster

**Pricing:** Unable to retrieve current pricing (JavaScript-heavy site)

**Typical Market Position:**
- Estimated $50-150/month for starter plans
- Per-profile costs vary by automation

#### Bright Data (Proxy Provider)

**Residential Proxies:**
| Plan | GB Included | Price/GB | Monthly Cost |
|------|-------------|----------|--------------|
| Pay As You Go | - | $8.00 | Variable |
| 141 GB | 141 | $3.50 | $499 |
| 332 GB | 332 | $3.00 | $999 |
| 798 GB | 798 | $2.50 | $1,999 |

*50% discount currently available with code RESIGB50*

#### Decodo/Smartproxy (Proxy Provider)

**Residential Proxies:**
| GB | Price/GB | Monthly Cost |
|----|----------|--------------|
| 2 | $3.00 | $6 |
| 25 | $2.60 | $65 |
| 100 | $2.25 | $225 |
| 500 | $1.75 | $875 |

### In-House LinkedIn Scraping + Email Finding

**Total Cost Breakdown:**

1. **LinkedIn Scraping:**
   - Apify/similar: $3-8 per 1,000 profiles
   - Proxies: $2-5 per 1,000 profiles
   
2. **Email Finding Still Required:**
   - You get: name, company, title from LinkedIn
   - You still need: email finding service
   - Additional cost: $5-15 per 1,000 leads

3. **Email Validation:**
   - Standard validation: $0.30-0.50 per 1,000
   - Catch-all validation: $10-30 per 1,000

**Total In-House Approach: ~$15-35 per 1,000 leads** (more expensive AND more complex than using existing tools)

---

## Cost Calculations for 100,000 Leads

### Option 1: Current Stack (ICYPEAS → Lead Magic → Million Verifier → Bounceback)

Assuming waterfall approach where:
- ICYPEAS finds ~70% of emails
- Lead Magic catches remaining ~20%
- ~10% unfound

| Step | Volume | Cost/1,000 | Total Cost |
|------|--------|------------|------------|
| ICYPEAS (primary) | 100,000 | $4.00 | $400 |
| Lead Magic (waterfall) | 30,000 | $8.00 | $240 |
| Million Verifier (all found) | 90,000 | $0.30 | $27 |
| Bounceback (catch-all ~30%) | 27,000 | $15.00* | $405 |

**Total: ~$1,072 for 100k leads**
**Cost per 1,000 leads: ~$10.72**

*Bounceback estimate based on comparable services

### Option 2: Prospeo

| Volume | Cost |
|--------|------|
| 100,000 leads | 100,000 credits |

Annual plan: $5,744/year for 530,000 credits
- 100k leads = 18.9% of annual allocation
- Prorated cost: **~$1,085**

**Cost per 1,000 leads: $10.84**

*Note: Prospeo credits may require 1+ credit per lead depending on operations*

### Option 3: In-House LinkedIn Scraping + Email Finding

| Step | Volume | Cost/1,000 | Total Cost |
|------|--------|------------|------------|
| LinkedIn scraping (Apify) | 100,000 | $5.00 | $500 |
| Residential proxies | ~50GB | $3.00/GB | $150 |
| Email finding (still needed) | 100,000 | $8.00 | $800 |
| Email validation | 100,000 | $0.30 | $30 |
| Catch-all validation | 30,000 | $15.00 | $450 |

**Total: ~$1,930 for 100k leads**
**Cost per 1,000 leads: ~$19.30**

---

## Comparison Summary Table

| Approach | Cost/1,000 Leads | 100k Lead Cost | Complexity | Data Quality |
|----------|------------------|----------------|------------|--------------|
| **Current Stack** (ICYPEAS + Lead Magic + MV + Bounceback) | **$10.72** | **$1,072** | Medium | High (waterfall) |
| **Prospeo** (all-in-one) | **$10.84** | **$1,085** | Low | High (LinkedIn-synced) |
| **In-House LinkedIn** + email finding | **$19.30** | **$1,930** | High | Variable |

---

## Key Insights & Recommendations

### 1. LinkedIn Scraping Reality Check
**You cannot get emails from LinkedIn.** Period. Any in-house scraping approach still requires:
- An email finding service (using company domain + name patterns)
- Email validation
- The scraped data only gives you the inputs for email finding

### 2. Current Stack vs Prospeo
- Costs are nearly identical (~$10.72 vs $10.84 per 1,000)
- Current stack offers more control and waterfall redundancy
- Prospeo offers simplicity and LinkedIn-synced freshness
- **Recommendation:** Stick with current stack unless Prospeo's data freshness provides measurably better results

### 3. In-House Approach is NOT Cost-Effective
- ~80% more expensive ($19.30 vs $10.72)
- Much higher complexity (multiple tools, proxies, maintenance)
- Risk of LinkedIn account bans
- Still requires email finding service anyway
- **Not recommended** unless you need specific LinkedIn data not available through other tools

### 4. Key Cost Drivers
- **Email finding** is the biggest cost component
- **Catch-all validation** adds significant cost (~30% of leads are catch-all)
- **Lead Magic's free catch-all policy** is valuable - no charge for catch-all on initial find

### 5. Optimization Opportunities
- Negotiate volume pricing with current vendors
- Reduce catch-all validation to only essential campaigns
- Consider Prospeo for simpler workflows if current stack becomes unwieldy
- Monitor email find rates - if ICYPEAS find rate is lower than expected, Lead Magic waterfall costs increase

---

## Appendix: Other Tools Reference

### Email Verification Services

| Service | Cost/1,000 | Notes |
|---------|------------|-------|
| DeBounce | $0.30-1.50 | Catch-all validation 10 credits each |
| Emailable | $0.50-2.00 | Volume discounts, credits never expire |
| EmailListVerify | $0.30-1.00 | 97% accuracy claim |

### Email Finding Services

| Service | Cost/1,000 | Notes |
|---------|------------|-------|
| Wiza | $150/1,000 | LinkedIn Sales Nav focused, unlimited on annual plans |
| Dropcontact | Variable | GDPR compliant, V2 has waterfall enrichment |
| Apollo.io | Free-$99/mo | Includes database access, limited credits |
| Evaboot | $9-499/mo | Sales Nav extractor, credits from 50-5000+ |

---

*Document prepared for lead generation cost optimization analysis.*
