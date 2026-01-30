#!/usr/bin/env python3
"""Deep dive analysis for LTS positive reply drop on Jan 28."""

import httpx
import json
from datetime import datetime
from collections import defaultdict

# LTS workspace config
LTS_API_KEY = "34|HmjfeCILd2OtBfgCC4zvvYGaHShoZ45qJjVwcFj339c7497e"
BASE_URL = "https://send.leadsthat.show/api"

headers = {
    "Authorization": f"Bearer {LTS_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

client = httpx.Client(timeout=60.0, headers=headers)

def get_all_campaigns():
    """Get all campaigns from LTS workspace."""
    all_campaigns = []
    page = 1
    while page <= 20:
        response = client.get(f"{BASE_URL}/campaigns", params={"page": page, "per_page": 15})
        response.raise_for_status()
        data = response.json()
        campaigns = data.get("data", [])
        if not campaigns:
            break
        all_campaigns.extend(campaigns)
        print(f"Page {page}: {len(campaigns)} campaigns (total: {len(all_campaigns)})")
        if len(campaigns) < 15:
            break
        page += 1
    return all_campaigns

def get_campaign_line_chart_stats(campaign_id, start_date=None, end_date=None):
    """Get daily stats for a campaign."""
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    try:
        response = client.get(
            f"{BASE_URL}/campaigns/{campaign_id}/line-area-chart-stats",
            params=params
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error getting stats for campaign {campaign_id}: {e}")
        return None

def get_campaign_details(campaign_id):
    """Get full campaign details."""
    try:
        response = client.get(f"{BASE_URL}/campaigns/{campaign_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error getting details for campaign {campaign_id}: {e}")
        return None

# Main analysis
print("=" * 60)
print("LTS Deep Dive - Positive Reply Drop Analysis")
print("=" * 60)

# Step 1: Get all campaigns
print("\n[1] Fetching all LTS campaigns...")
campaigns = get_all_campaigns()
print(f"Total campaigns: {len(campaigns)}")

# Step 2: Get campaign details and daily stats
print("\n[2] Fetching daily stats for each campaign (Jan 19-29)...")

campaign_stats = {}
daily_totals = defaultdict(lambda: {"sent": 0, "replied": 0, "interested": 0, "opened": 0, "bounced": 0})

for c in campaigns:
    cid = c["id"]
    name = c.get("name", f"Campaign {cid}")
    status = c.get("status", "unknown")
    
    # Get line chart stats
    stats = get_campaign_line_chart_stats(cid, "2025-01-19", "2025-01-29")
    details = get_campaign_details(cid)
    
    if stats and details:
        campaign_data = details.get("data", details)
        campaign_stats[cid] = {
            "name": name,
            "status": status,
            "total_sent": campaign_data.get("emails_sent", 0),
            "total_replied": campaign_data.get("replied", 0),
            "total_interested": campaign_data.get("interested", 0),
            "total_unique_replies": campaign_data.get("unique_replies", 0),
            "created_at": campaign_data.get("created_at", ""),
            "daily_stats": stats
        }
        
        # Parse daily stats from the response
        # The format is usually: {"data": [{"date": "2025-01-19", "sent": X, ...}, ...]}
        daily_data = stats.get("data", stats) if isinstance(stats, dict) else stats
        if isinstance(daily_data, list):
            for day in daily_data:
                date = day.get("date", "")
                if date:
                    daily_totals[date]["sent"] += day.get("sent", 0) or 0
                    daily_totals[date]["replied"] += day.get("replied", 0) or 0
                    daily_totals[date]["interested"] += day.get("interested", 0) or day.get("positive_replies", 0) or 0
                    daily_totals[date]["opened"] += day.get("opened", 0) or 0
                    daily_totals[date]["bounced"] += day.get("bounced", 0) or 0
        
        print(f"  Campaign {cid} ({status}): {name[:40]}... - {campaign_data.get('emails_sent', 0)} sent, {campaign_data.get('interested', 0)} interested")

# Step 3: Print daily totals
print("\n" + "=" * 60)
print("[3] DAILY TOTALS (Jan 19-29)")
print("=" * 60)
print(f"{'Date':<12} {'Sent':>8} {'Replied':>8} {'Interested':>10} {'Rate':>8}")
print("-" * 50)
for date in sorted(daily_totals.keys()):
    d = daily_totals[date]
    rate = (d["interested"] / d["replied"] * 100) if d["replied"] > 0 else 0
    print(f"{date:<12} {d['sent']:>8} {d['replied']:>8} {d['interested']:>10} {rate:>7.1f}%")

# Step 4: Top campaigns by interested count
print("\n" + "=" * 60)
print("[4] TOP CAMPAIGNS BY TOTAL INTERESTED")
print("=" * 60)
top_campaigns = sorted(campaign_stats.items(), key=lambda x: x[1]["total_interested"], reverse=True)[:15]
print(f"{'ID':<6} {'Status':<10} {'Sent':>8} {'Replied':>8} {'Interested':>10} {'Name':<35}")
print("-" * 80)
for cid, data in top_campaigns:
    print(f"{cid:<6} {data['status']:<10} {data['total_sent']:>8} {data['total_replied']:>8} {data['total_interested']:>10} {data['name'][:35]}")

# Step 5: Check flagged campaigns (328, 330)
print("\n" + "=" * 60)
print("[5] FLAGGED CAMPAIGNS STATUS (328, 330)")
print("=" * 60)
for cid in [328, 330]:
    if cid in campaign_stats:
        data = campaign_stats[cid]
        print(f"\nCampaign {cid}: {data['name']}")
        print(f"  Status: {data['status']}")
        print(f"  Total Sent: {data['total_sent']}")
        print(f"  Total Replied: {data['total_replied']}")
        print(f"  Total Interested: {data['total_interested']}")
        
        # Print daily breakdown for this campaign
        daily_data = data["daily_stats"].get("data", data["daily_stats"]) if isinstance(data["daily_stats"], dict) else data["daily_stats"]
        if isinstance(daily_data, list):
            print("  Daily breakdown (Jan 19-29):")
            for day in daily_data:
                date = day.get("date", "")
                if date and "2025-01" in date:
                    sent = day.get("sent", 0) or 0
                    interested = day.get("interested", 0) or day.get("positive_replies", 0) or 0
                    replied = day.get("replied", 0) or 0
                    print(f"    {date}: sent={sent}, replied={replied}, interested={interested}")
    else:
        print(f"Campaign {cid}: Not found in current data")

# Step 6: Active vs Paused campaigns
print("\n" + "=" * 60)
print("[6] CAMPAIGN STATUS BREAKDOWN")
print("=" * 60)
status_counts = defaultdict(lambda: {"count": 0, "sent": 0, "interested": 0})
for cid, data in campaign_stats.items():
    status = data["status"]
    status_counts[status]["count"] += 1
    status_counts[status]["sent"] += data["total_sent"]
    status_counts[status]["interested"] += data["total_interested"]

for status, counts in sorted(status_counts.items()):
    print(f"{status}: {counts['count']} campaigns, {counts['sent']} sent, {counts['interested']} interested")

# Step 7: Output raw data for further analysis
output = {
    "daily_totals": dict(daily_totals),
    "campaign_stats": campaign_stats,
    "status_breakdown": dict(status_counts)
}

with open("/root/clawd/analysis/lts_raw_data.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("\n\nRaw data saved to /root/clawd/analysis/lts_raw_data.json")

client.close()
