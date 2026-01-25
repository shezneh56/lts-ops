# API Integrations Reference

Quick reference for all external APIs used by Clawdbot.

## Calendly

**Docs:** `/root/clawd/docs/calendly-api.md` (to be created)

**Base URL:** `https://api.calendly.com`
**Auth:** `Authorization: Bearer {API_KEY}`
**Key env var:** `CALENDLY_API_KEY`

**Main endpoints:**
- `GET /users/me` - Get current user
- `GET /scheduled_events` - List events
- `GET /scheduled_events/{uuid}/invitees` - Get attendee details

---

## EmailBison

**Docs:** `/root/clawd/docs/emailbison-mcp-setup.md`, `/root/clawd/docs/emailbison-workspaces.md`

**Base URL:** `https://send.leadsthat.show/api`
**Auth:** `Authorization: Bearer {API_KEY}`
**Config:** `/root/clawd/claude-code-projects/config/workspace_keys.json`

**11 Workspaces:** C2, CGS, Gestell, Hygraph, Jampot, Lawtech, LTS, Legalsoft, Medvirtual, Paralect, Wow24-7

**Main tools:**
- Daily digest with deliverability tracking
- Campaign & sequence step management
- Auto-refresh for flagged variants
- MCP server for Claude integration

---

## Fathom

**Docs:** `/root/clawd/docs/fathom-api.md`

**Base URL:** `https://api.fathom.ai/external/v1`
**Auth:** `X-Api-Key: {API_KEY}`
**Key env var:** `FATHOM_API_KEY`

**Main endpoints:**
- `GET /meetings` - Fetch recordings with pagination

**Helper:** `/root/clawd/gmail-integration/fathom-api.js`

---

## Gmail API

**Docs:** (to be created)

**Auth:** OAuth 2.0 via `token.json`
**Account:** liam@leadsthat.show
**Access:** Read + Send
**Filter:** Excludes warmup emails containing `p0zfhi2t`

**Main features:**
- Daily inbox monitoring
- Auto-send emails via templates
- Integration with call tracker alerts

---

## Google Sheets

**Call Tracker ID:** `1nXeNTdObxbH723Pdlo2Op48d_CJqjCoci6oaGJV1c9o`
**Access:** Public read via CSV export
**URL:** `https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv`

**No auth required** for read-only CSV export.

---

## OpenAI

**Key env var:** `OPENAI_API_KEY`
**Location:** `/root/clawd/.env`

**Used for:**
- Voice note transcription (Whisper API)
- Future: Email drafting, call summaries

**Cost:** Whisper = $0.006/minute

---

## Status: All APIs Working ✅

Last updated: 2026-01-25
