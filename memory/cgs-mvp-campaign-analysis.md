# CGS Team MVP Campaign Analysis - Reply Rate by Domain/Inbox

**Date:** 2025-02-01
**Focus:** Identifying burned inboxes/domains via reply rate analysis

---

## Executive Summary

**Key Finding:** The `.co` and `.com` domains are significantly underperforming compared to `.info` domains.

| TLD | Sent | Replies | Reply Rate | vs Average |
|-----|------|---------|------------|------------|
| **.info** | 95,551 | 1,655 | **1.73%** | +12% above avg |
| **.co** | 21,683 | 217 | **1.00%** | -35% below avg |
| **.com** | 8,934 | 82 | **0.92%** | -41% below avg |

**Overall Average:** 1.55% reply rate across 126,168 emails sampled

---

## 🔴 Domains to PAUSE (Likely Burned)

These domains have reply rates below 50% of average (< 0.77%):

| Domain | Sent | Replies | Reply Rate | Status |
|--------|------|---------|------------|--------|
| cgsteamai.com | 512 | 3 | **0.59%** | 🔴 PAUSE |
| cgsteamco.co | 1,166 | 9 | **0.77%** | 🔴 PAUSE |

---

## 🟡 Domains to MONITOR (Below Average)

These `.co` and `.com` domains are underperforming but not critically:

| Domain | Sent | Replies | Reply Rate | Status |
|--------|------|---------|------------|--------|
| cgsteamplatform.co | 2,245 | 18 | 0.80% | 🟡 Monitor |
| cgsteamops.co | 2,189 | 17 | 0.78% | 🟡 Monitor |
| cgsteameu.co | 1,886 | 17 | 0.90% | 🟡 Monitor |
| cgsteamtech.com | 1,737 | 15 | 0.86% | 🟡 Monitor |
| cgsteameu.com | 5,060 | 46 | 0.91% | 🟡 Monitor |
| salescgsteam.co | 1,209 | 11 | 0.91% | 🟡 Monitor |
| cgsteamagency.co | 1,169 | 11 | 0.94% | 🟡 Monitor |
| thecgsteam.co | 1,718 | 18 | 1.05% | 🟡 Monitor |
| cgsteamlabs.co | 2,456 | 24 | 0.98% | 🟡 Monitor |
| cgsteamsales.co | 1,014 | 11 | 1.08% | 🟡 Monitor |
| cgsteamnetwork.co | 1,124 | 12 | 1.07% | 🟡 Monitor |
| cgsteamgrowth.co | 1,322 | 14 | 1.06% | 🟡 Monitor |
| cgsteammarketing.co | 1,498 | 16 | 1.07% | 🟡 Monitor |
| thecgsteam.com | 973 | 10 | 1.03% | 🟡 Monitor |
| cgsteamco.com | 652 | 8 | 1.23% | 🟡 Monitor |

---

## 🟢 Domains PERFORMING WELL (Keep Active)

Top `.info` domains with above-average reply rates:

| Domain | Sent | Replies | Reply Rate | Status |
|--------|------|---------|------------|--------|
| cgsteampro.info | 1,726 | 43 | **2.49%** | 🟢 Excellent |
| cgsteammedia.info | 865 | 21 | **2.43%** | 🟢 Excellent |
| cgsteaminnovation.info | 867 | 21 | **2.42%** | 🟢 Excellent |
| cgsteamalliance.info | 1,724 | 41 | **2.38%** | 🟢 Excellent |
| cgsteamconsulting.info | 842 | 19 | **2.26%** | 🟢 Excellent |
| cgsteamplus.info | 1,714 | 38 | **2.22%** | 🟢 Excellent |
| cgsteamcore.info | 865 | 19 | **2.20%** | 🟢 Excellent |
| cgsteammatrix.info | 1,727 | 37 | **2.14%** | 🟢 Excellent |
| cgsteamnexus.info | 1,728 | 37 | **2.14%** | 🟢 Excellent |
| cgsteamcollective.info | 1,727 | 36 | **2.08%** | 🟢 Excellent |

---

## Recommendations

### Immediate Actions:
1. **PAUSE** `cgsteamai.com` - 62% below average, likely burned
2. **PAUSE** `cgsteamco.co` - 50% below average, likely burned

### Strategic Changes:
3. **Reduce volume** on ALL `.co` domains - performing 35% worse than `.info`
4. **Reduce volume** on ALL `.com` domains - performing 41% worse than `.info`
5. **Prioritize `.info` domains** - they're your best performers

### TLD Strategy:
The data strongly suggests `.info` TLD has significantly better deliverability for CGS campaigns:
- `.info`: 1.73% reply rate (baseline)
- `.co`: 1.00% reply rate (-42% vs .info)
- `.com`: 0.92% reply rate (-47% vs .info)

**Consider shifting sending volume away from `.co` and `.com` domains toward `.info` domains.**

---

## Data Notes

- **Sample size:** 126,168 emails across 7 MVP campaigns
- **Analysis method:** Sampled scheduled emails from multiple pages per campaign
- **Metrics used:** Reply rate (replies/sent) as primary deliverability indicator
- **Open tracking:** Intentionally disabled (normal for deliverability)

---

*Analysis performed using EmailBison API via campaign-engine*
