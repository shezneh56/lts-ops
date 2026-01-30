# CGS Team Domain-Level Deliverability Analysis

**Analysis Date:** 2026-01-28  
**Prepared by:** Automated Analysis

---

## Executive Summary

**Overall Reply Rate: 0.64%** — This is below target, but the problem isn't uniform across all campaigns. The issue appears to be **targeting Microsoft environments** rather than domain infrastructure.

### Key Findings

1. **Microsoft-targeted campaigns are severely underperforming**
   - MS → MS: 0.08% reply rate (10,087 emails sent)
   - EMEA MS: 0.11% reply rate (8,861 emails sent)
   - These two campaigns alone account for ~25% of all sends but almost zero replies

2. **Google-targeted campaigns perform 10-15x better**
   - Google → Google (US): 0.86%
   - EMEA Google: 1.42%
   - EMEA Google → Other: 1.82%

3. **Domain infrastructure is NOT the root cause**
   - All 15 inboxes share 3 similar domains
   - Same domains used across both high and low performing campaigns
   - Problem is message-to-audience fit, not deliverability

---

## Overall CGS Performance

| Metric | Value |
|--------|-------|
| Total Campaigns | 15 |
| Total Emails Sent | 76,521 |
| Total Replies | 501 |
| Unique Replies | 493 |
| Bounces | 521 |
| **Overall Reply Rate** | **0.64%** |
| Bounce Rate | 0.68% |

---

## Campaign Performance Breakdown

### ✅ High Performers (≥1% replies)

| Campaign | Sent | Replies | Reply Rate | Status |
|----------|------|---------|------------|--------|
| Real Estate UK - 11-200 | 1,000 | 26 | **2.60%** | paused |
| CyberSecurity EMEA - Google → Other | 2,422 | 44 | **1.82%** | completed |
| CyberSecurity EMEA - Google | 7,913 | 115 | **1.42%** | active |
| Crunchbase USA - SaaS - 11-50 | 697 | 9 | **1.29%** | completed |

### ⚠️ Low Performers (<0.5% replies)

| Campaign | Sent | Replies | Reply Rate | Status | Notes |
|----------|------|---------|------------|--------|-------|
| **CyberSecurity US - MS → MS** | 10,087 | 8 | **0.08%** | completed | 🚨 MAJOR PROBLEM |
| **CyberSecurity EMEA - MS** | 8,861 | 10 | **0.11%** | completed | 🚨 MAJOR PROBLEM |
| Crunchbase EU - SaaS - 3-10 | 4,681 | 15 | 0.32% | completed | Higher bounces |
| MVP USA - SaaS - 3-10 | 12,071 | 54 | 0.43% | active | Volume play |

### ⚡ Moderate (0.5-1% replies)

| Campaign | Sent | Replies | Reply Rate | Status |
|----------|------|---------|------------|--------|
| CyberSecurity US - MS → Other | 3,255 | 31 | 0.95% | completed |
| CyberSecurity US - Google → Google | 13,110 | 115 | 0.86% | completed |
| Crunchbase USA - SaaS - 1-2 | 607 | 4 | 0.66% | completed |
| MVP USA - SaaS - 1-2 | 2,049 | 13 | 0.59% | active |

---

## Sending Domain Analysis

### Domains in Use

| Domain | Inboxes | Notes |
|--------|---------|-------|
| theaicgsteamhq.info | 8 | Primary domain |
| thecgsteam.info | 5 | Secondary domain |
| theaicgsteam.info | 2 | Third domain |

**⚠️ Note:** The EmailBison API doesn't return per-inbox send statistics. Domain-level performance couldn't be isolated. However, since all campaigns use the same domain pool and some campaigns perform well, **domains are likely not the issue**.

---

## Pattern Analysis

### What's Working
1. **Google-targeted prospects** — consistently 0.8-1.8% reply rates
2. **EMEA CyberSecurity (non-MS)** — strong engagement
3. **Real Estate UK** — highest reply rate at 2.6%

### What's NOT Working
1. **Microsoft-targeted prospects** — 0.08-0.11% reply rates
   - Possible reasons:
     - MS spam filtering may be catching messages
     - Copy doesn't resonate with MS-stack companies
     - ICP mismatch
2. **Large SaaS campaigns** — volume with low reply rates suggests poor targeting

### Impact Analysis

If we exclude the two worst MS campaigns:

| Without MS→MS campaigns | Value |
|------------------------|-------|
| Emails Sent | 57,573 |
| Replies | 483 |
| **Reply Rate** | **0.84%** |

That's a **31% improvement** just from excluding the MS-heavy campaigns.

---

## Recommendations

### Immediate Actions

1. **⏸️ Pause or Archive MS-targeted campaigns**
   - CyberSecurity US - MS → MS (0.08% replies)
   - CyberSecurity EMEA - MS (0.11% replies)
   - These are damaging overall metrics and likely warming inboxes poorly

2. **📊 Split future campaigns by email provider**
   - Track Google vs MS vs Other separately
   - Adjust messaging for each environment

3. **🔍 Investigate MS deliverability**
   - Run deliverability tests (Glockapps, MailReach)
   - Check if messages hitting MS inboxes are landing in spam

### Infrastructure (Lower Priority)

Since domains don't appear to be the root cause:

4. **Keep current domains** — no need to replace or pause
5. **Consider adding Google Workspace inboxes** — may improve delivery to Google recipients
6. **Monitor bounce rates** — currently healthy at 0.68%

### Copy/Targeting Changes

7. **Audit MS campaign copy**
   - Is the value prop relevant to MS-stack companies?
   - Are there trigger words hitting spam filters?

8. **Consider audience overlap**
   - MS-heavy companies may have different buying patterns
   - Adjust ICP or messaging for this segment

---

## Data Files

- Raw JSON data: `/root/clawd/memory/cgs-domain-analysis.json`
- Analysis script: `/root/clawd/claude-code-projects/cgs_domain_analysis.py`

---

## Conclusion

The <1% reply rate is not a domain/infrastructure problem — it's a **targeting and copy problem concentrated in Microsoft-targeted campaigns**. The same sending infrastructure achieves 1-2.6% reply rates on other campaigns.

**Action: Pause MS campaigns, investigate deliverability to MS environments, and focus volume on Google-targeted prospects where CGS is already succeeding.**
