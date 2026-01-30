#!/usr/bin/env python3
"""
Daily Performance Report for Leads That Show

Pulls metrics from EmailBison API across all workspaces and generates
a consolidated daily report with:
- Emails sent (yesterday)
- Replies / reply rate
- Positive (interested) replies / rate
- Bounces / bounce rate
- Meetings booked (from Calendly, if configured)

Usage:
    python3 daily-report.py                    # Yesterday's report
    python3 daily-report.py --date 2025-01-15  # Specific date
    python3 daily-report.py --json             # JSON output only
    python3 daily-report.py --text             # Text output only
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

# Configuration
CONFIG_PATH = Path("/root/clawd/claude-code-projects/config/workspace_keys.json")
CALENDLY_ENV_FILE = Path("/root/clawd/gmail-integration/.env")
CALENDLY_TOKEN_ENV = "CALENDLY_API_KEY"  # From .env file or environment


def load_calendly_token() -> Optional[str]:
    """Load Calendly API token from .env file or environment."""
    # First check environment variable
    token = os.environ.get(CALENDLY_TOKEN_ENV)
    if token:
        return token
    
    # Then check .env file
    if CALENDLY_ENV_FILE.exists():
        try:
            with open(CALENDLY_ENV_FILE) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{CALENDLY_TOKEN_ENV}="):
                        return line.split("=", 1)[1].strip()
        except Exception:
            pass
    
    return None


class EmailBisonAPI:
    """Simple EmailBison API client for daily stats."""
    
    def __init__(self, api_key: str, base_url: str = "https://send.leadsthat.show/api"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
    
    def list_campaigns(self, page: int = 1, per_page: int = 50) -> List[Dict]:
        """Get list of campaigns."""
        resp = self.client.get(
            f"{self.base_url}/campaigns",
            params={"page": page, "per_page": per_page}
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", []) if isinstance(data, dict) else data
    
    def get_campaign_stats(self, campaign_id: str) -> Dict:
        """Get detailed campaign stats."""
        resp = self.client.get(f"{self.base_url}/campaigns/{campaign_id}")
        resp.raise_for_status()
        return resp.json()
    
    def get_line_chart_stats(
        self, 
        campaign_id: str, 
        start_date: str, 
        end_date: str
    ) -> Dict:
        """Get daily breakdown stats for a campaign."""
        resp = self.client.get(
            f"{self.base_url}/campaigns/{campaign_id}/line-area-chart-stats",
            params={"start_date": start_date, "end_date": end_date}
        )
        resp.raise_for_status()
        return resp.json()
    
    def get_scheduled_emails(
        self, 
        campaign_id: str, 
        page: int = 1, 
        per_page: int = 100
    ) -> Dict:
        """Get scheduled email records with timestamps."""
        resp = self.client.get(
            f"{self.base_url}/campaigns/{campaign_id}/scheduled-emails",
            params={"page": page, "per_page": per_page}
        )
        resp.raise_for_status()
        return resp.json()
    
    def close(self):
        self.client.close()


class CalendlyAPI:
    """Calendly API client for meeting bookings."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.calendly.com"
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            }
        )
        self._user_uri = None
        self._org_uri = None
    
    def _get_current_user(self) -> Dict:
        """Get current user info to find organization."""
        resp = self.client.get(f"{self.base_url}/users/me")
        resp.raise_for_status()
        return resp.json()
    
    def get_scheduled_events(
        self, 
        min_start_time: str, 
        max_start_time: str
    ) -> List[Dict]:
        """
        Get scheduled events within a time range.
        
        Uses the /scheduled_events endpoint with user parameter.
        Docs: https://developer.calendly.com/api-docs
        """
        # Get user URI if not cached
        if not self._user_uri:
            user_data = self._get_current_user()
            self._user_uri = user_data.get("resource", {}).get("uri")
            self._org_uri = user_data.get("resource", {}).get("current_organization")
        
        events = []
        page_token = None
        
        while True:
            # Query by user (required parameter)
            params = {
                "user": self._user_uri,
                "min_start_time": min_start_time,
                "max_start_time": max_start_time,
                "status": "active",
                "count": 100,
            }
            if page_token:
                params["page_token"] = page_token
            
            resp = self.client.get(f"{self.base_url}/scheduled_events", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            events.extend(data.get("collection", []))
            
            pagination = data.get("pagination", {})
            page_token = pagination.get("next_page_token")
            if not page_token:
                break
        
        return events
    
    def get_invitee_info(self, event_uri: str) -> List[Dict]:
        """Get invitee details for an event."""
        try:
            # Extract event UUID from URI
            resp = self.client.get(f"{event_uri}/invitees")
            resp.raise_for_status()
            return resp.json().get("collection", [])
        except Exception:
            return []
    
    def close(self):
        self.client.close()


def load_workspaces() -> List[Dict]:
    """Load workspace configurations."""
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return config.get("workspaces", [])


def parse_line_chart_stats(data: Dict, target_date: str) -> Dict[str, int]:
    """
    Parse the line-area-chart-stats response format.
    
    Format: {
      "data": [
        {"label": "Replied", "dates": [["2026-01-20", 5], ...]},
        {"label": "Sent", "dates": [["2026-01-20", 100], ...]},
        ...
      ]
    }
    """
    result = {
        "emails_sent": 0,
        "replies": 0,
        "positive_replies": 0,
        "bounces": 0,
        "opens": 0,
    }
    
    # Map API labels to our stat keys
    label_map = {
        "sent": "emails_sent",
        "replied": "replies",
        "interested": "positive_replies",
        "bounced": "bounces",
        "total opens": "opens",
        "unique opens": "opens",  # fallback if total opens not present
    }
    
    metrics = data.get("data", [])
    if not isinstance(metrics, list):
        return result
    
    for metric in metrics:
        label = metric.get("label", "").lower()
        stat_key = label_map.get(label)
        
        if not stat_key:
            continue
        
        dates = metric.get("dates", [])
        for date_entry in dates:
            if isinstance(date_entry, list) and len(date_entry) >= 2:
                date_str, value = date_entry[0], date_entry[1]
                if date_str == target_date:
                    result[stat_key] += int(value)
                    break
    
    return result


def get_workspace_daily_stats(
    workspace: Dict, 
    target_date: str
) -> Dict[str, Any]:
    """
    Get daily stats for a single workspace.
    
    Returns aggregated stats across all campaigns for the target date.
    """
    api = EmailBisonAPI(workspace["api_key"], workspace.get("base_url", "https://send.leadsthat.show/api"))
    
    stats = {
        "workspace_id": workspace["id"],
        "workspace_name": workspace["name"],
        "short_name": workspace["short_name"],
        "date": target_date,
        "emails_sent": 0,
        "replies": 0,
        "positive_replies": 0,
        "bounces": 0,
        "opens": 0,
        "campaigns_checked": 0,
        "errors": [],
    }
    
    try:
        # Get all campaigns (paginate)
        all_campaigns = []
        page = 1
        while True:
            campaigns = api.list_campaigns(page=page, per_page=50)
            if not campaigns:
                break
            all_campaigns.extend(campaigns)
            if len(campaigns) < 50:
                break
            page += 1
        
        # Include all campaigns that have sent emails (regardless of status)
        active_campaigns = [
            c for c in all_campaigns 
            if c.get("emails_sent", 0) > 0 or c.get("status") in ("active", "running")
        ]
        
        stats["campaigns_checked"] = len(active_campaigns)
        
        # Get daily stats for each campaign
        for campaign in active_campaigns:
            campaign_id = str(campaign["id"])
            try:
                # Use line-chart-stats endpoint (has daily breakdown)
                daily_data = api.get_line_chart_stats(
                    campaign_id, 
                    start_date=target_date, 
                    end_date=target_date
                )
                
                # Parse the EmailBison line-chart response format
                day_stats = parse_line_chart_stats(daily_data, target_date)
                
                stats["emails_sent"] += day_stats["emails_sent"]
                stats["replies"] += day_stats["replies"]
                stats["positive_replies"] += day_stats["positive_replies"]
                stats["bounces"] += day_stats["bounces"]
                stats["opens"] += day_stats["opens"]
                        
            except httpx.HTTPStatusError as e:
                if e.response.status_code != 404:
                    stats["errors"].append(f"Campaign {campaign_id}: {str(e)}")
            except Exception as e:
                stats["errors"].append(f"Campaign {campaign_id}: {str(e)}")
        
    except Exception as e:
        stats["errors"].append(f"Workspace error: {str(e)}")
    finally:
        api.close()
    
    # Calculate rates
    if stats["emails_sent"] > 0:
        stats["reply_rate"] = round(stats["replies"] / stats["emails_sent"] * 100, 2)
        stats["positive_rate"] = round(stats["positive_replies"] / stats["emails_sent"] * 100, 2)
        stats["bounce_rate"] = round(stats["bounces"] / stats["emails_sent"] * 100, 2)
    else:
        stats["reply_rate"] = 0.0
        stats["positive_rate"] = 0.0
        stats["bounce_rate"] = 0.0
    
    return stats


def get_calendly_meetings(target_date: str) -> Dict[str, Any]:
    """
    Get Calendly meetings scheduled for a specific date.
    
    Queries events where start_time falls within the target date.
    """
    token = load_calendly_token()
    
    result = {
        "available": False,
        "meetings_booked": 0,
        "meetings": [],
        "error": None,
    }
    
    if not token:
        result["error"] = f"Calendly API token not found. Set {CALENDLY_TOKEN_ENV} in environment or {CALENDLY_ENV_FILE}"
        return result
    
    try:
        api = CalendlyAPI(token)
        
        # Get events scheduled for target date (UTC)
        start_time = f"{target_date}T00:00:00Z"
        end_time = f"{target_date}T23:59:59Z"
        
        events = api.get_scheduled_events(start_time, end_time)
        
        result["available"] = True
        result["meetings_booked"] = len(events)
        
        # Extract useful meeting info
        for e in events:
            meeting = {
                "name": e.get("name"),
                "start_time": e.get("start_time"),
                "end_time": e.get("end_time"),
                "status": e.get("status"),
                "created_at": e.get("created_at"),
                "invitees_count": e.get("invitees_counter", {}).get("total", 0),
            }
            
            # Get event type name if available
            event_type = e.get("event_type", "")
            if event_type:
                meeting["event_type_uri"] = event_type
            
            result["meetings"].append(meeting)
        
        api.close()
        
    except httpx.HTTPStatusError as e:
        result["error"] = f"Calendly API error: {e.response.status_code} - {e.response.text[:200]}"
    except Exception as e:
        result["error"] = f"Calendly error: {str(e)}"
    
    return result


def generate_report(target_date: str, output_format: str = "both") -> Dict:
    """
    Generate the full daily performance report.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        output_format: "json", "text", or "both"
    
    Returns:
        Complete report as dictionary
    """
    workspaces = load_workspaces()
    
    report = {
        "report_date": target_date,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "workspaces": [],
        "totals": {
            "emails_sent": 0,
            "replies": 0,
            "positive_replies": 0,
            "bounces": 0,
            "opens": 0,
            "reply_rate": 0.0,
            "positive_rate": 0.0,
            "bounce_rate": 0.0,
        },
        "calendly": None,
        "errors": [],
    }
    
    print(f"Generating daily report for {target_date}...\n", file=sys.stderr)
    
    # Collect stats from each workspace
    for ws in workspaces:
        print(f"  Fetching {ws['short_name']}...", file=sys.stderr)
        stats = get_workspace_daily_stats(ws, target_date)
        report["workspaces"].append(stats)
        
        # Aggregate totals
        report["totals"]["emails_sent"] += stats["emails_sent"]
        report["totals"]["replies"] += stats["replies"]
        report["totals"]["positive_replies"] += stats["positive_replies"]
        report["totals"]["bounces"] += stats["bounces"]
        report["totals"]["opens"] += stats["opens"]
        
        if stats["errors"]:
            report["errors"].extend(stats["errors"])
    
    # Calculate total rates
    if report["totals"]["emails_sent"] > 0:
        report["totals"]["reply_rate"] = round(
            report["totals"]["replies"] / report["totals"]["emails_sent"] * 100, 2
        )
        report["totals"]["positive_rate"] = round(
            report["totals"]["positive_replies"] / report["totals"]["emails_sent"] * 100, 2
        )
        report["totals"]["bounce_rate"] = round(
            report["totals"]["bounces"] / report["totals"]["emails_sent"] * 100, 2
        )
    
    # Get Calendly meetings
    print("  Checking Calendly...", file=sys.stderr)
    report["calendly"] = get_calendly_meetings(target_date)
    
    print("\nDone!\n", file=sys.stderr)
    
    return report


def format_text_report(report: Dict) -> str:
    """Format report as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"DAILY PERFORMANCE REPORT - {report['report_date']}")
    lines.append(f"Generated: {report['generated_at']}")
    lines.append("=" * 60)
    lines.append("")
    
    # Totals section
    t = report["totals"]
    lines.append("📊 TOTALS (All Workspaces)")
    lines.append("-" * 40)
    lines.append(f"  Emails Sent:      {t['emails_sent']:,}")
    lines.append(f"  Replies:          {t['replies']:,} ({t['reply_rate']}%)")
    lines.append(f"  Positive Replies: {t['positive_replies']:,} ({t['positive_rate']}%)")
    lines.append(f"  Bounces:          {t['bounces']:,} ({t['bounce_rate']}%)")
    lines.append(f"  Opens:            {t['opens']:,}")
    lines.append("")
    
    # Calendly section
    cal = report.get("calendly", {})
    lines.append("📅 MEETINGS (Calendly)")
    lines.append("-" * 40)
    if cal.get("available"):
        lines.append(f"  Meetings Booked: {cal['meetings_booked']}")
        # Show meeting details if any
        for m in cal.get("meetings", [])[:10]:  # Limit to 10
            start = m.get("start_time", "")[:16].replace("T", " ")  # Truncate to min
            name = m.get("name", "Meeting")[:30]
            lines.append(f"    • {start} - {name}")
        if len(cal.get("meetings", [])) > 10:
            lines.append(f"    ... and {len(cal['meetings']) - 10} more")
    elif cal.get("error"):
        lines.append(f"  ⚠️  {cal['error']}")
    else:
        lines.append("  Not configured")
    lines.append("")
    
    # Per-workspace breakdown
    lines.append("📈 BY WORKSPACE")
    lines.append("-" * 40)
    
    # Sort by emails sent (descending)
    sorted_ws = sorted(
        report["workspaces"], 
        key=lambda x: x["emails_sent"], 
        reverse=True
    )
    
    for ws in sorted_ws:
        if ws["emails_sent"] > 0 or ws["replies"] > 0:
            lines.append(f"  {ws['short_name']:12} | Sent: {ws['emails_sent']:4} | "
                        f"Replies: {ws['replies']:3} ({ws['reply_rate']:5.1f}%) | "
                        f"Pos: {ws['positive_replies']:3} | "
                        f"Bounce: {ws['bounces']:3}")
    
    # Show workspaces with no activity
    inactive = [ws for ws in sorted_ws if ws["emails_sent"] == 0 and ws["replies"] == 0]
    if inactive:
        lines.append("")
        lines.append(f"  No activity: {', '.join(ws['short_name'] for ws in inactive)}")
    
    lines.append("")
    
    # Errors section
    if report["errors"]:
        lines.append("⚠️  ERRORS")
        lines.append("-" * 40)
        for err in report["errors"][:5]:  # Limit to 5
            lines.append(f"  • {err[:80]}")
        if len(report["errors"]) > 5:
            lines.append(f"  ... and {len(report['errors']) - 5} more")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate daily performance report for Leads That Show"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Report date (YYYY-MM-DD). Defaults to yesterday."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON only"
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Output text only"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (default: stdout)"
    )
    
    args = parser.parse_args()
    
    # Default to yesterday
    if args.date:
        target_date = args.date
    else:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        target_date = yesterday.strftime("%Y-%m-%d")
    
    # Validate date format
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{target_date}'. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    report = generate_report(target_date)
    
    # Determine output format
    if args.json:
        output = json.dumps(report, indent=2)
    elif args.text:
        output = format_text_report(report)
    else:
        # Both
        output = format_text_report(report)
        output += "\n\n--- JSON DATA ---\n"
        output += json.dumps(report, indent=2)
    
    # Output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
