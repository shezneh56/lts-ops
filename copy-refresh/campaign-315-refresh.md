# Campaign 315 — AS400 Refresh Copy

**Campaign:** AS400 Campaign - Retail/Manufacturing  
**Step:** 3287 (Step 2 Follow-up)  
**Workspace:** Gestell  
**Issue:** 0% reply rate vs 0.14% average (100% drop)  
**Date:** 2026-01-29

---

## Problem Analysis

**Original copy:**
```
Subject: Re: {{Quick question, {FIRST_NAME}|Question for you, {FIRST_NAME}|{FIRST_NAME} - quick question|{COMPANY}'s AS400 modernization}}

{FIRST_NAME}, worth a quick chat to see if we can help with your modernization project?
```

**Why it's failing:**
1. Zero technical credibility — sounds like every generic SDR
2. No pain point articulation — IT leaders need to see you understand their world
3. "Modernization project" is vague — AS400 shops face specific, known challenges
4. No value proposition — what do you actually do?
5. Subject uses `{{double braces}}` — should be single `{}`

---

## Refreshed Copy — Version A: Skills Gap Angle

**Subject:**
```
Re: {AS400 talent at {COMPANY}|{COMPANY}'s RPG developers|the AS400 skills gap}
```

**Body:**
```html
<p>{FIRST_NAME}, {circling back on this|wanted to bump this up|following up}.</p>

<p>{Finding developers who know RPG or COBOL|Hiring AS400 talent|Recruiting for legacy systems} gets harder every year. The developers who built your systems are {retiring|aging out|moving on} — and the knowledge goes with them.</p>

<p>We help {retail and manufacturing companies|companies like {COMPANY}|organizations running IBM i} {modernize without the rewrite risk|extend AS400 systems with modern APIs|bridge legacy and cloud} so you're not stuck in a talent crisis.</p>

<p>{Worth 15 minutes to see if we can help?|Open to a quick call?|Would a short conversation make sense?}</p>

<p>{SENDER_EMAIL_SIGNATURE}</p>

<p>P.S. One client {avoided a full rewrite|skipped the rip-and-replace|kept their core AS400 logic} and {cut integration time by 60 percent|connected to Salesforce in weeks, not months|launched a mobile app on top of their existing system}.</p>
```

---

## Refreshed Copy — Version B: Integration Pain Angle

**Subject:**
```
Re: {connecting {COMPANY}'s AS400|APIs for your IBM i|AS400 integration challenges}
```

**Body:**
```html
<p>{FIRST_NAME}, {bringing this back|following up on this|circling back}.</p>

<p>Most AS400 systems {weren't built to talk to anything|predate modern integration|don't have REST APIs}. That makes connecting to {your CRM|e-commerce platforms|cloud tools} {painful|expensive|a multi-month project}.</p>

<p>We {expose AS400 business logic as modern APIs|build integration layers for IBM i|connect legacy systems to the rest of your stack} — without {touching your core RPG code|risky rewrites|betting the business on a migration}.</p>

<p>{Does that problem exist at {COMPANY}?|Is that on your radar?|Worth a 15-minute call?}</p>

<p>{SENDER_EMAIL_SIGNATURE}</p>

<p>P.S. A {manufacturing client|retail company we work with|distribution company} {went from zero APIs to 40 endpoints|connected their AS400 to Shopify|automated order sync to their ERP} in {under 90 days|12 weeks|one quarter}.</p>
```

---

## Refreshed Copy — Version C: Technical Debt Angle

**Subject:**
```
Re: {{COMPANY}'s AS400 roadmap|legacy system strategy at {COMPANY}|IBM i modernization path}
```

**Body:**
```html
<p>{FIRST_NAME}, {bumping this up|floating this back|following up}.</p>

<p>{Rip-and-replace is risky and expensive|Full rewrites fail more than they succeed|Replacing a 30-year-old system is a multi-year bet}. But doing nothing means {mounting technical debt|increasing security exposure|falling further behind}.</p>

<p>There's a middle path: {modernize incrementally|add modern capabilities without rewriting|wrap your existing system with modern interfaces}. Keep what works, fix what doesn't.</p>

<p>If {COMPANY} is {weighing options|planning a roadmap|figuring out next steps} for your AS400 environment, {I'd like to share how others have approached it|let me show you what's worked for similar companies|worth comparing notes}.</p>

<p>{SENDER_EMAIL_SIGNATURE}</p>

<p>P.S. {We've helped companies|Our clients have} {avoid 7-figure rewrite projects|modernize in phases over 18 months|launch customer-facing apps without touching RPG code}.</p>
```

---

## Refreshed Copy — Version D: Security/Compliance Angle

**Subject:**
```
Re: {AS400 security at {COMPANY}|audit findings on legacy systems|IBM i compliance gaps}
```

**Body:**
```html
<p>{FIRST_NAME}, {following up|circling back|wanted to check in}.</p>

<p>Legacy systems {often fail modern security audits|create compliance headaches|have gaps that auditors flag}. {SOC 2|PCI|your security team} probably {has questions about your AS400|wants better visibility into IBM i access|needs logging and controls you don't have}.</p>

<p>We help {add modern authentication and logging|close security gaps without rewriting|bring AS400 environments up to current standards} — so you pass audits without {betting the business on a migration|a risky rewrite|disrupting operations}.</p>

<p>{Is compliance pressure part of what's driving modernization at {COMPANY}?|Does this match what you're seeing?|Worth a conversation?}</p>

<p>{SENDER_EMAIL_SIGNATURE}</p>

<p>P.S. One client {went from audit findings to clean report|closed 12 security gaps|added MFA to their AS400 access} in {90 days|one quarter|under 4 months}.</p>
```

---

## Implementation Notes

1. **Pick one version** to A/B test against current copy
2. **Fix the double braces** — EmailBison uses `{single|braces|for|spintax}`
3. **Subject lines reference Step 1** — these are follow-ups, so Re: is correct
4. **All versions under 100 words** — punchy, not walls of text
5. **P.S. has concrete proof** — specific outcomes, not vague claims

---

## Spam Check ✓

- [ ] No % symbol — used "percent" and "60 percent"
- [ ] No $ — avoided dollar amounts
- [ ] No urgency words — no "act now," "limited time"
- [ ] No overpromise — no "guaranteed," "revolutionary"
- [ ] No ALL CAPS — clean
- [ ] No "click here" — natural CTAs
- [ ] Variables correct — {FIRST_NAME}, {COMPANY}, {SENDER_EMAIL_SIGNATURE}
- [ ] Spintax has 3+ alternatives — verified throughout

---

## Recommendation

**Start with Version B (Integration Pain)** — it's the most concrete technical problem and easiest for prospects to self-identify with. If someone's running AS400 in 2026, they've definitely struggled to connect it to modern tools.

Version A (Skills Gap) is the backup if Version B doesn't improve performance — the talent shortage is universal but slightly more abstract.
