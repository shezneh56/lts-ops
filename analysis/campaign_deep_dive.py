#!/usr/bin/env python3
"""
Campaign Deep Dive Analysis Script
Pulls data from all EmailBison workspaces and analyzes performance.
"""

import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Load workspace configuration
config_path = Path("/root/clawd/claude-code-projects/config/workspace_keys.json")
with open(config_path) as f:
    config = json.load(f)

# Workspaces to analyze (skip Wow24-7)
SKIP_WORKSPACES = ["Wow24-7"]

def get_client(workspace: Dict) -> httpx.Client:
    """Create HTTP client for a workspace."""
    return httpx.Client(
        timeout=60.0,
        headers={
            "Authorization": f"Bearer {workspace['api_key']}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

def list_all_campaigns(client: httpx.Client, base_url: str) -> List[Dict]:
    """Get all campaigns for a workspace with pagination."""
    all_campaigns = []
    page = 1
    
    while page <= 20:  # Safety limit
        try:
            response = client.get(f"{base_url}/campaigns", params={"page": page, "per_page": 50})
            response.raise_for_status()
            data = response.json()
            
            campaigns = data.get("data", []) if isinstance(data, dict) else data
            if not campaigns:
                break
                
            all_campaigns.extend(campaigns)
            
            if len(campaigns) < 50:
                break
            page += 1
        except Exception as e:
            print(f"  Error fetching campaigns page {page}: {e}")
            break
    
    return all_campaigns

def get_campaign_details(client: httpx.Client, base_url: str, campaign_id: int) -> Optional[Dict]:
    """Get detailed campaign stats."""
    try:
        response = client.get(f"{base_url}/campaigns/{campaign_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error fetching campaign {campaign_id}: {e}")
        return None

def get_sequence_steps(client: httpx.Client, base_url: str, campaign_id: int) -> List[Dict]:
    """Get sequence steps for a campaign."""
    try:
        response = client.get(f"{base_url}/campaigns/{campaign_id}/sequence-steps")
        response.raise_for_status()
        data = response.json()
        return data.get("data", []) if isinstance(data, dict) else data
    except Exception as e:
        print(f"  Error fetching steps for campaign {campaign_id}: {e}")
        return []

def main():
    """Main analysis function."""
    all_data = {
        "workspaces": {},
        "campaigns": [],
        "steps": [],
        "timestamp": datetime.now().isoformat()
    }
    
    for workspace in config["workspaces"]:
        if workspace["short_name"] in SKIP_WORKSPACES:
            print(f"Skipping {workspace['short_name']} (offboarded)")
            continue
            
        print(f"\n{'='*60}")
        print(f"Processing: {workspace['name']} ({workspace['short_name']})")
        print(f"{'='*60}")
        
        client = get_client(workspace)
        base_url = workspace["base_url"]
        
        workspace_data = {
            "name": workspace["name"],
            "short_name": workspace["short_name"],
            "campaigns": [],
            "totals": {
                "sent": 0,
                "replies": 0,
                "interested": 0,
                "bounced": 0,
                "opened": 0
            }
        }
        
        # Get all campaigns
        campaigns = list_all_campaigns(client, base_url)
        print(f"  Found {len(campaigns)} campaigns")
        
        for i, campaign in enumerate(campaigns):
            campaign_id = campaign.get("id")
            campaign_name = campaign.get("name", "Unnamed")
            
            print(f"  [{i+1}/{len(campaigns)}] Processing: {campaign_name[:50]}...")
            
            # Get detailed stats
            details = get_campaign_details(client, base_url, campaign_id)
            if not details:
                continue
            
            campaign_data = details.get("data", details)
            
            # Get sequence steps
            steps = get_sequence_steps(client, base_url, campaign_id)
            
            # Build campaign record
            campaign_record = {
                "workspace": workspace["short_name"],
                "workspace_name": workspace["name"],
                "id": campaign_id,
                "name": campaign_data.get("name", ""),
                "status": campaign_data.get("status", ""),
                "created_at": campaign_data.get("created_at", ""),
                "stats": {
                    "sent": campaign_data.get("emails_sent", 0),
                    "replies": campaign_data.get("replied", 0),
                    "unique_replies": campaign_data.get("unique_replies", 0),
                    "interested": campaign_data.get("interested", 0),
                    "bounced": campaign_data.get("bounced", 0),
                    "opened": campaign_data.get("opened", 0),
                    "unique_opens": campaign_data.get("unique_opens", 0),
                    "total_leads": campaign_data.get("total_leads_contacted", 0),
                    "unsubscribed": campaign_data.get("unsubscribed", 0),
                },
                "steps": []
            }
            
            # Calculate rates
            sent = campaign_record["stats"]["sent"]
            if sent > 0:
                campaign_record["stats"]["reply_rate"] = round(campaign_record["stats"]["replies"] / sent * 100, 2)
                campaign_record["stats"]["interested_rate"] = round(campaign_record["stats"]["interested"] / sent * 100, 2)
                campaign_record["stats"]["open_rate"] = round(campaign_record["stats"]["opened"] / sent * 100, 2)
                campaign_record["stats"]["bounce_rate"] = round(campaign_record["stats"]["bounced"] / sent * 100, 2)
            else:
                campaign_record["stats"]["reply_rate"] = 0
                campaign_record["stats"]["interested_rate"] = 0
                campaign_record["stats"]["open_rate"] = 0
                campaign_record["stats"]["bounce_rate"] = 0
            
            # Process steps
            for step in steps:
                step_record = {
                    "workspace": workspace["short_name"],
                    "campaign_id": campaign_id,
                    "campaign_name": campaign_data.get("name", ""),
                    "step_id": step.get("id"),
                    "step_number": step.get("order", step.get("step_number", 0)),
                    "subject": step.get("email_subject", step.get("subject", "")),
                    "body": step.get("email_body", step.get("body", "")),
                    "wait_days": step.get("wait_in_days", step.get("wait_days", 0)),
                    "variant": step.get("variant", False),
                    "thread_reply": step.get("thread_reply", False),
                    "stats": {
                        "sent": step.get("emails_sent", 0),
                        "opens": step.get("opened", step.get("opens", 0)),
                        "replies": step.get("replied", step.get("replies", 0)),
                        "interested": step.get("interested", 0),
                        "bounced": step.get("bounced", 0),
                    }
                }
                
                # Calculate step rates
                step_sent = step_record["stats"]["sent"]
                if step_sent > 0:
                    step_record["stats"]["reply_rate"] = round(step_record["stats"]["replies"] / step_sent * 100, 2)
                    step_record["stats"]["open_rate"] = round(step_record["stats"]["opens"] / step_sent * 100, 2)
                else:
                    step_record["stats"]["reply_rate"] = 0
                    step_record["stats"]["open_rate"] = 0
                
                campaign_record["steps"].append(step_record)
                all_data["steps"].append(step_record)
            
            # Update workspace totals
            workspace_data["totals"]["sent"] += campaign_record["stats"]["sent"]
            workspace_data["totals"]["replies"] += campaign_record["stats"]["replies"]
            workspace_data["totals"]["interested"] += campaign_record["stats"]["interested"]
            workspace_data["totals"]["bounced"] += campaign_record["stats"]["bounced"]
            workspace_data["totals"]["opened"] += campaign_record["stats"]["opened"]
            
            workspace_data["campaigns"].append(campaign_record)
            all_data["campaigns"].append(campaign_record)
        
        # Calculate workspace rates
        if workspace_data["totals"]["sent"] > 0:
            workspace_data["totals"]["reply_rate"] = round(workspace_data["totals"]["replies"] / workspace_data["totals"]["sent"] * 100, 2)
            workspace_data["totals"]["interested_rate"] = round(workspace_data["totals"]["interested"] / workspace_data["totals"]["sent"] * 100, 2)
        else:
            workspace_data["totals"]["reply_rate"] = 0
            workspace_data["totals"]["interested_rate"] = 0
        
        all_data["workspaces"][workspace["short_name"]] = workspace_data
        
        print(f"  Workspace totals: {workspace_data['totals']['sent']} sent, {workspace_data['totals']['replies']} replies ({workspace_data['totals']['reply_rate']}%)")
        
        client.close()
    
    # Save raw data
    output_path = Path("/root/clawd/analysis/campaign_data_raw.json")
    with open(output_path, "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print(f"\n\nData saved to {output_path}")
    print(f"Total campaigns: {len(all_data['campaigns'])}")
    print(f"Total steps: {len(all_data['steps'])}")
    
    return all_data

if __name__ == "__main__":
    main()
