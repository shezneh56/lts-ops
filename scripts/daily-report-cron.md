# Daily Report Cron Job Specification

## Schedule
Run daily at 8:00 AM CET (Central European Time)

CET is UTC+1 in winter, UTC+2 in summer (CEST).
- Winter: 8:00 CET = 07:00 UTC
- Summer: 8:00 CEST = 06:00 UTC

For simplicity, use 07:00 UTC (will be 8:00 AM CET in winter, 9:00 AM CEST in summer).

## Cron Entry

```cron
# Daily LTS Performance Report at 07:00 UTC (8:00 CET winter / 9:00 CEST summer)
0 7 * * * /usr/bin/python3 /root/clawd/scripts/daily-report.py --output /root/clawd/reports/daily-$(date +\%Y-\%m-\%d).txt 2>&1 | logger -t lts-daily-report
```

Or with timezone-aware timing (requires TZ-aware cron like cronie):
```cron
# Using CET timezone explicitly (if supported)
TZ=Europe/Amsterdam
0 8 * * * /usr/bin/python3 /root/clawd/scripts/daily-report.py --output /root/clawd/reports/daily-$(date +\%Y-\%m-\%d).txt 2>&1 | logger -t lts-daily-report
```

## Setup Instructions

1. Create reports directory:
```bash
mkdir -p /root/clawd/reports
```

2. Edit crontab:
```bash
crontab -e
```

3. Add the cron entry (pick one from above)

4. (Optional) Set up Calendly API token:
```bash
# Add to /etc/environment or ~/.bashrc
export CALENDLY_API_TOKEN="your_token_here"
```

5. Test manually:
```bash
/usr/bin/python3 /root/clawd/scripts/daily-report.py --text
```

## Alternative: Systemd Timer (recommended)

Create `/etc/systemd/system/lts-daily-report.service`:
```ini
[Unit]
Description=LTS Daily Performance Report
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /root/clawd/scripts/daily-report.py --output /root/clawd/reports/daily-%Y-%m-%d.txt
Environment="CALENDLY_API_TOKEN=your_token_here"
WorkingDirectory=/root/clawd/scripts
User=root
```

Create `/etc/systemd/system/lts-daily-report.timer`:
```ini
[Unit]
Description=Run LTS Daily Report at 8:00 CET

[Timer]
OnCalendar=*-*-* 07:00:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:
```bash
systemctl daemon-reload
systemctl enable lts-daily-report.timer
systemctl start lts-daily-report.timer
```

## Output Locations

- Text + JSON report: `/root/clawd/reports/daily-YYYY-MM-DD.txt`
- Logs: `journalctl -t lts-daily-report` or syslog

## Calendly Integration

✅ **Already configured!** The script auto-loads the Calendly API key from:
`/root/clawd/gmail-integration/.env` (CALENDLY_API_KEY)

No additional setup needed. Meeting counts are automatically included in reports.
