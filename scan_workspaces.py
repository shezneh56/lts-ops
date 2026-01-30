#!/usr/bin/env python3
"""Scan EmailBison workspaces for interested leads without meetings booked."""

import json
import re
import requests
import sys

# Flush print immediately
import functools
print = functools.partial(print, flush=True)

def get_api_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

def get_campaigns(base_url, headers):
    """Get all campaigns for a workspace."""
    url = f"{base_url}/campaigns"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("data", [])

def get_interested_replies(base_url, headers, campaign_id):
    """Get replies where interested=true for a campaign."""
    url = f"{base_url}/campaigns/{campaign_id}/replies"
    params = {"interested": "true", "per_page": 100}
    all_replies = []
    page = 1
    
    while True:
        params["page"] = page
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        replies = data.get("data", [])
        if not replies:
            break
        all_replies.extend(replies)
        if page >= data.get("meta", {}).get("last_page", 1):
            break
        page += 1
    
    return all_replies

def get_lead_details(base_url, headers, lead_id):
    """Get full lead details including tags."""
    url = f"{base_url}/leads/{lead_id}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json().get("data", {})

def extract_phone_from_text(text):
    """Try to extract phone number from reply text."""
    if not text:
        return ""
    # Common phone patterns
    patterns = [
        r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+\d{1,3}[-.\s]?\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return ""

def has_meeting_booked_tag(lead_data):
    """Check if lead has 'meeting booked' tag."""
    tags = lead_data.get("tags", [])
    for tag in tags:
        tag_name = tag.get("name", "").lower() if isinstance(tag, dict) else str(tag).lower()
        if "meeting" in tag_name and "booked" in tag_name:
            return True
    return False

def process_workspace(workspace_config, progress):
    """Process a single workspace and return new leads."""
    short_name = workspace_config["short_name"]
    api_key = workspace_config["api_key"]
    base_url = workspace_config["base_url"]
    
    print(f"\n{'='*60}")
    print(f"Processing workspace: {short_name}")
    print(f"{'='*60}")
    
    headers = get_api_headers(api_key)
    new_leads = []
    
    # Get all campaigns
    campaigns = get_campaigns(base_url, headers)
    print(f"Found {len(campaigns)} campaigns")
    
    for campaign in campaigns:
        campaign_id = campaign.get("id")
        campaign_name = campaign.get("name", "Unknown")
        print(f"\n  Campaign: {campaign_name} (ID: {campaign_id})")
        
        # Get interested replies
        replies = get_interested_replies(base_url, headers, campaign_id)
        print(f"  Found {len(replies)} interested replies")
        
        for reply in replies:
            lead_id = reply.get("lead_id")
            if not lead_id:
                continue
            
            # Get lead details
            lead = get_lead_details(base_url, headers, lead_id)
            if not lead:
                continue
            
            # Check for meeting booked tag
            meeting_booked = "Yes" if has_meeting_booked_tag(lead) else "No"
            
            # Get phone - try lead data first, then reply
            phone = lead.get("phone", "") or ""
            if not phone:
                reply_text = reply.get("body", "") or reply.get("text", "") or ""
                phone = extract_phone_from_text(reply_text)
            
            lead_record = {
                "workspace": short_name,
                "first_name": lead.get("first_name", ""),
                "last_name": lead.get("last_name", ""),
                "company": lead.get("company", ""),
                "email": lead.get("email", ""),
                "reply": reply.get("body", "") or reply.get("text", "") or "",
                "phone": phone,
                "campaign": campaign_name,
                "meeting_booked": meeting_booked,
                "status": ""
            }
            
            new_leads.append(lead_record)
            print(f"    + {lead.get('first_name', '')} {lead.get('last_name', '')} ({lead.get('email', '')}) - Meeting: {meeting_booked}")
    
    return new_leads

def main():
    # Load workspace keys
    with open("/root/clawd/claude-code-projects/config/workspace_keys.json") as f:
        config = json.load(f)
    
    # Load progress
    progress_file = "/root/clawd/workspace_scan_progress.json"
    with open(progress_file) as f:
        progress = json.load(f)
    
    completed = set(progress.get("completed", []))
    
    # Workspaces to skip
    skip = {"C2", "Wow24-7"}
    
    # Process workspaces to scan
    workspaces_to_scan = ["CGS", "Gestell", "Hygraph", "Jampot", "Lawtech", "Legalsoft", "LTS", "Medvirtual", "Paralect"]
    
    # Filter by command line arg if provided
    if len(sys.argv) > 1:
        workspaces_to_scan = [sys.argv[1]]
    
    for ws_name in workspaces_to_scan:
        if ws_name in completed or ws_name in skip:
            print(f"Skipping {ws_name} (already done or skipped)")
            continue
        
        # Find workspace config
        ws_config = None
        for ws in config["workspaces"]:
            if ws["short_name"] == ws_name:
                ws_config = ws
                break
        
        if not ws_config:
            print(f"Workspace {ws_name} not found in config")
            continue
        
        try:
            new_leads = process_workspace(ws_config, progress)
            
            # Add to progress
            progress["results"].extend(new_leads)
            progress["completed"].append(ws_name)
            
            # Save progress after each workspace
            with open(progress_file, "w") as f:
                json.dump(progress, f, indent=2)
            
            print(f"\nSaved {len(new_leads)} leads from {ws_name}")
            
        except Exception as e:
            print(f"Error processing {ws_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total leads: {len(progress['results'])}")
    print(f"Completed workspaces: {progress['completed']}")
    
    # Count not booked
    not_booked = [r for r in progress["results"] if r.get("meeting_booked") == "No"]
    print(f"Leads without meeting booked: {len(not_booked)}")

if __name__ == "__main__":
    main()
