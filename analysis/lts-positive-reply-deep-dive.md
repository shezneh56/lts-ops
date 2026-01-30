# LTS Positive Reply Deep Dive
## Why Did Interested Count Drop on Jan 28?

**Generated:** 2025-01-29  
**Workspace:** Leads That Show (LTS)  
**Period Analyzed:** Jan 19-29, 2025

---

## Executive Summary

Liam's dashboard shows **361k sent, 5.6k replies, 136 interested** with peaks on Jan 20, 23, 27 and a sharp drop on Jan 28.

**Key Findings:**
1. **Current active campaigns have a 0.047% interest rate** - below the historical completed average of 0.055%
2. **Flagged campaigns 328 and 330 are severely underperforming** - 0% and 0.024% interest rates respectively
3. **Copy refreshes already exist** for both flagged campaigns - ready to deploy
4. **Best performing campaigns** achieve 0.15-0.19% interest rates - 3-4x the current active average
5. **9 campaigns are paused** representing 120k+ sends with only 0.018% interest rate - likely paused for good reason

---

## 1. Campaign Performance Analysis

### Active Campaigns (Currently Sending)

| Campaign ID | Name | Sent | Replied | Interested | Rate |
|-------------|------|------|---------|------------|------|
| **717** | LTS-PROF-SALES V5 | 64,821 | 708 | 35 | 0.054% |
| **421** | Tech B2B - CRO - US - old | 42,590 | 945 | 34 | 0.080% ⭐ |
| **712** | LTS-FIN-SALES V5 | 33,425 | 356 | 13 | 0.039% |
| **715** | LTS-FIN-MKT V5 | 5,603 | 62 | 0 | 0.000% ⚠️ |
| **714** | LTS-SAAS-MKT V5 | 1,471 | 20 | 0 | 0.000% ⚠️ |
| **713** | LTS-CYBER-SALES V5 | 2,539 | 23 | 0 | 0.000% ⚠️ |
| **424** | LTS - VC/PE - UK - Sales Leaders | 5,455 | 157 | 0 | 0.000% ⚠️ |
| **422** | LTS - VC/PE - US - Sales Leaders | 8,033 | 93 | 0 | 0.000% ⚠️ |
| **328** | LTS - SaaS - US - Sales Leaders | 9,734 | 131 | 0 | 0.000% 🔴 |
| **425** | LTS - VC/PE - UK - CEO/Founder | 12 | 0 | 0 | 0.000% |

**Total Active:** 173,683 sent → 82 interested (0.047%)

### Key Observations:
- Only **3 of 10 active campaigns** are generating interested replies
- Campaign 421 (Tech B2B - old) is outperforming the new V5 campaigns
- **6 campaigns showing ZERO interested** despite significant volume

---

## 2. Flagged Campaigns (328, 330)

### Campaign 328: LTS - SaaS - US - Sales Leaders
| Metric | Value |
|--------|-------|
| Status | **Active** |
| Total Sent | 9,734 |
| Total Replied | 131 (1.35% reply rate) |
| Interested | **0** (0.00% interest rate) |

**Diagnosis:** Campaign is getting replies but ZERO are positive. Copy is actively repelling prospects.

**Copy Issues Identified:**
- Step 2179: "pipeline predictability" - No spintax, template-like
- Step 2180: "75 meetings per quarter" - Repetitive structure  
- Step 2181: "quick question" - Spam-flagged subject
- Step 2182: "the prediction" - Too cute, repetitive phrases

**✅ COPY REFRESH READY:** `/root/clawd/copy-refresh/campaign-328-refresh.md`

---

### Campaign 330: LTS - SaaS - UK - Sales Leaders
| Metric | Value |
|--------|-------|
| Status | **Queued** |
| Total Sent | 16,733 |
| Total Replied | 257 (1.54% reply rate) |
| Interested | **4** (0.024% interest rate) |

**Diagnosis:** Better than 328 but still severely underperforming. Reply rate is decent, but positive conversion is terrible.

**Copy Issues Identified:**
- Step 2191: "quick question" - Generic, gets filtered
- Step 2192: "the prediction" - Vague, template format fingerprinted
- Step 2193: "Re: re: pipeline predictability" - Fake threading triggers spam

**✅ COPY REFRESH READY:** `/root/clawd/copy-refresh/campaign-330-refresh.md`

---

## 3. Historical Best Performers

These campaigns achieved the highest interest rates with significant volume:

| Campaign | Name | Sent | Interested | Rate | Status |
|----------|------|------|------------|------|--------|
| **20** | SaaS - Founder - US - 10-100 | 9,313 | 18 | **0.193%** | Completed |
| **35** | SaaS - CRO - US - 11-50 | 8,497 | 15 | **0.177%** | Archived |
| **57** | Tech B2B - CRO - US - 11-2000 pt 2 | 7,111 | 11 | **0.155%** | Completed |
| **23** | Marketing - Founder - US - 10-100 | 8,707 | 10 | **0.115%** | Completed |
| **108** | SaaS - CRO - US | 23,171 | 25 | **0.108%** | Completed |

**Insight:** Smaller company size (10-100, 11-50) and Founder/Marketing targeting consistently outperforms larger company CRO targeting.

---

## 4. Status Breakdown

| Status | Campaigns | Sent | Interested | Rate |
|--------|-----------|------|------------|------|
| **Active** | 10 | 173,683 | 82 | 0.047% |
| **Launching** | 1 | 62,526 | 19 | 0.030% |
| **Completed** | 70 | 626,085 | 344 | **0.055%** |
| **Paused** | 9 | 120,205 | 22 | 0.018% |
| **Queued** | 3 | 30,672 | 4 | 0.013% |
| **Archived** | 15 | 62,526 | 60 | **0.096%** |

**Insight:** Archived campaigns (older copy/approach) have nearly **2x the interest rate** of current active campaigns.

---

## 5. What Likely Caused the Jan 28 Drop

Based on the data:

1. **Cumulative effect of fingerprinting** - Campaigns 328, 330, and the new V5 campaigns have been flagged for repetitive copy. As more volume goes through fingerprinted templates, deliverability drops industry-wide.

2. **Zero-performing campaigns diluting totals** - 6 of 10 active campaigns have 0 interested. These keep sending volume but produce nothing, dragging down daily averages.

3. **Older high-performers completed** - The best campaigns (20, 35, 57, 108) are all completed/archived. New V5 campaigns haven't achieved similar performance.

4. **Reply-to-interested conversion collapsed** - Campaign 328 has 1.35% reply rate but 0% positive. People are responding but negatively.

---

## 6. Recommendations

### 🔴 URGENT (This Week)

1. **Deploy copy refresh for Campaign 328 immediately**
   - File: `/root/clawd/copy-refresh/campaign-328-refresh.md`
   - Replace all 4 steps (2179, 2180, 2181, 2182)
   - Campaign is actively damaging sender reputation with 0% positive

2. **Deploy copy refresh for Campaign 330**
   - File: `/root/clawd/copy-refresh/campaign-330-refresh.md`
   - Replace steps 2191, 2192, 2193
   - Resume from Queued status only after refresh

3. **Pause campaigns with 0% interested + high volume:**
   - 715 (LTS-FIN-MKT V5) - 5,603 sent, 0 interested
   - 424 (LTS - VC/PE - UK - Sales Leaders) - 5,455 sent, 0 interested
   - 422 (LTS - VC/PE - US - Sales Leaders) - 8,033 sent, 0 interested

### 🟡 SHORT-TERM (Next 2 Weeks)

4. **Audit V5 campaigns** - All the new V5 campaigns are underperforming the old versions:
   - 717 (LTS-PROF-SALES V5): 0.054% vs historical 0.09%
   - 712 (LTS-FIN-SALES V5): 0.039% vs historical 0.06%
   - 711 (LTS-SAAS-SALES V5): 0.030% vs historical 0.11%

5. **Replicate success patterns from top performers:**
   - Target smaller companies (10-100, 11-50 employees)
   - Focus on Founders/Marketing over pure Sales
   - Review copy from campaigns 20, 35, 57 for patterns

### 🟢 LONGER-TERM

6. **Campaign 421 is a star** - Tech B2B - CRO - US - old
   - 0.080% interest rate (best among active)
   - Increase volume allocation to this campaign
   - Study what makes this copy work

7. **Consider reactivating archived campaigns:**
   - Campaign 27: Prof Services - CRO - US - 51-500 (0.096% rate)
   - Campaign 35: SaaS - CRO - US - 11-50 (0.177% rate)

---

## 7. Available Copy Refreshes

These refreshes have already been written and are ready to deploy:

| Campaign | File | Priority |
|----------|------|----------|
| 328 | `/root/clawd/copy-refresh/campaign-328-refresh.md` | 🔴 Critical |
| 330 | `/root/clawd/copy-refresh/campaign-330-refresh.md` | 🔴 Critical |
| 140 | `/root/clawd/copy-refresh/campaign-140-refresh.md` | 🟡 Medium |
| 219 | `/root/clawd/copy-refresh/campaign-219-refresh.md` | 🟡 Medium |
| 315 | `/root/clawd/copy-refresh/campaign-315-refresh.md` | 🟡 Medium |
| 312/313/314 | `/root/clawd/copy-refresh/campaigns-312-313-314-refresh.md` | 🟡 Medium |
| 668 | `/root/clawd/copy-refresh/campaign-668-refresh.md` | 🟢 Low |
| 688 | `/root/clawd/copy-refresh/campaign-688-refresh.md` | 🟢 Low |

---

## 8. Bottom Line

**The drop on Jan 28 is likely due to:**
1. Fingerprinted copy on high-volume campaigns (328, 330, V5 series)
2. Zero-performing campaigns continuing to send without generating interested
3. Best performers exhausted (completed) without comparable replacements

**Fix priority:**
1. Refresh campaign 328 copy (0% interested is unacceptable)
2. Refresh campaign 330 copy before resuming
3. Pause or refresh V5 campaigns that show 0% interested
4. Shift volume to campaign 421 (best performer among active)
5. Study historical winners for copy patterns to apply to new campaigns
