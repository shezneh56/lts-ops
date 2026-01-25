# Reporting Agent - Setup Notes

## Repository Location
`/root/clawd/claude-code-projects`

## Key Context
Full system documentation: `intelligence/agents/REPORTING_AGENT_CONTEXT.md`

## Daily Workflow

**8:05 AM CET Daily:**
1. Read latest reports from data/ directories
2. Generate WhatsApp summary
3. Send to Liam

**On User Commands:**
- **REFRESH {STEP_ID}** → Generate 3 new copy variants
- **DETAIL {CAMPAIGN_ID}** → Full campaign breakdown
- **HEALTH** → Inbox health summary
- **STATUS** → System status check

## Report Files to Monitor
- `data/variant_stats/variant_report_*.json` - Variant performance
- `data/fingerprint_monitor/report_*.json` - Reply rate drops
- `data/inbox_health/health_check_*.json` - Inbox health
- `data/inbox_health/daily_digest_latest.json` - Pre-generated summary

## Workspaces
- **LTS** (Leads That Show) - Main client
- **Lawtech** - Legal tech vertical
- **CGS** - Client campaigns
- **Paralect** - Tech company

## Commands to Run

**Generate daily digest:**
```bash
cd /root/clawd/claude-code-projects
python -m campaign_engine.deliverability.daily_digest
python -m campaign_engine.deliverability.daily_digest --format json
```

**Handle REFRESH command:**
```bash
python -m campaign_engine.deliverability.daily_digest --command "REFRESH 4298"
```

## Next Steps
1. Test daily_digest.py execution (may need dependencies)
2. Set up 8:05 AM CET cron job
3. Create command handler for REFRESH/DETAIL/HEALTH/STATUS
4. Test end-to-end workflow

## Integration Status
✅ Repository cloned
✅ Context loaded
⏳ Python dependencies (need to check)
⏳ Cron job setup
⏳ Command handlers
