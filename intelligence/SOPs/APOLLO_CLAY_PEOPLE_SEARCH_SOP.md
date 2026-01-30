# Apollo + Clay People Search SOP

> **Source:** [Loom Video - Automating Lead Generation for MedVirtual Private Practices](https://www.loom.com/share/12ac35e15dd64c308877cf91a7c70031)  
> **Presenter:** Liam Sheridan  
> **Duration:** ~5:40  
> **Last Updated:** 2026-01-27

---

## Overview / Purpose

This SOP documents the process of finding and validating people/contacts from a Clay table that has already been populated with companies from an Apollo search. The goal is to:

1. Find relevant contacts at target companies
2. Retrieve their work emails
3. Validate email deliverability
4. Handle catchall domains
5. Export clean, validated leads for outbound sequences

---

## Prerequisites

Before starting this process, ensure you have:

- [ ] **Apollo export** of target accounts (companies) already loaded
- [ ] **Clay account** with active credits
- [ ] **ICPs integration** configured in Clay (for email finding)
- [ ] **MillionVerifier API key** configured as HTTP API template
- [ ] **Bounceback API key** configured as HTTP API template
- [ ] Target **job titles** defined for your ICP
- [ ] Target **location(s)** defined (e.g., United States)

---

## Step-by-Step Instructions

### Phase 1: Import People from Companies

#### Step 1.1: Access Your Company Table
Navigate to your Clay table containing the Apollo company export.

> **Screenshot context:** Screen shows a Clay table with 10,000 rows of company accounts for MedVirtual private practices, exported from Apollo.

#### Step 1.2: Find People at Companies
1. Click **Sources** in the Clay menu
2. Select **"Find people at these companies"**

> **Screenshot context:** Clay sources panel showing "Find people at these companies" option.

#### Step 1.3: Configure Search Filters

**Job Title Filter:**
- Enter the job titles from your ICP search
- This returns contacts matching those specific roles

> **Example:** Liam's search returned ~21,000 results with specified job titles.

**Location Filter:**
- Set to **United States** (or your target geography)
- This ensures contacts are in your target market

> **Note from Liam:** "Just to make sure. We've already done our company search in terms of the sizing, so everything should already be targeted there."

#### Step 1.4: Import to New Table
1. Click **"Import to a new table"**
2. This creates a new table with all matching contacts

> **Screenshot context:** New table populated with contact names, companies, and basic info.

---

### Phase 2: Configure Contact Columns

#### Step 2.1: Add Essential Columns
Add the following columns to your contact table:

| Column | Purpose |
|--------|---------|
| Website | Company domain for email finding |
| Industry | Validate company fit (⚠️ check accuracy) |
| Employees | Validate company size |
| Company Name | Reference |
| Short Description | For Clay AI use cases |
| First Name | Personalization |
| Last Name | Personalization |
| Full Name | Email finding input |
| Job Title | ICP validation |
| Location | Geographic targeting |
| Domain | Company domain |
| LinkedIn Profile | Research/outreach |

> **⚠️ Liam's Warning:** "Airlines, aviation is obviously wrong... These don't look like private practices to me, financial services, management consulting."

---

### Phase 3: Find Work Emails

#### Step 3.1: Configure ICPs Integration
1. Navigate to your **ICPs** integration in Clay
2. This integration uses **Full Name + Website** to find work emails
3. Configure to **return the email** field

#### Step 3.2: Run Email Finding
1. Select **"Run on X rows"** (test on 10 rows first)
2. Wait for the API queue to process
3. ICPs will populate the email column

> **Screenshot context:** ICPs queue processing, showing "This is going to queue. And then you have to wait for the API response from ICPs where I have credits loaded."

**Example Result:** `adam@rb2b.com`

> **💡 Tip from Liam:** Always test on a small batch (10 rows) before running on the full dataset.

---

### Phase 4: Email Validation with MillionVerifier

#### Step 4.1: Configure MillionVerifier HTTP API
This should be pre-configured as an HTTP API request template in Clay with:
- Your MillionVerifier API key
- Input: Email column
- Condition: **Only run if email is not empty**

#### Step 4.2: Run Validation
1. Apply the MillionVerifier template
2. Run on your rows
3. Results populate in a new column

#### Step 4.3: Interpret Results

| Result | Meaning | Action |
|--------|---------|--------|
| **OK** | Email is valid and deliverable | ✅ Ready to send |
| **Catchall** | Domain accepts all emails | ⚠️ Needs Bounceback validation |
| **Invalid** | Email doesn't exist | ❌ Remove from list |

---

### Phase 5: Catchall Handling with Bounceback

#### Step 5.1: Configure Bounceback HTTP API
Pre-configure as HTTP API request with:
- Your Bounceback API key
- GET request on email field
- **Condition: Only run if MillionVerifier result = "catchall"**

> **Screenshot context:** Bounceback template showing "GET from there on the email using our API key. And it would only do it if it is catchall as a result."

#### Step 5.2: Run Bounceback on Catchalls
1. Apply the Bounceback template
2. Only processes rows where validation returned "catchall"
3. Non-catchall rows show "run condition not met" (expected)

#### Step 5.3: Final Email Qualification

An email is **safe to send** when:
- MillionVerifier returns **"OK"**, OR
- MillionVerifier returns **"Catchall"** AND Bounceback returns **"Deliverable"**

---

### Phase 6: Export and Load to Sequence

#### Step 6.1: Filter Qualified Leads
Create a view or filter for:
- Valid emails only (OK or deliverable catchalls)
- Verified industry/company fit

#### Step 6.2: Export Data
Export the qualified contacts for your outbound sequence.

---

## Critical Notes & Warnings

### ⚠️ Lead Accuracy Validation (IMPORTANT)

> **Liam's Critical Observation:** "I need to validate the fact that these are accurate leads. Because what we're looking at here is from table one, private practices. And these don't look like private practices to me, financial services, management consulting. So this is an issue that I'm now using credits for getting leads that aren't even targeted."

**Recommended Actions:**
1. **Spot-check industries** before running expensive API calls
2. **Use AI validation** in Clay to verify company fit before email finding
3. **Review Apollo search criteria** if many results are off-target
4. **Add industry filters** when importing to new table

### 💰 Credit Management

- Email finding (ICPs) costs credits per lookup
- Validation (MillionVerifier, Bounceback) costs per API call
- **Always test on 10 rows first** before full runs
- Don't waste credits on unvalidated/off-target companies

### 🔄 Process Optimization Ideas (from Liam)

- "We can validate them with AI later and do some validation"
- Consider adding AI classification step **before** email finding
- Filter out obviously wrong industries at the company level

---

## Summary Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  APOLLO COMPANY EXPORT                                       │
│  (10,000 accounts already in Clay)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  FIND PEOPLE AT COMPANIES                                    │
│  • Filter by Job Titles (from ICP)                          │
│  • Filter by Location (United States)                       │
│  • Import to new table                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  ⚠️ VALIDATE LEAD ACCURACY                                   │
│  • Check industries match target                            │
│  • Verify company sizes                                     │
│  • Remove off-target contacts                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  FIND WORK EMAILS (ICPs)                                     │
│  • Input: Full Name + Website                               │
│  • Test on 10 rows first                                    │
│  • Run on validated contacts only                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  VALIDATE EMAILS (MillionVerifier)                          │
│  • Only run if email is not empty                           │
│  • Results: OK / Catchall / Invalid                         │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌───────────────┐       ┌───────────────┐
        │  OK = ✅ SEND  │       │   CATCHALL    │
        └───────────────┘       └───────┬───────┘
                                        │
                                        ▼
                                ┌───────────────┐
                                │  BOUNCEBACK   │
                                │  Validation   │
                                └───────┬───────┘
                                        │
                        ┌───────────────┴───────────────┐
                        │                               │
                        ▼                               ▼
                ┌───────────────┐               ┌───────────────┐
                │ Deliverable   │               │ Not           │
                │ = ✅ SEND     │               │ Deliverable   │
                └───────────────┘               │ = ❌ SKIP     │
                                                └───────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  EXPORT TO SEQUENCE                                          │
│  • Only qualified emails                                    │
│  • Ready for outbound                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Video Chapter Reference

| Timestamp | Topic |
|-----------|-------|
| 0:00 | Process Automation Overview |
| 2:00 | Email Retrieval Process |
| 3:56 | Email Validation Steps |
| 5:18 | Lead Accuracy Concerns |

---

## Related Resources

- [MillionVerifier Documentation](https://www.millionverifier.com/)
- [Bounceback Documentation](https://usebounceback.com/)
- [Clay Documentation](https://www.clay.com/docs)
- [Apollo Documentation](https://www.apollo.io/docs)
