# Clay ICP Validation & Pain Point Identification

**Created:** 2026-01-29
**Status:** Spec needed
**Priority:** High — Med Virtual showing "wrong person" replies

## Problem

Leads entering campaigns don't match ICP. Result: "We don't do that" / "Wrong person" replies.

## Solution: Two New Clay Columns

### Column 1: ICP Validator

**Purpose:** Validate lead matches Ideal Customer Profile before entering sequence.

**Inputs:**
- Job title
- Company name
- Company description/keywords
- Company size
- Industry

**Output:** 
- `ICP_MATCH`: Yes / No / Maybe
- `ICP_REASON`: Brief explanation

**Logic (per client):**
- Define ICP criteria in campaign setup
- AI validates against criteria
- Hard filter or soft flag based on confidence

### Column 2: Pain Point Identifier

**Purpose:** Extract relevant pain point for personalization.

**Inputs:**
- Company website/description
- Company keywords
- Industry
- Recent news (optional)

**Output:**
- `PAIN_POINT`: Specific pain point relevant to our service
- `PERSONALIZATION_HOOK`: One-liner to use in email

**Example:**
- Company: "Healthcare staffing agency, 50 employees, rapid growth"
- Pain Point: "Scaling intake without adding headcount"
- Hook: "Noticed [COMPANY] is growing fast — most healthcare staffing firms hit a wall at intake volume around this stage"

## Implementation Options

1. **Hard filter** — Don't send to non-ICP (safest)
2. **Soft flag** — Tag and send different copy
3. **Hybrid** — Filter obvious mismatches, flag edge cases

## Rollout

1. Start with Med Virtual (current problem)
2. Expand to all client campaigns
3. Template the ICP criteria per vertical

## Clay Integration

- Use Clay AI column or HTTP request to Claude API
- Add as enrichment step before sequence upload
- Cost: ~$0.01-0.02 per lead for AI validation
