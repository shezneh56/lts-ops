# Integration Status

## Active Integrations

### Gmail
- **Account:** liam@leadsthat.show
- **Access:** Read + Send
- **Filter:** Excludes warmup emails containing `p0zfhi2t`
- **Status:** ✅ Live

### Calendly
- **API Key:** Stored in .env
- **Tracking:** Recent bookings, invitee details
- **Status:** ✅ Live

### Fathom
- **API Key:** Stored in .env
- **Webhook Secret:** Configured
- **Use:** Call recording verification, transcript summaries
- **Status:** ⏳ Ready (not automated yet)

### Google Sheets
- **Call Tracker:** 1nXeNTdObxbH723Pdlo2Op48d_CJqjCoci6oaGJV1c9o
- **Access:** Public read (CSV export)
- **Status:** ✅ Live

## Daily Automations

### Morning Alert (8 AM CET)
- Scans call tracker for urgent actions
- Identifies follow-ups due
- Lists post-call tasks needed
- Shows top HOT leads
- Sends via WhatsApp to +447716953711
- **Status:** ✅ Scheduled (crontab)

### Voice Note Reminders (Hourly)
- Checks Calendly for new bookings
- Immediate reminder when call booked
- 11 PM CET reminder if not sent same day
- 9 AM prospect timezone reminder if still pending
- **Status:** ✅ Scheduled (crontab)

### Weekly Metrics (Friday 9 PM CET)
- Calls booked this week
- Show rate (showed / due)
- Target check (30 calls/week goal)
- Closes count
- Alerts if below targets
- **Status:** ✅ Scheduled (crontab)

## Pending Integrations

### iMessage / BlueBubbles
- **Purpose:** Auto-message new bookings, track voice note reminders
- **Number:** +16462940798 (US)
- **Status:** ⏳ Awaiting setup

### Calendly Webhooks
- **Purpose:** Real-time booking notifications (vs polling)
- **Status:** ⏳ Not set up yet

### Fathom Automation
- **Purpose:** Auto-generate call summaries, draft post-call emails
- **Status:** ⏳ Credentials ready, automation not built
