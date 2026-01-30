# TASKS.md

## Active Tasks (For Today - Jan 27)

### C2 Campaign Execution
- **Context:** 4-tier plan created. ABM (2,500 Optimizely users), Lookalikes, Sitecore Displacement, DXP Competitors. 10-year domains warming, LinkedIn running, Jack calling.
- **Pending:** Execute based on Sunday call outcomes
- **Added:** 2026-01-26

### MedVirtual Campaign Deploy
- **Context:** All 7 checkpoints COMPLETE (see /intelligence/clients/medvirtual/RESEARCH/). NPI data pulled (39K leads), Apollo searches created.
- **Pending:** Liam to review checkpoint outputs, then deploy to EmailBison (08-09)
- **Added:** 2026-01-25
- **Status:** ✅ Sub-agent completed all checkpoints

### Lead Database Setup
- **Context:** Complete system built at /root/clawd/lead-database/. Schema, upload script, full documentation ready.
- **Pending:** Create Supabase project, run schema.sql, test with sample data
- **Added:** 2026-01-25
- **Status:** ✅ Sub-agent completed all deliverables

### Deliverability Issues
- **Context:** Jampot "JP V3 - SaaS" Step 4014 dropped 61%. LawTech "USA - GC/Legal Ops" at 0% open rate.
- **Pending:** Copy refresh needed
- **Added:** 2026-01-26
- **8AM CET:** Deliverability checker runs - will provide summary

### Cua Computer-Server ✅
- **Status:** Running (Docker container `cua-desktop`)
- **noVNC:** http://localhost:6080
- **API:** http://localhost:8000
- **Added:** 2026-01-26

---

## Overnight Work Completed (Jan 26-27)

### Sub-Agent Outputs Reviewed ✅
**MedVirtual Campaign:** All 7 checkpoints complete
- 01_DATA_INVENTORY.md
- 02_BUYER_VOICE.md
- 03_PAIN_VALIDATION.md
- 04_POSITIONING.md
- 05_CAMPAIGN_ANGLES.md
- 06_EMAIL_COPY.md (+ v2)
- 07_DELIVERABILITY_CHECK.md

**Lead Database:** Complete system built
- schema.sql (Supabase)
- upload_leads.py (smart CSV import, auto-dedup)
- Full documentation
- Ready for testing with 208k Paralect leads

### Voice Note Reminder System Built ✅
**Location:** /root/clawd/gmail-integration/voice-note-tracker.js

**Commands:**
- `node voice-note-tracker.js check` - Check for new bookings
- `node voice-note-tracker.js evening` - 11 PM CET reminders
- `node voice-note-tracker.js morning` - 9 AM prospect timezone reminders
- `node voice-note-tracker.js done <name>` - Mark as sent
- `node voice-note-tracker.js status` - Show pending

**Current Status:** 25 upcoming calls tracked, all need voice notes

### Email Draft Formatting Fixed ✅
**Location:** /root/clawd/gmail-integration/create-draft.js

**Improvements:**
- Uses HTML Content-Type
- Proper line spacing and fonts
- Takes command line arguments
- No more broken half-page formatting

**Usage:**
```bash
node create-draft.js --to "email" --subject "Subject" --body "Body text"
```

### ClawdHub Research ✅
**Relevant skills found:**
- `recruitment-automation` - Recruitment automation (could help with hiring)
- `linkedin` - LinkedIn integration
- `n8n-workflow-automation` - n8n workflow automation
- `agent-browser-clawdbot` - Browser automation
- `browser-use-api` - Browser Use API

**Note:** Don't download without Liam's permission

---

## Completed Jan 26

### MedVirtual Lead Sourcing (MAJOR WIN)
- Discovered NPI Registry FREE public API
- Pulled 39,251 leads across 4 personas
- Tested in Clay: 32% website match rate
- Combined with niche databases = 100K+ potential leads

### C2 Campaign Strategy
- Created 4-Tier Plan
- Designed ABM multi-channel sequence
- Created Notion docs
- Trigify research: monitor PEOPLE not keywords

### Google API Access
- Calendar, Drive, Docs, Sheets, Compose scopes added
- All working

### Kent/Wavity Discovery Call
- Pulled Fathom transcript
- Drafted + sent post-call email
- Follow-up: Wed Jan 29, 11:30 AM Pacific (20:30 CET)

---

## Completed Jan 25

- Gmail API integration
- Call tracker monitoring
- Daily WhatsApp alerts (8 AM CET)
- Calendly integration
- Fathom credentials stored
- Business deep dive
- Spawned MedVirtual + Lead Database sub-agents

---

## Upcoming Calls

### Tomorrow (Jan 27)
- 12:30 CET - Maria Matos (Hygraph - existing client)
- 13:00 CET - Theodor Larsen
- 14:00 CET - Justin Smith
- 16:00 CET - Eberhard Lucke
- 17:00 CET - Alejandro Valenzuela
- 18:00 CET - Jordan Sanders
- 19:00 CET - Adam Brown

### Wednesday (Jan 28)
- 12:00 CET - Francois Labuschagne
- 18:15 CET - Tucker McCready
- 19:00 CET - Ria Richardson
- 20:30 CET - Kent Harkins (Wavity follow-up)

### Thursday (Jan 29)
- 13:00 CET - Jason Tunley
- 15:00 CET - Graham Clark
- 16:00 CET - Tino Sida
- 16:30 CET - Dave Fox
- 17:45 CET - Chan Lee
- 18:30 CET - Barry Rothstein
- 19:15 CET - Bader Obeid

### Friday (Jan 30)
- 15:30 CET - Alanna Johnson
- 16:30 CET - Scott Harvey
- 17:00 CET - Jeff Davis
- 17:30 CET - Bjorn Paulsson
- 18:30 CET - Lyman Wescott

---

## Ideas for Additional Help

Based on Liam's business (cold outbound agency), areas I could help more:

1. **Campaign Copy Generation** - Generate email variants faster, A/B test angles
2. **Lead Enrichment Pipeline** - Automate NPI → Clay → EmailBison flow
3. **Call Prep Summaries** - Before each call, pull company info + talking points
4. **Post-Call Automation** - Auto-draft follow-up emails from Fathom transcripts
5. **Deliverability Monitoring** - Daily digest of flagged campaigns
6. **Client Reporting** - Auto-generate weekly reports from EmailBison data
7. **Competitive Intel** - Monitor competitor pricing/positioning changes
8. **Desktop Automation (Cua)** - Automate legacy apps, data entry, GUI tasks

---

## Hard Rules
- NEVER send emails without Liam's permission
- NEVER download from ClawdHub without permission
