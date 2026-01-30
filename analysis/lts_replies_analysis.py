#!/usr/bin/env python3
"""Get replies with timestamps for daily analysis."""

import httpx
import json
from collections import defaultdict
from datetime import datetime

# LTS workspace config
LTS_API_KEY = "34|HmjfeCILd2OtBfgCC4zvvYGaHShoZ45qJjVwcFj339c7497e"
BASE_URL = "https://send.leadsthat.show/api"

headers = {
    "Authorization": f"Bearer {LTS_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

client = httpx.Client(timeout=60.0, headers=headers)

def get_all_leads(status=None, limit=500):
    """Get leads with pagination."""
    all_leads = []
    page = 1
    while page <= 50:  # Safety limit
        params = {"page": page, "per_page": 100}
        if status:
            params["status"] = status
        
        try:
            response = client.get(f"{BASE_URL}/leads", params=params)
            response.raise_for_status()
            data = response.json()
            leads = data.get("data", [])
            
            if not leads:
                break
            
            all_leads.extend(leads)
            print(f"Page {page}: {len(leads)} leads (total: {len(all_leads)})")
            
            if len(leads) < 100 or len(all_leads) >= limit:
                break
            page += 1
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    
    return all_leads

# Get interested/positive leads specifically
print("=" * 60)
print("Fetching Interested Leads...")
print("=" * 60)

# Try different status values
interested_leads = get_all_leads(status="interested", limit=500)
print(f"\nTotal 'interested' leads fetched: {len(interested_leads)}")

# Sample a few to see the data structure
if interested_leads:
    print("\nSample interested lead:")
    sample = interested_leads[0]
    print(json.dumps(sample, indent=2, default=str)[:2000])

# Analyze by date
print("\n" + "=" * 60)
print("Interested Leads by Date (updated_at)")
print("=" * 60)

date_counts = defaultdict(int)
campaign_date_counts = defaultdict(lambda: defaultdict(int))

for lead in interested_leads:
    # Try to get date from various fields
    date_field = lead.get("updated_at") or lead.get("created_at") or lead.get("replied_at")
    campaign_id = lead.get("campaign_id") or lead.get("campaign", {}).get("id")
    
    if date_field:
        # Parse date - format is usually "2025-01-20T15:30:00.000000Z"
        date_str = date_field[:10]
        date_counts[date_str] += 1
        if campaign_id:
            campaign_date_counts[campaign_id][date_str] += 1

print(f"\n{'Date':<12} {'Count':>8}")
print("-" * 25)
for date in sorted(date_counts.keys(), reverse=True)[:30]:
    print(f"{date:<12} {date_counts[date]:>8}")

# Campaign breakdown for interested
print("\n" + "=" * 60)
print("Interested by Campaign (from leads)")
print("=" * 60)

campaign_totals = defaultdict(int)
for campaign_id, dates in campaign_date_counts.items():
    total = sum(dates.values())
    campaign_totals[campaign_id] = total

for cid, total in sorted(campaign_totals.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"Campaign {cid}: {total} interested")

# Now try to get all replied leads
print("\n" + "=" * 60)
print("Fetching Replied Leads...")
print("=" * 60)

replied_leads = get_all_leads(status="replied", limit=500)
print(f"\nTotal 'replied' leads fetched: {len(replied_leads)}")

# Analyze replied by date
print("\n" + "=" * 60)
print("Replied Leads by Date")
print("=" * 60)

replied_date_counts = defaultdict(int)
for lead in replied_leads:
    date_field = lead.get("updated_at") or lead.get("replied_at") or lead.get("created_at")
    if date_field:
        date_str = date_field[:10]
        replied_date_counts[date_str] += 1

print(f"\n{'Date':<12} {'Count':>8}")
print("-" * 25)
for date in sorted(replied_date_counts.keys(), reverse=True)[:30]:
    print(f"{date:<12} {replied_date_counts[date]:>8}")

# Save results
results = {
    "interested_by_date": dict(date_counts),
    "replied_by_date": dict(replied_date_counts),
    "interested_by_campaign": dict(campaign_totals),
    "total_interested": len(interested_leads),
    "total_replied": len(replied_leads)
}

with open("/root/clawd/analysis/lts_daily_replies.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n\nResults saved to /root/clawd/analysis/lts_daily_replies.json")

client.close()
