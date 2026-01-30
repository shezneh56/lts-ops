#!/usr/bin/env python3
"""
Deploy all 15 Hygraph campaigns to EmailBison.
V2: Creates steps one at a time to handle variant_from_step_id correctly.

Campaign structure:
- Step 1 variations: order=1, wait_in_days=1, variant=False for first, variant=True for rest
- Step 2 follow-up: order=2, wait_in_days=3, thread_reply=True, variant=False

Naming: "HYG New ICP - [Industry] - [Persona]"
"""

import sys
import os
import json
import re
import httpx

# Set config path
os.environ['EMAILBISON_CONFIG'] = '/root/clawd/claude-code-projects/config/workspace_keys.json'

WORKSPACE = "Hygraph"

# Load API config
with open('/root/clawd/claude-code-projects/config/workspace_keys.json') as f:
    config = json.load(f)
    ws = next(w for w in config['workspaces'] if w['short_name'] == WORKSPACE)
    API_KEY = ws['api_key']
    BASE_URL = ws['base_url']

# Campaign definitions
CAMPAIGNS = {
    1: {"id": "D2C-ENG", "name": "HYG New ICP - D2C Ecommerce - Engineering", "source": "original", "variations": ["C"]},
    2: {"id": "D2C-PROD", "name": "HYG New ICP - D2C Ecommerce - Product", "source": "original", "variations": ["B"]},
    3: {"id": "D2C-EXEC", "name": "HYG New ICP - D2C Ecommerce - Executive", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    4: {"id": "MFG-ENG", "name": "HYG New ICP - Manufacturing - Engineering", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    5: {"id": "MFG-PROD", "name": "HYG New ICP - Manufacturing - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    6: {"id": "MFG-EXEC", "name": "HYG New ICP - Manufacturing - Executive", "source": "original", "variations": ["A", "B"]},
    7: {"id": "GAME-ENG", "name": "HYG New ICP - Gaming - Engineering", "source": "original", "variations": ["B"]},
    8: {"id": "GAME-PROD", "name": "HYG New ICP - Gaming - Product", "source": "original", "variations": ["A", "B"]},
    9: {"id": "GAME-EXEC", "name": "HYG New ICP - Gaming - Executive", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    10: {"id": "HOSP-ENG", "name": "HYG New ICP - Hospitality - Engineering", "source": "original", "variations": ["B"]},
    11: {"id": "HOSP-PROD", "name": "HYG New ICP - Hospitality - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    12: {"id": "HOSP-EXEC", "name": "HYG New ICP - Hospitality - Executive", "source": "original", "variations": ["A"]},
    13: {"id": "ENT-ENG", "name": "HYG New ICP - Entertainment - Engineering", "source": "original", "variations": ["A", "B"]},
    14: {"id": "ENT-PROD", "name": "HYG New ICP - Entertainment - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    15: {"id": "ENT-EXEC", "name": "HYG New ICP - Entertainment - Executive", "source": "original", "variations": ["A", "B"]},
}


def text_to_html(text: str) -> str:
    """Convert plain text to HTML paragraph format."""
    lines = text.strip().split('\n')
    html_parts = []
    for line in lines:
        if line.strip():
            html_parts.append(f"<p>{line.strip()}</p>")
        else:
            html_parts.append("<p><br></p>")
    return "".join(html_parts)


def parse_original_campaign(content: str, campaign_num: int, campaign_id: str, variations: list) -> dict:
    """Parse campaign from original markdown file."""
    pattern = rf"## Campaign {campaign_num}:.*?{campaign_id}\)"
    start_match = re.search(pattern, content, re.IGNORECASE)
    if not start_match:
        raise ValueError(f"Campaign {campaign_num} ({campaign_id}) not found")
    
    start_idx = start_match.start()
    next_campaign = re.search(r"\n## Campaign \d+:", content[start_idx + 1:])
    end_idx = start_idx + 1 + next_campaign.start() if next_campaign else len(content)
    section = content[start_idx:end_idx]
    
    result = {"variations": {}, "followup": None}
    
    for var in ["A", "B", "C"]:
        if var not in variations:
            continue
        var_pattern = rf"### Step 1 - Variation {var}.*?\n\*\*Subject:\*\* (.+?)\n\n(.+?)(?=\n### Step|---|\Z)"
        var_match = re.search(var_pattern, section, re.DOTALL)
        if var_match:
            subject = var_match.group(1).strip()
            body = re.sub(r'\n---$', '', var_match.group(2).strip())
            result["variations"][var] = {"subject": subject, "body": body}
    
    followup_pattern = r"### Step 2 - Follow-up\n\*\*Subject:\*\* (.+?)\n\n(.+?)(?=\n## Campaign|\Z)"
    followup_match = re.search(followup_pattern, section, re.DOTALL)
    if followup_match:
        result["followup"] = {
            "subject": followup_match.group(1).strip(),
            "body": re.sub(r'\n---$', '', followup_match.group(2).strip())
        }
    
    return result


def parse_revised_campaign(content: str, campaign_num: int, campaign_id: str) -> dict:
    """Parse campaign from revised markdown file."""
    pattern = rf"## Campaign {campaign_num}:.*?{campaign_id}.*?Revised\)"
    start_match = re.search(pattern, content, re.IGNORECASE)
    if not start_match:
        raise ValueError(f"Campaign {campaign_num} ({campaign_id}) not found in revised file")
    
    start_idx = start_match.start()
    next_campaign = re.search(r"\n## Campaign \d+:", content[start_idx + 1:])
    end_idx = start_idx + 1 + next_campaign.start() if next_campaign else len(content)
    section = content[start_idx:end_idx]
    
    result = {"variations": {}}
    
    for var in ["A", "B", "C", "D", "E"]:
        var_pattern = rf"### Step 1 - Variation {var}\nSubject: (.+?)\n\n(.+?)(?=\n### Step 1 - Variation|\n---|\Z)"
        var_match = re.search(var_pattern, section, re.DOTALL)
        if var_match:
            subject = var_match.group(1).strip()
            body = re.sub(r'\n---$', '', var_match.group(2).strip())
            result["variations"][var] = {"subject": subject, "body": body}
    
    return result


class EmailBisonClient:
    def __init__(self):
        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    def create_campaign(self, name: str) -> int:
        """Create a campaign and return its ID."""
        resp = self.client.post(f"{BASE_URL}/campaigns", json={"name": name})
        if resp.status_code not in [200, 201]:
            raise Exception(f"Failed to create campaign: {resp.text}")
        data = resp.json()
        return data.get("data", {}).get("id") or data.get("id")
    
    def add_step(self, campaign_id: int, campaign_name: str, step_data: dict) -> int:
        """Add a single step to a campaign and return its ID."""
        # Convert body to HTML if needed
        body = step_data.get("email_body", "")
        if body and not body.strip().startswith("<p>"):
            step_data["email_body"] = text_to_html(body)
        
        payload = {
            "title": campaign_name,
            "sequence_steps": [step_data]
        }
        
        resp = self.client.post(f"{BASE_URL}/campaigns/v1.1/{campaign_id}/sequence-steps", json=payload)
        if resp.status_code not in [200, 201]:
            raise Exception(f"Failed to add step: {resp.text}")
        
        result_data = resp.json().get("data", {})
        steps = result_data.get("sequence_steps", [])
        return steps[-1].get("id") if steps else None
    
    def close(self):
        self.client.close()


def deploy_campaign(client: EmailBisonClient, campaign_num: int, config: dict, original_content: str, revised_content: str, confirm: bool = False):
    """Deploy a single campaign with steps created one at a time."""
    print(f"\n{'='*60}")
    print(f"Campaign {campaign_num}: {config['id']} - {config['name']}")
    print(f"Source: {config['source']}, Variations: {config['variations']}")
    print(f"{'='*60}")
    
    try:
        # Parse campaign content
        if config["source"] == "original":
            campaign_data = parse_original_campaign(original_content, campaign_num, config["id"], config["variations"])
            followup = campaign_data.get("followup")
        else:
            campaign_data = parse_revised_campaign(revised_content, campaign_num, config["id"])
            original_data = parse_original_campaign(original_content, campaign_num, config["id"], ["A"])
            followup = original_data.get("followup")
        
        variations = list(campaign_data["variations"].items())
        total_steps = len(variations) + (1 if followup else 0)
        
        print(f"Steps to create: {total_steps}")
        for i, (var_name, var_data) in enumerate(variations):
            var_info = "(variant)" if i > 0 else "(primary)"
            print(f"  Var {var_name}: subject='{var_data['subject'][:40]}...' {var_info}")
        if followup:
            print(f"  Follow-up: subject='{followup['subject'][:40]}...'")
        
        if not confirm:
            return {"success": True, "dry_run": True, "steps": total_steps}
        
        # Create campaign
        campaign_id = client.create_campaign(config["name"])
        print(f"  Created campaign ID: {campaign_id}")
        
        step_ids = []
        first_step_id = None
        
        # Add first variation (primary step)
        if variations:
            first_var_name, first_var = variations[0]
            first_step_id = client.add_step(campaign_id, config["name"], {
                "email_subject": first_var["subject"],
                "email_body": first_var["body"],
                "order": 1,
                "wait_in_days": 1,
                "variant": False,
                "thread_reply": False
            })
            step_ids.append(first_step_id)
            print(f"  Added primary step {first_var_name}: ID {first_step_id}")
        
        # Add remaining variations
        for var_name, var_data in variations[1:]:
            step_id = client.add_step(campaign_id, config["name"], {
                "email_subject": var_data["subject"],
                "email_body": var_data["body"],
                "order": 1,
                "wait_in_days": 1,
                "variant": True,
                "variant_from_step_id": first_step_id,
                "thread_reply": False
            })
            step_ids.append(step_id)
            print(f"  Added variant {var_name}: ID {step_id}")
        
        # Add follow-up
        if followup:
            followup_id = client.add_step(campaign_id, config["name"], {
                "email_subject": followup["subject"],
                "email_body": followup["body"],
                "order": 2,
                "wait_in_days": 3,
                "variant": False,
                "thread_reply": True
            })
            step_ids.append(followup_id)
            print(f"  Added follow-up: ID {followup_id}")
        
        print(f"✅ SUCCESS: Campaign {campaign_id} with {len(step_ids)} steps")
        return {"success": True, "campaign_id": campaign_id, "steps": len(step_ids), "step_ids": step_ids}
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", action="store_true", help="Actually create campaigns")
    parser.add_argument("--campaign", type=int, help="Deploy specific campaign number only")
    parser.add_argument("--start-from", type=int, help="Start from campaign number")
    args = parser.parse_args()
    
    # Load source files
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/15-campaign-matrix-FINAL.md", "r") as f:
        original_content = f.read()
    
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/REVISED-6-CAMPAIGNS.md", "r") as f:
        revised_content = f.read()
    
    client = EmailBisonClient()
    results = []
    
    if args.campaign:
        campaigns_to_deploy = [args.campaign]
    elif args.start_from:
        campaigns_to_deploy = [n for n in CAMPAIGNS.keys() if n >= args.start_from]
    else:
        campaigns_to_deploy = list(CAMPAIGNS.keys())
    
    try:
        for campaign_num in campaigns_to_deploy:
            config = CAMPAIGNS[campaign_num]
            result = deploy_campaign(
                client, campaign_num, config,
                original_content, revised_content,
                confirm=args.confirm
            )
            result["campaign_num"] = campaign_num
            result["name"] = config["name"]
            results.append(result)
    finally:
        client.close()
    
    # Summary
    print("\n" + "="*60)
    print("DEPLOYMENT SUMMARY")
    print("="*60)
    
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"\nSuccessful: {len(successful)}/{len(results)}")
    for r in successful:
        if r.get("dry_run"):
            print(f"  Campaign {r['campaign_num']}: {r['name']} - DRY RUN ({r['steps']} steps)")
        else:
            print(f"  Campaign {r['campaign_num']}: {r['name']} - ID: {r.get('campaign_id')} ({r['steps']} steps)")
    
    if failed:
        print(f"\nFailed: {len(failed)}")
        for r in failed:
            print(f"  Campaign {r['campaign_num']}: {r['name']} - {r.get('error')}")
    
    # Save results
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/deployment_results_v2.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to deployment_results_v2.json")
    
    return results


if __name__ == "__main__":
    main()
