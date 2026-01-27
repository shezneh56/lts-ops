# Spam Analysis - All Clients
**Date:** 2026-01-27
**Analyst:** Automated spam word scan + step-level stats review

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Total clients analyzed | 6 |
| Total active campaigns reviewed | 47 |
| Steps with 0 replies (>100 sent) | 14 |
| Critical spam word issues | **0** |
| MS inbox deliverability issues | **HIGH** |

### Key Finding
**NO % symbols detected** in any active campaign copy. All clients are correctly using "percent" spelled out. The primary issue is **Microsoft inbox deliverability** rather than spam word content.

---

## Client Analysis

### 1. C2 Experience

**Status:** ✅ Clean - No spam word issues

**Active/Paused Campaigns with data:**
- Campaign 432: C2 Group - Tech - C-Suite (728 sent, 12 replies) - 1.6% reply rate
- Campaign 434: C2 Group - Tech - Non C-Suite (2190 sent, 39 replies) - 1.8% reply rate
- Campaign 433: C2 Group - Tech - VPs (168 sent, 4 replies) - 2.4% reply rate
- Campaign 436: C2 Group - Marketing - VPs (198 sent, 6 replies) - 3.0% reply rate

**Flagged Campaign:**
- **Campaign 245: CIO/CTO - Sitecore - USA - MS** (44 sent, **0 replies**) - PAUSED
  - Steps 1496-1499: ALL have 0 replies (8-12 sends each)
  - Copy reviewed: Clean, no spam words
  - **Root cause:** MS inbox targeting, low sample size

**Copy Review:**
- ✅ Uses "percent" spelled out
- ✅ No urgency words
- ⚠️ Uses "significant" claims without specifics
- ⚠️ "We've helped numerous clients" - vague

**Severity:** LOW - Low volume, copy is clean

---

### 2. CGS Team

**Status:** ⚠️ Moderate - MS inbox campaigns underperforming

**High-Performing Campaigns (Google inbox):**
- Campaign 300: CyberSecurity - US - Google (13,099 sent, 113 replies) - **1.71% reply rate**
- Campaign 303: CyberSecurity - EMEA - Google (7,913 sent, 112 replies) - 1.42% reply rate
- Campaign 707: Crunchbase MVP - USA SaaS (5,072 sent, 32 replies) - 0.63% reply rate

**Underperforming Campaigns (MS inbox):**
- **Campaign 301: CyberSecurity - US - MS** (10,087 sent, 8 replies) - **0.08% reply rate** ⚠️
  - Step 1953: 719 sent, 0 replies
  - Step 1956: 759 sent, 0 replies  
  - Step 1958: 1,640 sent, 0 replies
  - Step 1959: 1,668 sent, 0 replies
  - Step 1963: 709 sent, 0 replies

- **Campaign 304: CyberSecurity - EMEA - MS** (8,861 sent, 10 replies) - 0.11% reply rate

**Copy Analysis - Campaign 301 (0 replies steps):**
```
Step 1953: "{FIRST_NAME}, are you the right person to talk to about 
implementing AI for {COMPANY}? We recently helped Cydome, reduce 
overhead by 78k/year by implementing our AI agent."
```

**Spam triggers found:**
- ✅ "percent" used correctly (not %)
- ⚠️ "78k/year" - monetary claim (acceptable)
- ⚠️ "65 percent reduction" - specific claim (borderline)
- ⚠️ "If we don't deliver more value than our project fee, we return the difference" - guarantee language
- ✅ No urgency words

**Diagnosis:** The copy is CLEAN. Issue is MS inbox deliverability, not spam content.

**Severity:** MEDIUM - Same copy works on Google (1.71%) but fails on MS (0.08%)

---

### 3. LawTech

**Status:** ✅ Excellent - Highest performing client

**Active Campaigns:**
- **Campaign 140: USA - GC/Legal Ops** (74,834 sent, 820 replies) - **1.1% reply rate** ✅
- **Campaign 173: EU - GC/Legal Ops** (14,101 sent, 275 replies) - **1.95% reply rate** ✅

**Copy Analysis:**
```
Step 573: "{FIRST_NAME}, getting flooded with LawTech vendor emails 
lately? We help in-house teams make sense of what's actually out 
there – what's working (and what's not!)."
```

**Spam word check:**
- ✅ No % symbols
- ✅ No monetary claims in opening
- ✅ Conversational tone
- ✅ "No pitch, no fee" - frames free as "no fee" (safer)
- ✅ Avoids urgency language

**Why it works:**
- Acknowledges pain point (vendor fatigue)
- No hard sells
- Clear value proposition
- Professional signature only

**Severity:** NONE - Model client for email copy

---

### 4. LegalSoft

**Status:** ⚠️ Moderate - Clear MS vs Google disparity

**Google Inbox Campaigns (High Performance):**
- **Campaign 312: Law Practice - Google** (6,683 sent, 191 replies) - **10.37% reply rate** ✅
- Campaign 314: Law Practice - Other (10,255 sent, 211 replies) - 5.04% reply rate

**MS Inbox Campaigns (Low Performance):**
- **Campaign 313: Law Practice - MS** (7,737 sent, 16 replies) - **0.76% reply rate** ⚠️
  - Step 2048: 424 sent, 0 replies
  - Step 2059: 431 sent, 0 replies
  - Step 2061: 423 sent, 0 replies
  - Step 2064: 672 sent, 0 replies

**Copy Analysis - Campaign 313 (0 replies steps):**
```
Step 2048: "{FIRST_NAME}, I noticed from your website you {FIRST LINE}. 
A mid-sized law firm in Chicago saved 1M annually by replacing 
in-house hires with our pre-vetted virtual staff..."
```

**Spam triggers found:**
- ✅ "percent" not used (only whole numbers)
- ⚠️ "2.5M in revenue" - large monetary claim
- ⚠️ "saved 1M annually" - large monetary claim
- ⚠️ "1,000+ cases" - scale claim
- ✅ No urgency words
- ✅ No guarantee language

**Diagnosis:** Copy is CLEAN. Same copy gets 10.37% on Google vs 0.76% on MS.

**Severity:** MEDIUM - MS deliverability issue, not spam content

---

### 5. MedVirtual

**Status:** ⏸️ Not Analyzed - All campaigns in draft

**Campaigns:**
- MV - Private Practices - US - V2 (DRAFT)
- MV - Dental Practices - US - V2 (DRAFT)
- MV - Chiropractic - US - V2 (DRAFT)
- MV - Aesthetics/MedSpa - US - V2 (DRAFT)

**Note:** No emails sent yet. Review copy before launch.

**Severity:** N/A - Pending

---

### 6. Paralect

**Status:** ⚠️ Moderate - Some underperforming steps

**Active Campaigns:**
- **Campaign 516: USA Paralect CO - Corporates** (9,369 sent, 44 replies) - 0.78% reply rate
  - Step 3301: 310 sent, 0 replies
  - Step 3302: 344 sent, 0 replies

- **Campaign 515: USA Paralect MS - Mature Startups** (3,844 sent, 23 replies) - 0.64% reply rate
  - Step 3298: 678 sent, 0 replies ⚠️
  
- Campaign 514: USA Paralect ES - Early Stage (2,411 sent, 10 replies) - 0.41% reply rate
- Campaign 309: Crunchbase USA - Founder (10,367 sent, 38 replies) - 0.37% reply rate

**Copy Analysis - Step 3298 (678 sent, 0 replies):**
```
"{FIRST_NAME}, most founders who've been burned by contractors are 
hesitant to try again. VeroSkills came to us after their previous 
team wasted 6 months and burned budget..."
```

**Spam triggers found:**
- ✅ No % symbols
- ✅ No urgency words
- ⚠️ "700K ARR" - monetary claim
- ⚠️ "raised 5.3M" - monetary claim
- ⚠️ "burned runway" in subject line - negative framing

**Potential Issue:** Subject line "Re: re: Your team is burning runway" uses negative/fear-based framing.

**Severity:** LOW-MEDIUM - Relatively clean, watch step 3298

---

## Cross-Client Pattern Analysis

### MS vs Google Inbox Performance

| Client | Google Reply Rate | MS Reply Rate | Difference |
|--------|-------------------|---------------|------------|
| CGS Team | 1.71% | 0.08% | **21x worse** |
| LegalSoft | 10.37% | 0.76% | **14x worse** |
| LawTech | N/A (mixed) | N/A | - |

**Conclusion:** Microsoft inboxes are filtering emails significantly more aggressively than Google. This is NOT a spam word issue - identical copy performs 10-20x worse on MS.

### Common Copy Patterns

**What's Working (LawTech model):**
- Conversational opener acknowledging pain
- "No pitch, no fee" framing
- Question-based subject lines
- Short, focused emails

**What's Borderline:**
- Large monetary claims (1M, 2.5M, 78k)
- Specific percentage claims (65 percent)
- Guarantee-adjacent language

**Not Found (GOOD):**
- % symbols ✅
- "Free" ✅
- "Act now" / urgency ✅
- ALL CAPS ✅
- Multiple exclamation marks ✅

---

## Priority Fixes

### Critical (None)
No critical spam word issues found.

### High Priority
1. **CGS Team - Campaign 301:** Pause MS inbox targeting, focus on Google
2. **LegalSoft - Campaign 313:** Same - pause MS inbox targeting

### Medium Priority
1. **Paralect - Step 3298:** Test removing "burned runway" from subject line
2. **Review monetary claims:** Consider softening "1M annually" → "significant annual savings"

### Low Priority
1. **C2 Experience - Campaign 245:** Low volume, monitor
2. **MedVirtual:** Review copy before launching draft campaigns

---

## Recommendations

### Immediate Actions
1. **Reduce MS inbox volume** - Until deliverability improves, focus budget on Google inboxes
2. **Warm up MS domains separately** - MS requires different warmup approach

### Copy Improvements
1. **Soften monetary claims:**
   - "1M annually" → "significant savings" or "major cost reduction"
   - "2.5M in revenue" → "multi-million in revenue" or remove specifics
   
2. **Remove guarantee language:**
   - "If we don't deliver more value than our project fee, we return the difference" → Remove or move to meeting

3. **Test LawTech copy patterns on other clients:**
   - Vendor fatigue angle
   - "No pitch, no fee" framing
   - Question-based CTAs

### Monitoring
- Track step-level reply rates weekly
- Flag any step with >200 sent and 0 replies
- A/B test MS vs Google performance monthly

---

## Appendix: Steps with 0 Replies (>100 sent)

| Client | Campaign | Step ID | Sent | Subject | Inbox Type |
|--------|----------|---------|------|---------|------------|
| CGS Team | 301 | 1953 | 719 | Question | MS |
| CGS Team | 301 | 1956 | 759 | Question | MS |
| CGS Team | 301 | 1958 | 1,640 | Re: Question | MS |
| CGS Team | 301 | 1959 | 1,668 | Re: Question | MS |
| CGS Team | 301 | 1963 | 709 | Question | MS |
| LegalSoft | 313 | 2048 | 424 | ROI Calculator | MS |
| LegalSoft | 313 | 2059 | 431 | Question | MS |
| LegalSoft | 313 | 2061 | 423 | Question | MS |
| LegalSoft | 313 | 2064 | 672 | Re: Question | MS |
| Paralect | 515 | 3298 | 678 | Contractor question | Mixed |
| Paralect | 516 | 3301 | 310 | Question | Mixed |
| Paralect | 516 | 3302 | 344 | Question | Mixed |

**Pattern:** 75% of 0-reply steps are targeting MS inboxes.

---

*Report generated automatically. Last updated: 2026-01-27*
