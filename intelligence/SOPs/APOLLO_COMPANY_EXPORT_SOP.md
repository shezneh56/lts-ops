# Apollo Company Export SOP

> **Standard Operating Procedure for Exporting Company Lists from Apollo**
> 
> This is the pre-requisite step BEFORE running people searches in Clay.

---

## Overview / Purpose

Export company lists from Apollo to use as inputs for Clay enrichment workflows. Apollo's company search provides rich firmographic data that forms the foundation for targeted outreach campaigns.

**Why this matters:** You need clean company lists with accurate firmographic data before you can find decision-makers at those companies in Clay.

---

## Prerequisites

- [ ] Active Apollo.io account with export credits
- [ ] Clear target criteria (industry keywords, geography, employee count)
- [ ] Access to Clay for downstream people enrichment

---

## Key Limitation: 10,000 Record Export Cap

⚠️ **Apollo only allows exporting 10,000 records at a time.**

If your search returns more than 10,000 results, you must "slice" the data into batches using filters (typically **employee count ranges**).

---

## Step-by-Step Instructions

### Step 1: Set Up Your Company Search

1. **Navigate to:** Apollo → Search → Companies
2. **Apply your filters:**
   - **Keywords/Industry:** Enter relevant terms (e.g., "private practice", "dental office")
   - **Location:** Select target geography (e.g., United States)
   - **Employee Count:** Start broad (e.g., 1-50 employees)

> 💡 **Example from Liam:** Starting with 37,000 leads, filtered to ~13,000 by adding specific keywords and limiting to 1-50 employees in the United States.

---

### Step 2: Check Your Result Count

Look at the total number of results displayed.

- **If ≤10,000:** Proceed directly to export (Step 4)
- **If >10,000:** You need to slice the data (Step 3)

---

### Step 3: Slice Data to Stay Under 10K (When Needed)

#### Strategy: Use Employee Count Ranges

The most reliable way to slice is by **custom employee count ranges**. Adjust the ranges until each batch is under 10,000 records.

**Example Workflow:**

| Batch | Employee Range | Result Count | Status |
|-------|---------------|--------------|--------|
| 1 | 1-10 | 10,800 | ❌ Still too high |
| 1 | 1-8 | 10,460 | ❌ Still too high |
| 1 | 1-7 | 9,600 | ✅ Ready to export |
| 2 | 8-50 | 3,639 | ✅ Ready to export |

**How to set custom ranges:**

1. Click on the **# of Employees** filter
2. Select **Custom Range**
3. Enter min/max values (e.g., 1-7)
4. Click **Apply**
5. Verify the result count is under 10,000

> 💡 **Pro tip:** Get the number as close to 10,000 as possible to minimize the number of batches needed. But it MUST be under 10,000 or you'll miss records.

#### Alternative Slicing Options

If employee count doesn't create good splits, you can also slice by:
- **Geography** (state by state, or region by region)
- **Industry sub-categories**
- **Revenue ranges**

---

### Step 4: Export the Batch

1. **Select All:**
   - Click the checkbox at the top of the results list
   - Confirm "Select All" to include all filtered results

2. **Click Export:**
   - Look for the **Export** button
   - The export will begin processing

3. **Wait for Processing:**
   - You'll see a progress indicator
   - Larger exports (9,000+) may take several minutes

---

### Step 5: Download Your Exports

1. **Navigate to:**
   - Click **Settings** (gear icon)
   - Select **All Settings**
   - Find **Imports and Exports** in the left sidebar
   - Click **CSV Exports**

2. **Monitor Progress:**
   - You'll see progress bars (e.g., "30%", "25%")
   - Wait until status shows "Complete"

3. **Download:**
   - Click the download button next to each completed export

---

### Step 6: Rename Files Descriptively

**Critical:** Rename the downloaded CSV files with a clear naming convention.

**Recommended Format:**
```
[Search Type]_[Industry/Vertical]_[Geography]_[Size]_Companies_Apollo.csv
```

**Examples:**
- `Private_Practices_USA_1-50_Companies_Apollo.csv`
- `Dental_Offices_California_1-10_Companies_Apollo.csv`
- `SaaS_Companies_USA_50-200_Companies_Apollo.csv`

> 💡 **Why this matters:** When you have multiple export files, clear naming prevents confusion during Clay import and helps track what's been processed.

---

### Step 7: Repeat for Additional Batches

If you sliced the data, repeat Steps 3-6 for each employee range band until you've captured all records.

**Verification:** Your batch totals should add up to (approximately) your original search count.
- Example: 9,600 + 3,639 = 13,239 ≈ 13,000 original results ✅

---

## Complete Workflow Example

**Scenario:** Export private practice companies in the USA with 1-50 employees

1. **Initial search:** 13,000 results (too large)
2. **Batch 1:** Filter to 1-7 employees → 9,600 results → Export
3. **Batch 2:** Filter to 8-50 employees → 3,639 results → Export
4. **Download both CSVs** from Settings → Imports and Exports → CSV Exports
5. **Rename files:**
   - `Private_Practices_USA_1-7_Companies_Apollo.csv`
   - `Private_Practices_USA_8-50_Companies_Apollo.csv`
6. **Ready for Clay!**

---

## Tips from Liam

- 🎯 "The idea here is to get this number as close to 10,000" — maximize each batch but stay under the limit
- ⚠️ "It has to be less than 10,000 because I could have already missed out on 70 accounts" — if you're at 10,070, you've lost 70 records
- 📋 Exports can run simultaneously — you don't have to wait for one to finish before starting another
- 🔄 Refresh the CSV Exports page to check progress

---

## Common Mistakes to Avoid

| Mistake | Why It's Bad | How to Avoid |
|---------|--------------|--------------|
| Exporting with >10K results | You'll silently lose records | Always verify count is under 10,000 before exporting |
| Not renaming files | Confusing "apollo_export_12345.csv" files | Rename immediately after download |
| Forgetting a batch | Missing a segment of your target market | Track your ranges and verify totals match |
| Overlapping ranges | Duplicate records | Use exclusive ranges (1-7, then 8-50, not 1-7 and 7-50) |

---

## What Happens Next

Once your Apollo company CSVs are downloaded and renamed:

1. **Import to Clay:** Upload the CSV files to a new Clay table
2. **People Search:** Use Clay's "Find People at Company" enrichment
3. **Continue the workflow:** Follow the Clay People Search SOP

---

## Quick Reference Checklist

- [ ] Search filters applied (keywords, geography, employee count)
- [ ] Result count verified under 10,000
- [ ] If >10K, sliced by employee count ranges
- [ ] All batches exported
- [ ] Exports downloaded from Settings → CSV Exports
- [ ] Files renamed with descriptive names
- [ ] Batch totals verified against original search count
- [ ] Ready for Clay import

---

*Last Updated: January 2025*
*Source: Loom Training Video - "Efficiently Exporting Company Leads from Apollo"*
