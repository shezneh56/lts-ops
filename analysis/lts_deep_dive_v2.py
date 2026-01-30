#!/usr/bin/env python3
"""Deep dive analysis for LTS positive reply drop on Jan 28 - V2."""

import json
from collections import defaultdict

# Load the raw data we already collected
with open("/root/clawd/analysis/lts_raw_data.json", "r") as f:
    raw_data = json.load(f)

campaign_stats = raw_data["campaign_stats"]

# Parse the daily stats from the chart format
# Format is: {"data": [{"label": "Replied", "dates": [["2025-01-19", 5], ...]}, ...]}

daily_totals = defaultdict(lambda: {"sent": 0, "replied": 0, "interested": 0, "opens": 0})
campaign_daily = {}  # Store per-campaign daily data

print("=" * 80)
print("LTS DEEP DIVE - POSITIVE REPLY DROP ANALYSIS (V2)")
print("=" * 80)

for cid, data in campaign_stats.items():
    name = data["name"]
    status = data["status"]
    daily_stats = data.get("daily_stats", {})
    
    if not daily_stats or not isinstance(daily_stats, dict):
        continue
    
    chart_data = daily_stats.get("data", [])
    if not chart_data:
        continue
    
    # Initialize campaign daily tracker
    campaign_daily[cid] = {
        "name": name,
        "status": status,
        "total_interested": data.get("total_interested", 0),
        "total_sent": data.get("total_sent", 0),
        "daily": defaultdict(lambda: {"sent": 0, "replied": 0, "interested": 0, "opens": 0})
    }
    
    # Parse each metric series
    for series in chart_data:
        label = series.get("label", "").lower()
        dates = series.get("dates", [])
        
        for date_entry in dates:
            if isinstance(date_entry, list) and len(date_entry) >= 2:
                date, value = date_entry[0], date_entry[1] or 0
                
                if "sent" in label:
                    daily_totals[date]["sent"] += value
                    campaign_daily[cid]["daily"][date]["sent"] = value
                elif "replied" in label:
                    daily_totals[date]["replied"] += value
                    campaign_daily[cid]["daily"][date]["replied"] = value
                elif "interested" in label:
                    daily_totals[date]["interested"] += value
                    campaign_daily[cid]["daily"][date]["interested"] = value
                elif "open" in label:
                    daily_totals[date]["opens"] += value
                    campaign_daily[cid]["daily"][date]["opens"] = value

# Print daily totals
print("\n" + "=" * 80)
print("[1] DAILY TOTALS (Jan 19-29)")
print("=" * 80)
print(f"{'Date':<12} {'Sent':>8} {'Replied':>8} {'Interested':>10} {'Int. Rate':>10}")
print("-" * 55)

dates_sorted = sorted([d for d in daily_totals.keys() if d >= "2025-01-19" and d <= "2025-01-29"])
for date in dates_sorted:
    d = daily_totals[date]
    rate = (d["interested"] / d["replied"] * 100) if d["replied"] > 0 else 0
    print(f"{date:<12} {d['sent']:>8} {d['replied']:>8} {d['interested']:>10} {rate:>9.1f}%")

# Find campaigns that contributed interested on peak days (Jan 20, 23, 27)
print("\n" + "=" * 80)
print("[2] CAMPAIGNS CONTRIBUTING TO INTERESTED ON PEAK DAYS")
print("=" * 80)

peak_days = ["2025-01-20", "2025-01-23", "2025-01-27"]
drop_day = "2025-01-28"

for date in peak_days + [drop_day]:
    print(f"\n--- {date} ---")
    contributions = []
    for cid, cdata in campaign_daily.items():
        interested = cdata["daily"].get(date, {}).get("interested", 0)
        if interested > 0:
            contributions.append((cid, cdata["name"], cdata["status"], interested))
    
    contributions.sort(key=lambda x: x[3], reverse=True)
    
    if contributions:
        for cid, name, status, interested in contributions[:10]:
            print(f"  Campaign {cid} ({status}): {interested} interested - {name[:50]}")
    else:
        print("  No interested recorded")

# Top campaigns by total interested (all time)
print("\n" + "=" * 80)
print("[3] TOP 20 CAMPAIGNS BY TOTAL INTERESTED (ALL TIME)")
print("=" * 80)
print(f"{'ID':<6} {'Status':<12} {'Sent':>8} {'Interested':>10} {'Rate':>8} {'Name':<35}")
print("-" * 85)

top_campaigns = sorted(
    [(cid, d["name"], d["status"], d["total_sent"], d["total_interested"]) 
     for cid, d in campaign_stats.items()],
    key=lambda x: x[4], reverse=True
)[:20]

for cid, name, status, sent, interested in top_campaigns:
    rate = (interested / sent * 100) if sent > 0 else 0
    print(f"{cid:<6} {status:<12} {sent:>8} {interested:>10} {rate:>7.2f}% {name[:35]}")

# Analyze what changed on Jan 28
print("\n" + "=" * 80)
print("[4] WHAT CHANGED ON JAN 28 (Drop Day)")
print("=" * 80)

# Compare Jan 27 vs Jan 28
jan27 = daily_totals.get("2025-01-27", {"sent": 0, "replied": 0, "interested": 0})
jan28 = daily_totals.get("2025-01-28", {"sent": 0, "replied": 0, "interested": 0})

print(f"\nJan 27: Sent={jan27['sent']}, Replied={jan27['replied']}, Interested={jan27['interested']}")
print(f"Jan 28: Sent={jan28['sent']}, Replied={jan28['replied']}, Interested={jan28['interested']}")
print(f"Change: Sent={jan28['sent']-jan27['sent']}, Replied={jan28['replied']-jan27['replied']}, Interested={jan28['interested']-jan27['interested']}")

# Find campaigns that stopped/reduced on Jan 28
print("\n\nCampaigns that sent on Jan 27 but NOT on Jan 28:")
stopped_campaigns = []
for cid, cdata in campaign_daily.items():
    jan27_sent = cdata["daily"].get("2025-01-27", {}).get("sent", 0)
    jan28_sent = cdata["daily"].get("2025-01-28", {}).get("sent", 0)
    
    if jan27_sent > 0 and jan28_sent == 0:
        stopped_campaigns.append((cid, cdata["name"], cdata["status"], jan27_sent, cdata["total_interested"]))

stopped_campaigns.sort(key=lambda x: x[4], reverse=True)  # Sort by total interested
for cid, name, status, jan27_sent, total_int in stopped_campaigns[:15]:
    print(f"  Campaign {cid} ({status}): {jan27_sent} sent on Jan 27, total interested: {total_int} - {name[:40]}")

print("\n\nCampaigns that significantly reduced volume on Jan 28:")
reduced_campaigns = []
for cid, cdata in campaign_daily.items():
    jan27_sent = cdata["daily"].get("2025-01-27", {}).get("sent", 0)
    jan28_sent = cdata["daily"].get("2025-01-28", {}).get("sent", 0)
    
    if jan27_sent > 50 and jan28_sent > 0 and jan28_sent < jan27_sent * 0.5:
        reduction = jan27_sent - jan28_sent
        reduced_campaigns.append((cid, cdata["name"], cdata["status"], jan27_sent, jan28_sent, reduction, cdata["total_interested"]))

reduced_campaigns.sort(key=lambda x: x[5], reverse=True)  # Sort by reduction amount
for cid, name, status, jan27_sent, jan28_sent, reduction, total_int in reduced_campaigns[:10]:
    print(f"  Campaign {cid} ({status}): {jan27_sent}→{jan28_sent} (↓{reduction}), total interested: {total_int}")

# Flagged campaigns analysis
print("\n" + "=" * 80)
print("[5] FLAGGED CAMPAIGNS (328, 330) DETAILED ANALYSIS")
print("=" * 80)

for cid in ["328", "330"]:
    if cid in campaign_daily:
        cdata = campaign_daily[cid]
        stats = campaign_stats[cid]
        print(f"\nCampaign {cid}: {cdata['name']}")
        print(f"  Status: {cdata['status']}")
        print(f"  Total Sent: {stats['total_sent']}")
        print(f"  Total Replied: {stats.get('total_replied', 0)}")
        print(f"  Total Interested: {stats['total_interested']}")
        print(f"  Reply Rate: {(stats.get('total_replied', 0) / stats['total_sent'] * 100):.2f}%" if stats['total_sent'] > 0 else "N/A")
        print(f"  Interest Rate: {(stats['total_interested'] / stats['total_sent'] * 100):.3f}%" if stats['total_sent'] > 0 else "N/A")
        
        print(f"\n  Daily breakdown (Jan 19-29):")
        for date in dates_sorted:
            day = cdata["daily"].get(date, {})
            sent = day.get("sent", 0)
            replied = day.get("replied", 0)
            interested = day.get("interested", 0)
            if sent > 0 or replied > 0 or interested > 0:
                print(f"    {date}: sent={sent}, replied={replied}, interested={interested}")

# Campaign status analysis
print("\n" + "=" * 80)
print("[6] STATUS BREAKDOWN WITH PERFORMANCE")
print("=" * 80)

status_stats = defaultdict(lambda: {"count": 0, "sent": 0, "interested": 0, "replied": 0})
for cid, data in campaign_stats.items():
    status = data["status"]
    status_stats[status]["count"] += 1
    status_stats[status]["sent"] += data["total_sent"]
    status_stats[status]["interested"] += data["total_interested"]
    status_stats[status]["replied"] += data.get("total_replied", 0)

print(f"{'Status':<12} {'Count':>6} {'Sent':>10} {'Replied':>8} {'Interested':>10} {'Int Rate':>10}")
print("-" * 60)
for status in ["active", "launching", "completed", "paused", "queued", "archived", "draft"]:
    if status in status_stats:
        s = status_stats[status]
        rate = (s["interested"] / s["sent"] * 100) if s["sent"] > 0 else 0
        print(f"{status:<12} {s['count']:>6} {s['sent']:>10} {s['replied']:>8} {s['interested']:>10} {rate:>9.3f}%")

# Active campaigns detailed view
print("\n" + "=" * 80)
print("[7] ACTIVE CAMPAIGNS PERFORMANCE (Current Senders)")
print("=" * 80)

active_campaigns = [(cid, d) for cid, d in campaign_stats.items() if d["status"] == "active"]
active_campaigns.sort(key=lambda x: x[1]["total_interested"], reverse=True)

print(f"{'ID':<6} {'Sent':>8} {'Replied':>8} {'Interested':>10} {'Int Rate':>8} {'Name':<35}")
print("-" * 85)
for cid, data in active_campaigns:
    rate = (data["total_interested"] / data["total_sent"] * 100) if data["total_sent"] > 0 else 0
    print(f"{cid:<6} {data['total_sent']:>8} {data.get('total_replied',0):>8} {data['total_interested']:>10} {rate:>7.3f}% {data['name'][:35]}")

# Recommendations summary
print("\n" + "=" * 80)
print("[8] KEY FINDINGS & RECOMMENDATIONS")
print("=" * 80)

# Find best performing campaigns (interested rate)
high_performers = [(cid, d) for cid, d in campaign_stats.items() 
                  if d["total_sent"] > 5000 and d["total_interested"] > 5]
high_performers.sort(key=lambda x: x[1]["total_interested"]/x[1]["total_sent"], reverse=True)

print("\n🏆 TOP PERFORMING CAMPAIGNS (by interest rate, >5k sent):")
for cid, data in high_performers[:5]:
    rate = (data["total_interested"] / data["total_sent"] * 100)
    print(f"  Campaign {cid}: {rate:.3f}% interest rate ({data['total_interested']} interested) - {data['name'][:40]}")

print("\n⚠️  CAMPAIGNS NEEDING ATTENTION (flagged 328, 330):")
print("  Campaign 328: 0 interested from 9,734 sent (0.00% rate) - NEEDS COPY REFRESH")
print("  Campaign 330: 4 interested from 16,733 sent (0.024% rate) - UNDERPERFORMING")

print("\n📊 Volume Analysis:")
total_active_sent = sum(d["total_sent"] for _, d in active_campaigns)
total_active_interested = sum(d["total_interested"] for _, d in active_campaigns)
print(f"  Total from active campaigns: {total_active_sent:,} sent, {total_active_interested} interested")
print(f"  Overall interest rate (active): {(total_active_interested/total_active_sent*100):.3f}%")

# Save processed data
output = {
    "daily_totals": {k: dict(v) for k, v in daily_totals.items()},
    "top_campaigns": [(cid, name, status, sent, interested) for cid, name, status, sent, interested in top_campaigns],
    "active_campaigns": [(cid, data["name"], data["total_sent"], data["total_interested"]) for cid, data in active_campaigns],
    "status_breakdown": {k: dict(v) for k, v in status_stats.items()}
}

with open("/root/clawd/analysis/lts_processed_data.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n\nProcessed data saved to /root/clawd/analysis/lts_processed_data.json")
