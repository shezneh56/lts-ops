# Slack Reporting System Specification

> Daily and weekly email campaign metrics notifications to Slack

**Author:** Clawd (subagent)  
**Created:** 2025-01-20  
**Status:** Draft Specification

---

## Table of Contents

1. [Overview](#overview)
2. [Data Sources](#data-sources)
3. [Metrics Definition](#metrics-definition)
4. [Report Formats](#report-formats)
5. [Slack Integration](#slack-integration)
6. [Implementation](#implementation)
7. [Sample Output](#sample-output)
8. [Configuration](#configuration)

---

## Overview

### Purpose

Automated Slack notifications providing visibility into email campaign performance across all workspaces. Reports surface key metrics, trends, and actionable alerts.

### Delivery Schedule

| Report Type | Schedule | Time (CET) | Day |
|-------------|----------|------------|-----|
| Daily Summary | Every weekday | 08:00 | Mon-Fri |
| Weekly Summary | Once per week | 09:00 | Monday |

### Target Audience

- Campaign managers
- Operations team
- Leadership (weekly only)

---

## Data Sources

### EmailBison API

**Base URL:** `https://send.leadsthat.show/api`

**Reference Implementation:** `/root/clawd/claude-code-projects/src/campaign_engine/deliverability/emailbison_client.py`

#### Required Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/campaigns` | GET | List all campaigns |
| `/campaigns/{id}` | GET | Campaign totals (sent, replied, bounced, interested) |
| `/campaigns/{id}/line-area-chart-stats` | GET | Daily breakdown with timestamps |
| `/sender-emails` | GET | Inbox health data |
| `/leads` | GET | Lead-level details (for meeting tracking) |
| `/replies` | GET | Reply content and sentiment |

#### Key Fields from Campaign Object

```python
{
    "id": 123,
    "name": "Campaign Name",
    "status": "active",
    "emails_sent": 1500,
    "replied": 45,
    "unique_replies": 42,
    "bounced": 12,
    "unsubscribed": 3,
    "interested": 28,
    "opened": 800,
    "unique_opens": 650,
    "total_leads_contacted": 1200
}
```

#### Line Chart Stats (Daily Breakdown)

```python
# GET /campaigns/{id}/line-area-chart-stats?start_date=2025-01-13&end_date=2025-01-20
{
    "data": [
        {"date": "2025-01-13", "sent": 50, "replies": 3, "interested": 2, "bounced": 1},
        {"date": "2025-01-14", "sent": 48, "replies": 2, "interested": 1, "bounced": 0},
        ...
    ]
}
```

### Workspace Configuration

**Location:** `/root/clawd/claude-code-projects/config/workspace_keys.json`

**Available Workspaces (11 total):**

| Short Name | Full Name | Workspace ID |
|------------|-----------|--------------|
| C2 | C2 Experience | 16 |
| CGS | CGS Team | 4 |
| Gestell | Gestell | 8 |
| Hygraph | Hygraph | 15 |
| Jampot | Jam Pot | 6 |
| Lawtech | LawTech | 3 |
| LTS | Leads That Show | 2 |
| Legalsoft | LegalSoft | 7 |
| Medvirtual | Med Virtual | 17 |
| Paralect | Paralect | 12 |
| Wow24-7 | Wow 24-7 | 5 |

---

## Metrics Definition

### Primary Metrics

| Metric | Calculation | Source |
|--------|-------------|--------|
| **Emails Sent** | Sum of `emails_sent` across campaigns | Campaign object |
| **Replies** | Sum of `replied` | Campaign object |
| **Reply Rate** | `(replied / emails_sent) * 100` | Calculated |
| **Positive Replies** | Sum of `interested` | Campaign object |
| **Positive Rate** | `(interested / replied) * 100` | Calculated |
| **Bounces** | Sum of `bounced` | Campaign object |
| **Bounce Rate** | `(bounced / emails_sent) * 100` | Calculated |
| **Meetings Booked** | Leads with status = "meeting_booked" or custom tag | Leads endpoint |

### Trend Calculation

```python
def calculate_trend(current: float, previous: float) -> str:
    """Calculate trend indicator vs previous period."""
    if previous == 0:
        return "🆕"  # New (no prior data)
    
    change = ((current - previous) / previous) * 100
    
    if change > 10:
        return f"↑ +{change:.1f}%"
    elif change < -10:
        return f"↓ {change:.1f}%"
    else:
        return f"→ {change:.1f}%"
```

### Period Definitions

| Report | Current Period | Comparison Period |
|--------|----------------|-------------------|
| Daily | Yesterday | Day before yesterday |
| Weekly | Last 7 days | Previous 7 days |

---

## Report Formats

### Daily Summary Report

**Purpose:** Quick morning overview of yesterday's performance

**Sections:**
1. Header with date
2. Global totals (all workspaces)
3. Per-workspace breakdown
4. Top performers
5. Alerts/warnings

### Weekly Summary Report

**Purpose:** Comprehensive weekly review with trends

**Sections:**
1. Header with week number
2. Global totals with WoW trends
3. Per-workspace detailed breakdown
4. Campaign leaderboard
5. Inbox health summary
6. Recommendations

---

## Slack Integration

### Webhook Setup

1. Create a Slack App at https://api.slack.com/apps
2. Enable "Incoming Webhooks"
3. Add webhook to desired channel
4. Store webhook URL in environment variable

**Environment Variable:**
```bash
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
```

**Optional - Multiple Channels:**
```bash
SLACK_WEBHOOK_DAILY="https://hooks.slack.com/services/..."   # #email-daily
SLACK_WEBHOOK_WEEKLY="https://hooks.slack.com/services/..."  # #email-weekly
SLACK_WEBHOOK_ALERTS="https://hooks.slack.com/services/..."  # #email-alerts
```

### Channel Recommendations

| Channel | Purpose | Webhook |
|---------|---------|---------|
| `#email-reports` | Daily + Weekly summaries | Primary |
| `#email-alerts` | Urgent alerts only (high bounce, low replies) | Optional |
| `#leadership-metrics` | Weekly executive summary | Optional |

### Message Formatting

Slack Block Kit is used for rich formatting.

**Key Block Types:**
- `header` - Report title
- `section` - Text with optional fields
- `divider` - Visual separator
- `context` - Small timestamp/metadata

**Formatting Tips:**
- Use emoji for visual scanning: 📊 📈 📉 ✅ ⚠️ 🚨
- Monospace for numbers: `` `1,234` ``
- Bold for emphasis: `*important*`
- Keep under 50 blocks per message (Slack limit)

---

## Implementation

### Option 1: Clawdbot Cron (Recommended)

Use Clawdbot's built-in cron scheduler for reliability.

**Setup:**
```bash
# Add to HEARTBEAT.md or create dedicated cron

# Daily report - 8am CET (7am UTC)
clawdbot cron add "0 7 * * 1-5" "python3 /root/clawd/scripts/slack_report.py --type daily"

# Weekly report - Monday 9am CET (8am UTC)
clawdbot cron add "0 8 * * 1" "python3 /root/clawd/scripts/slack_report.py --type weekly"
```

### Option 2: Standalone Python Script

**Location:** `/root/clawd/scripts/slack_report.py`

```python
#!/usr/bin/env python3
"""
Slack Reporting Script for Email Campaign Metrics

Usage:
    python slack_report.py --type daily
    python slack_report.py --type weekly
    python slack_report.py --type daily --dry-run
"""

import os
import sys
import json
import httpx
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent / "claude-code-projects"))

from campaign_engine.deliverability.emailbison_client import EmailBisonClient


class SlackReporter:
    """Generate and send Slack reports for email campaign metrics."""
    
    def __init__(self):
        self.webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        self.config_path = Path("/root/clawd/claude-code-projects/config/workspace_keys.json")
        self.workspaces = self._load_workspaces()
    
    def _load_workspaces(self) -> List[Dict]:
        """Load workspace configuration."""
        with open(self.config_path) as f:
            return json.load(f)["workspaces"]
    
    def fetch_workspace_stats(
        self,
        workspace: Dict,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Fetch stats for a single workspace."""
        client = EmailBisonClient(api_key=workspace["api_key"])
        client.base_url = workspace["base_url"]
        
        try:
            # Get all campaigns
            campaigns = []
            page = 1
            while True:
                batch = client.list_campaigns(page=page, per_page=15)
                if not batch:
                    break
                campaigns.extend(batch)
                if len(batch) < 15:
                    break
                page += 1
            
            # Filter active campaigns and aggregate
            totals = {
                "workspace": workspace["short_name"],
                "campaigns_active": 0,
                "emails_sent": 0,
                "replies": 0,
                "positive_replies": 0,
                "bounced": 0,
                "meetings_booked": 0,  # Requires custom tracking
            }
            
            for campaign in campaigns:
                if campaign.get("status") != "active":
                    continue
                
                totals["campaigns_active"] += 1
                
                # Get detailed stats with date filtering
                try:
                    details = client.get_campaign(str(campaign["id"]))
                    data = details.get("data", details)
                    
                    totals["emails_sent"] += data.get("emails_sent", 0)
                    totals["replies"] += data.get("replied", 0)
                    totals["positive_replies"] += data.get("interested", 0)
                    totals["bounced"] += data.get("bounced", 0)
                except Exception as e:
                    print(f"Warning: Failed to get campaign {campaign['id']}: {e}")
            
            # Calculate rates
            if totals["emails_sent"] > 0:
                totals["reply_rate"] = round(
                    totals["replies"] / totals["emails_sent"] * 100, 2
                )
                totals["bounce_rate"] = round(
                    totals["bounced"] / totals["emails_sent"] * 100, 2
                )
            else:
                totals["reply_rate"] = 0
                totals["bounce_rate"] = 0
            
            if totals["replies"] > 0:
                totals["positive_rate"] = round(
                    totals["positive_replies"] / totals["replies"] * 100, 2
                )
            else:
                totals["positive_rate"] = 0
            
            return totals
            
        finally:
            client.close()
    
    def fetch_all_stats(self, start_date: str, end_date: str) -> List[Dict]:
        """Fetch stats for all workspaces."""
        all_stats = []
        
        for workspace in self.workspaces:
            try:
                stats = self.fetch_workspace_stats(workspace, start_date, end_date)
                all_stats.append(stats)
            except Exception as e:
                print(f"Error fetching {workspace['short_name']}: {e}")
                all_stats.append({
                    "workspace": workspace["short_name"],
                    "error": str(e)
                })
        
        return all_stats
    
    def calculate_global_totals(self, workspace_stats: List[Dict]) -> Dict:
        """Aggregate totals across all workspaces."""
        totals = {
            "emails_sent": 0,
            "replies": 0,
            "positive_replies": 0,
            "bounced": 0,
            "campaigns_active": 0,
        }
        
        for ws in workspace_stats:
            if "error" in ws:
                continue
            totals["emails_sent"] += ws.get("emails_sent", 0)
            totals["replies"] += ws.get("replies", 0)
            totals["positive_replies"] += ws.get("positive_replies", 0)
            totals["bounced"] += ws.get("bounced", 0)
            totals["campaigns_active"] += ws.get("campaigns_active", 0)
        
        # Calculate rates
        if totals["emails_sent"] > 0:
            totals["reply_rate"] = round(
                totals["replies"] / totals["emails_sent"] * 100, 2
            )
            totals["bounce_rate"] = round(
                totals["bounced"] / totals["emails_sent"] * 100, 2
            )
        else:
            totals["reply_rate"] = 0
            totals["bounce_rate"] = 0
        
        if totals["replies"] > 0:
            totals["positive_rate"] = round(
                totals["positive_replies"] / totals["replies"] * 100, 2
            )
        else:
            totals["positive_rate"] = 0
        
        return totals
    
    def build_daily_blocks(
        self,
        date: str,
        global_totals: Dict,
        workspace_stats: List[Dict],
        previous_totals: Optional[Dict] = None
    ) -> List[Dict]:
        """Build Slack blocks for daily report."""
        
        def trend(current: float, previous: Optional[float]) -> str:
            if previous is None or previous == 0:
                return ""
            change = ((current - previous) / previous) * 100
            if change > 10:
                return f" ↑{change:.0f}%"
            elif change < -10:
                return f" ↓{abs(change):.0f}%"
            return ""
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Daily Email Report - {date}",
                    "emoji": True
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Global Summary*"
                },
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Emails Sent*\n`{global_totals['emails_sent']:,}`{trend(global_totals['emails_sent'], previous_totals.get('emails_sent') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Reply Rate*\n`{global_totals['reply_rate']}%`{trend(global_totals['reply_rate'], previous_totals.get('reply_rate') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Positive Replies*\n`{global_totals['positive_replies']}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Bounce Rate*\n`{global_totals['bounce_rate']}%`"
                    }
                ]
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Per-Workspace Breakdown*"
                }
            }
        ]
        
        # Add workspace rows (sorted by sent volume)
        sorted_ws = sorted(
            [w for w in workspace_stats if "error" not in w],
            key=lambda x: x.get("emails_sent", 0),
            reverse=True
        )
        
        workspace_text = ""
        for ws in sorted_ws:
            sent = ws.get("emails_sent", 0)
            if sent == 0:
                continue
            emoji = "🟢" if ws.get("reply_rate", 0) >= 3 else "🟡" if ws.get("reply_rate", 0) >= 1 else "🔴"
            workspace_text += f"{emoji} *{ws['workspace']}*: `{sent:,}` sent | `{ws.get('reply_rate', 0)}%` reply | `{ws.get('positive_replies', 0)}` positive\n"
        
        if workspace_text:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": workspace_text.strip()
                }
            })
        
        # Add timestamp
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Generated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
                }
            ]
        })
        
        return blocks
    
    def build_weekly_blocks(
        self,
        week_start: str,
        week_end: str,
        global_totals: Dict,
        workspace_stats: List[Dict],
        previous_totals: Optional[Dict] = None
    ) -> List[Dict]:
        """Build Slack blocks for weekly report."""
        
        def trend_emoji(current: float, previous: Optional[float]) -> str:
            if previous is None or previous == 0:
                return "🆕"
            change = ((current - previous) / previous) * 100
            if change > 10:
                return f"📈 +{change:.0f}%"
            elif change < -10:
                return f"📉 {change:.0f}%"
            return f"➡️ {change:+.0f}%"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Weekly Email Report",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*{week_start}* to *{week_end}*"
                    }
                ]
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*🌐 Global Totals (Week-over-Week)*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Emails Sent*\n`{global_totals['emails_sent']:,}`\n{trend_emoji(global_totals['emails_sent'], previous_totals.get('emails_sent') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Total Replies*\n`{global_totals['replies']}`\n{trend_emoji(global_totals['replies'], previous_totals.get('replies') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Reply Rate*\n`{global_totals['reply_rate']}%`\n{trend_emoji(global_totals['reply_rate'], previous_totals.get('reply_rate') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Positive Replies*\n`{global_totals['positive_replies']}`\n{trend_emoji(global_totals['positive_replies'], previous_totals.get('positive_replies') if previous_totals else None)}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Positive Rate*\n`{global_totals['positive_rate']}%`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Bounce Rate*\n`{global_totals['bounce_rate']}%`\n{trend_emoji(global_totals['bounce_rate'], previous_totals.get('bounce_rate') if previous_totals else None)}"
                    }
                ]
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*📋 Workspace Breakdown*"
                }
            }
        ]
        
        # Detailed workspace table
        sorted_ws = sorted(
            [w for w in workspace_stats if "error" not in w],
            key=lambda x: x.get("emails_sent", 0),
            reverse=True
        )
        
        # Top 5 detailed
        for ws in sorted_ws[:5]:
            if ws.get("emails_sent", 0) == 0:
                continue
                
            status = "🟢" if ws.get("bounce_rate", 0) < 2 else "🟡" if ws.get("bounce_rate", 0) < 5 else "🔴"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{status} *{ws['workspace']}*"
                },
                "fields": [
                    {"type": "mrkdwn", "text": f"Sent: `{ws.get('emails_sent', 0):,}`"},
                    {"type": "mrkdwn", "text": f"Reply: `{ws.get('reply_rate', 0)}%`"},
                    {"type": "mrkdwn", "text": f"Positive: `{ws.get('positive_replies', 0)}`"},
                    {"type": "mrkdwn", "text": f"Bounce: `{ws.get('bounce_rate', 0)}%`"}
                ]
            })
        
        # Remaining workspaces summarized
        if len(sorted_ws) > 5:
            remaining = sorted_ws[5:]
            remaining_text = ", ".join([f"{w['workspace']} ({w.get('emails_sent', 0):,})" for w in remaining if w.get("emails_sent", 0) > 0])
            if remaining_text:
                blocks.append({
                    "type": "context",
                    "elements": [
                        {"type": "mrkdwn", "text": f"_Other workspaces: {remaining_text}_"}
                    ]
                })
        
        # Footer
        blocks.extend([
            {"type": "divider"},
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"📅 Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC | 11 workspaces tracked"
                    }
                ]
            }
        ])
        
        return blocks
    
    def send_to_slack(self, blocks: List[Dict], dry_run: bool = False) -> bool:
        """Send blocks to Slack webhook."""
        if dry_run:
            print("=== DRY RUN - Would send to Slack ===")
            print(json.dumps({"blocks": blocks}, indent=2))
            return True
        
        if not self.webhook_url:
            print("ERROR: SLACK_WEBHOOK_URL not set")
            return False
        
        try:
            response = httpx.post(
                self.webhook_url,
                json={"blocks": blocks},
                timeout=30
            )
            response.raise_for_status()
            print(f"Successfully sent to Slack: {response.status_code}")
            return True
        except Exception as e:
            print(f"Failed to send to Slack: {e}")
            return False
    
    def run_daily(self, dry_run: bool = False):
        """Generate and send daily report."""
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        day_before = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")
        
        print(f"Generating daily report for {yesterday}...")
        
        # Fetch current and previous stats
        current_stats = self.fetch_all_stats(yesterday, yesterday)
        current_totals = self.calculate_global_totals(current_stats)
        
        # For comparison (simplified - uses cumulative totals)
        previous_totals = None  # Could implement proper daily delta tracking
        
        blocks = self.build_daily_blocks(
            yesterday,
            current_totals,
            current_stats,
            previous_totals
        )
        
        return self.send_to_slack(blocks, dry_run)
    
    def run_weekly(self, dry_run: bool = False):
        """Generate and send weekly report."""
        today = datetime.utcnow().date()
        week_end = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        
        prev_week_end = (today - timedelta(days=8)).strftime("%Y-%m-%d")
        prev_week_start = (today - timedelta(days=14)).strftime("%Y-%m-%d")
        
        print(f"Generating weekly report for {week_start} to {week_end}...")
        
        current_stats = self.fetch_all_stats(week_start, week_end)
        current_totals = self.calculate_global_totals(current_stats)
        
        # Previous week for trends
        prev_stats = self.fetch_all_stats(prev_week_start, prev_week_end)
        prev_totals = self.calculate_global_totals(prev_stats)
        
        blocks = self.build_weekly_blocks(
            week_start,
            week_end,
            current_totals,
            current_stats,
            prev_totals
        )
        
        return self.send_to_slack(blocks, dry_run)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Slack Email Campaign Reporter")
    parser.add_argument("--type", choices=["daily", "weekly"], required=True)
    parser.add_argument("--dry-run", action="store_true", help="Print output without sending")
    
    args = parser.parse_args()
    
    reporter = SlackReporter()
    
    if args.type == "daily":
        success = reporter.run_daily(dry_run=args.dry_run)
    else:
        success = reporter.run_weekly(dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

### Required Environment Variables

```bash
# Required
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional (for multi-channel setup)
SLACK_WEBHOOK_DAILY="https://hooks.slack.com/services/..."
SLACK_WEBHOOK_WEEKLY="https://hooks.slack.com/services/..."
SLACK_WEBHOOK_ALERTS="https://hooks.slack.com/services/..."
```

### File Structure

```
/root/clawd/
├── scripts/
│   └── slack_report.py          # Main reporting script
├── claude-code-projects/
│   ├── config/
│   │   └── workspace_keys.json  # Workspace API keys
│   └── src/campaign_engine/
│       └── deliverability/
│           └── emailbison_client.py
└── data/
    └── slack_reports/           # Historical report data (optional)
        ├── daily_2025-01-19.json
        └── weekly_2025-W03.json
```

---

## Sample Output

### Mock Daily Report

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Daily Email Report - 2025-01-19                      │
├─────────────────────────────────────────────────────────┤
│ Global Summary                                          │
│                                                         │
│ Emails Sent     Reply Rate      Positive Replies        │
│ `2,847`         `3.2%` ↑12%     `52`                    │
│                                                         │
│ Bounce Rate     Active Campaigns                        │
│ `1.8%`          `34`                                    │
├─────────────────────────────────────────────────────────┤
│ Per-Workspace Breakdown                                 │
│                                                         │
│ 🟢 LTS: `892` sent | `4.1%` reply | `18` positive       │
│ 🟢 Paralect: `654` sent | `3.8%` reply | `12` positive  │
│ 🟡 Hygraph: `421` sent | `2.1%` reply | `6` positive    │
│ 🟡 CGS: `398` sent | `2.8%` reply | `8` positive        │
│ 🔴 C2: `312` sent | `0.9%` reply | `2` positive         │
│ 🟢 Gestell: `170` sent | `5.2%` reply | `6` positive    │
├─────────────────────────────────────────────────────────┤
│ Generated at 2025-01-20 07:00 UTC                       │
└─────────────────────────────────────────────────────────┘
```

### Mock Weekly Report (Slack Block Kit Preview)

```
📊 Weekly Email Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2025-01-13 to 2025-01-19

🌐 Global Totals (Week-over-Week)
┌────────────────┬────────────────┬────────────────┐
│ Emails Sent    │ Total Replies  │ Reply Rate     │
│ `18,234`       │ `547`          │ `3.0%`         │
│ 📈 +8%         │ 📈 +15%        │ 📈 +6%         │
├────────────────┼────────────────┼────────────────┤
│ Positive Reply │ Positive Rate  │ Bounce Rate    │
│ `312`          │ `57%`          │ `1.9%`         │
│ 📈 +12%        │ ➡️ +2%         │ 📉 -5%         │
└────────────────┴────────────────┴────────────────┘

📋 Workspace Breakdown

🟢 LTS (Leads That Show)
   Sent: `5,234`  Reply: `4.2%`  Positive: `98`  Bounce: `1.2%`

🟢 Paralect
   Sent: `3,892`  Reply: `3.6%`  Positive: `72`  Bounce: `1.5%`

🟡 Hygraph
   Sent: `2,567`  Reply: `2.4%`  Positive: `34`  Bounce: `2.1%`

🟡 CGS Team
   Sent: `2,145`  Reply: `2.9%`  Positive: `42`  Bounce: `2.8%`

🟢 Gestell
   Sent: `1,456`  Reply: `5.1%`  Positive: `38`  Bounce: `0.9%`

Other workspaces: C2 (987), Jampot (654), Lawtech (543),
                  Legalsoft (398), Medvirtual (234), Wow24-7 (124)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 Generated 2025-01-20 08:00 UTC | 11 workspaces tracked
```

### Slack Block Kit JSON (Daily Example)

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📊 Daily Email Report - 2025-01-19",
        "emoji": true
      }
    },
    {"type": "divider"},
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*Global Summary*"},
      "fields": [
        {"type": "mrkdwn", "text": "*Emails Sent*\n`2,847` ↑12%"},
        {"type": "mrkdwn", "text": "*Reply Rate*\n`3.2%`"},
        {"type": "mrkdwn", "text": "*Positive Replies*\n`52`"},
        {"type": "mrkdwn", "text": "*Bounce Rate*\n`1.8%`"}
      ]
    },
    {"type": "divider"},
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Per-Workspace Breakdown*\n🟢 *LTS*: `892` sent | `4.1%` reply | `18` positive\n🟢 *Paralect*: `654` sent | `3.8%` reply | `12` positive\n🟡 *Hygraph*: `421` sent | `2.1%` reply | `6` positive"
      }
    },
    {
      "type": "context",
      "elements": [
        {"type": "mrkdwn", "text": "Generated at 2025-01-20 07:00 UTC"}
      ]
    }
  ]
}
```

---

## Configuration

### Slack App Setup Steps

1. **Create Slack App**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name: "Email Campaign Reporter"
   - Select workspace

2. **Enable Incoming Webhooks**
   - Navigate to "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" ON
   - Click "Add New Webhook to Workspace"
   - Select target channel (e.g., `#email-reports`)
   - Copy the webhook URL

3. **Set Environment Variable**
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T.../B.../..."
   ```

4. **Test Webhook**
   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Test from Email Reporter 🚀"}' \
     $SLACK_WEBHOOK_URL
   ```

### Cron Schedule Setup

Using Clawdbot cron (preferred):

```bash
# List existing crons
clawdbot cron list

# Add daily report (8am CET = 7am UTC)
clawdbot cron add "0 7 * * 1-5" "cd /root/clawd && python3 scripts/slack_report.py --type daily"

# Add weekly report (Monday 9am CET = 8am UTC)
clawdbot cron add "0 8 * * 1" "cd /root/clawd && python3 scripts/slack_report.py --type weekly"
```

Alternative: System crontab

```bash
crontab -e

# Add:
0 7 * * 1-5 cd /root/clawd && /usr/bin/python3 scripts/slack_report.py --type daily >> /var/log/slack-report.log 2>&1
0 8 * * 1 cd /root/clawd && /usr/bin/python3 scripts/slack_report.py --type weekly >> /var/log/slack-report.log 2>&1
```

---

## Future Enhancements

1. **Meetings Tracking**
   - Integrate with calendar API or CRM
   - Track leads with "meeting_booked" status

2. **Alert System**
   - Separate channel for urgent alerts
   - Trigger on: bounce rate > 5%, reply rate drop > 50%

3. **Interactive Reports**
   - Add Slack buttons for drill-down
   - "View Campaign Details" action

4. **Historical Trends**
   - Store daily snapshots in `/data/slack_reports/`
   - Generate 30-day trend charts

5. **Custom Workspace Grouping**
   - Group by client type
   - Separate reports per team

---

## Appendix: API Rate Limits

EmailBison API considerations:
- No documented rate limits, but recommend 1 req/sec
- Fetch campaigns in batches of 15 (API max per_page)
- Cache workspace totals if running multiple reports

---

*End of Specification*
