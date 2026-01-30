# Clay Regex Business Classification

**Purpose:** Classify companies using regex BEFORE burning AI credits
**Source:** [Mitchell Keller thread](https://x.com/mitchellkeller_/status/2016553205291798882)

---

## Implementation

Add these as Clay columns that run regex against scraped homepage text.
Run BEFORE any AI enrichment to save credits.

### Column 1: `business_type_regex`

**Input:** Homepage HTML/text (nav, footer, link text — main content is too noisy)

**Logic:**
```python
def classify_business(text):
    text = text.lower()
    
    # SaaS indicators
    saas_patterns = [
        r'free\s+trial',
        r'\bapi\b',
        r'\bintegrations?\b',
        r'per\s+month',
        r'\bdashboard\b',
        r'\bworkflow\b',
        r'\bplatform\b',
        r'\bsubscription\b',
        r'start\s+free',
        r'api[\s._-]?docs?',
        r'\bdeveloper[s]?\b',
        r'\bsdk\b'
    ]
    
    # Agency/Services indicators
    agency_patterns = [
        r'our\s+services',
        r'\bportfolio\b',
        r'get\s+a?\s*quote',
        r'\bconsulting\b',
        r'\bagency\b',
        r'our\s+work',
        r'\/services\b',
        r'\/our-services'
    ]
    
    # E-commerce indicators
    ecomm_patterns = [
        r'add\s+to\s+cart',
        r'\bcheckout\b',
        r'free\s+shipping',
        r'buy\s+now',
        r'\bin\s+stock\b',
        r'\bshopping\s+cart\b'
    ]
    
    # Local business indicators
    local_patterns = [
        r'visit\s+us',
        r'store\s+hours?',
        r'\bdirections?\b',
        r'\(\d{3}\)\s*\d{3}[-\s]?\d{4}',  # Phone number format
        r'\bmon(?:day)?\s*(?:-|through|to)\s*fri(?:day)?\b',
        r'walk[\s-]?ins?\s+welcome'
    ]
    
    # Count matches
    saas_score = sum(1 for p in saas_patterns if re.search(p, text))
    agency_score = sum(1 for p in agency_patterns if re.search(p, text))
    ecomm_score = sum(1 for p in ecomm_patterns if re.search(p, text))
    local_score = sum(1 for p in local_patterns if re.search(p, text))
    
    # Return highest
    scores = {
        'SaaS': saas_score,
        'Agency/Services': agency_score,
        'E-commerce': ecomm_score,
        'Local Business': local_score
    }
    
    max_type = max(scores, key=scores.get)
    if scores[max_type] >= 2:
        return max_type
    return 'Unknown'
```

**Output:** `SaaS` | `Agency/Services` | `E-commerce` | `Local Business` | `Unknown`

---

### Column 2: `research_links`

**Input:** All links from homepage scrape

**Logic:**
```python
def extract_research_links(links):
    patterns = {
        'careers': r'/careers?|/jobs?|/hiring|/join-us|/open-positions',
        'case_studies': r'/case-stud|/testimonial|/success-stor|/customers?|/reviews?',
        'pricing': r'/pricing|/plans|/packages',
        'docs': r'/docs?|/documentation|/api|/developer|/integrations?',
        'competitors': r'/compare|/vs|/alternatives?'
    }
    
    found = {}
    for link in links:
        for category, pattern in patterns.items():
            if re.search(pattern, link, re.I):
                found[category] = link
                break
    
    return found
```

**Output:** JSON with categorized links
```json
{
  "careers": "https://example.com/careers",
  "case_studies": "https://example.com/customers",
  "pricing": "https://example.com/pricing"
}
```

---

### Column 3: `website_alive`

**Input:** Company domain

**Logic:**
```python
def check_website(domain):
    try:
        resp = requests.head(f"https://{domain}", timeout=5, allow_redirects=True)
        if resp.status_code == 200:
            return "alive"
        elif resp.status_code == 404:
            return "404"
        elif resp.status_code >= 500:
            return "server_error"
        else:
            return f"status_{resp.status_code}"
    except:
        return "unreachable"
```

**Output:** `alive` | `404` | `server_error` | `unreachable`

---

## Clay Implementation

1. **Scrape Homepage** (existing Clay action)
2. **Add Formula Column** for `business_type_regex`
3. **Add Formula Column** for `research_links`
4. **Add HTTP Column** for `website_alive`
5. **Filter:** Skip leads where `website_alive` != `alive`
6. **Then** run AI enrichment only on filtered, classified leads

---

## Expected Savings

- 80% of companies classifiable without AI
- Skip 404/unreachable domains before enrichment
- Send AI directly to `/careers` instead of asking it to "find hiring info"

---

## Usage per Client

| Client | Focus `business_type` | Skip if |
|--------|----------------------|---------|
| CGS (UX) | SaaS, Agency | Local Business |
| Paralect (Dev) | SaaS | Local Business, E-commerce |
| LawTech | Agency/Services | E-commerce |
| Hygraph | SaaS | Local Business |
