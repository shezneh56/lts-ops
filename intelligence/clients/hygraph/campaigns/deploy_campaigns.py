#!/usr/bin/env python3
"""
Deploy all 15 Hygraph campaigns to EmailBison.

Campaign structure:
- Step 1 variations: order=1, wait_in_days=1, variant=False for first, variant=True for rest
- Step 2 follow-up: order=2, wait_in_days=3, thread_reply=True, variant=False

Naming: "HYG New ICP - [Industry] - [Persona]"
"""

import sys
import os
import json
import re

# Add MCP server to path
sys.path.insert(0, '/root/clawd/claude-code-projects/mcp-emailbison/src')
os.environ['EMAILBISON_CONFIG'] = '/root/clawd/claude-code-projects/config/workspace_keys.json'

import asyncio
from server import create_full_sequence

WORKSPACE = "Hygraph"

# Campaign definitions
CAMPAIGNS = {
    # Original campaigns (from 15-campaign-matrix-FINAL.md)
    1: {"id": "D2C-ENG", "name": "HYG New ICP - D2C Ecommerce - Engineering", "source": "original", "variations": ["C"]},  # Only C passes
    2: {"id": "D2C-PROD", "name": "HYG New ICP - D2C Ecommerce - Product", "source": "original", "variations": ["B"]},  # Only B passes
    3: {"id": "D2C-EXEC", "name": "HYG New ICP - D2C Ecommerce - Executive", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    4: {"id": "MFG-ENG", "name": "HYG New ICP - Manufacturing - Engineering", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    5: {"id": "MFG-PROD", "name": "HYG New ICP - Manufacturing - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    6: {"id": "MFG-EXEC", "name": "HYG New ICP - Manufacturing - Executive", "source": "original", "variations": ["A", "B"]},  # Both pass
    7: {"id": "GAME-ENG", "name": "HYG New ICP - Gaming - Engineering", "source": "original", "variations": ["B"]},  # Only B passes
    8: {"id": "GAME-PROD", "name": "HYG New ICP - Gaming - Product", "source": "original", "variations": ["A", "B"]},  # Both pass
    9: {"id": "GAME-EXEC", "name": "HYG New ICP - Gaming - Executive", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    10: {"id": "HOSP-ENG", "name": "HYG New ICP - Hospitality - Engineering", "source": "original", "variations": ["B"]},  # Only B passes
    11: {"id": "HOSP-PROD", "name": "HYG New ICP - Hospitality - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    12: {"id": "HOSP-EXEC", "name": "HYG New ICP - Hospitality - Executive", "source": "original", "variations": ["A"]},  # Only A passes
    13: {"id": "ENT-ENG", "name": "HYG New ICP - Entertainment - Engineering", "source": "original", "variations": ["A", "B"]},  # Both pass
    14: {"id": "ENT-PROD", "name": "HYG New ICP - Entertainment - Product", "source": "revised", "variations": ["A", "B", "C", "D", "E"]},
    15: {"id": "ENT-EXEC", "name": "HYG New ICP - Entertainment - Executive", "source": "original", "variations": ["A", "B"]},  # Both pass
}


def parse_original_campaign(content: str, campaign_num: int, campaign_id: str, variations: list) -> dict:
    """Parse campaign from original markdown file."""
    # Find the campaign section
    pattern = rf"## Campaign {campaign_num}:.*?{campaign_id}\)"
    start_match = re.search(pattern, content, re.IGNORECASE)
    if not start_match:
        raise ValueError(f"Campaign {campaign_num} ({campaign_id}) not found in original file")
    
    start_idx = start_match.start()
    
    # Find next campaign section or end
    next_campaign = re.search(r"\n## Campaign \d+:", content[start_idx + 1:])
    if next_campaign:
        end_idx = start_idx + 1 + next_campaign.start()
    else:
        end_idx = len(content)
    
    section = content[start_idx:end_idx]
    
    result = {"variations": {}, "followup": None}
    
    # Parse each variation
    for var in ["A", "B", "C"]:
        if var not in variations:
            continue
        
        # Find variation section
        var_pattern = rf"### Step 1 - Variation {var}.*?\n\*\*Subject:\*\* (.+?)\n\n(.+?)(?=\n### Step|---|\Z)"
        var_match = re.search(var_pattern, section, re.DOTALL)
        if var_match:
            subject = var_match.group(1).strip()
            body = var_match.group(2).strip()
            
            # Clean up body - remove trailing ---
            body = re.sub(r'\n---$', '', body.strip())
            
            result["variations"][var] = {
                "subject": subject,
                "body": body
            }
    
    # Parse follow-up
    followup_pattern = r"### Step 2 - Follow-up\n\*\*Subject:\*\* (.+?)\n\n(.+?)(?=\n## Campaign|\Z)"
    followup_match = re.search(followup_pattern, section, re.DOTALL)
    if followup_match:
        result["followup"] = {
            "subject": followup_match.group(1).strip(),
            "body": followup_match.group(2).strip()
        }
        # Clean up followup body
        result["followup"]["body"] = re.sub(r'\n---$', '', result["followup"]["body"].strip())
    
    return result


def parse_revised_campaign(content: str, campaign_num: int, campaign_id: str) -> dict:
    """Parse campaign from revised markdown file."""
    # Find the campaign section
    pattern = rf"## Campaign {campaign_num}:.*?{campaign_id}.*?Revised\)"
    start_match = re.search(pattern, content, re.IGNORECASE)
    if not start_match:
        raise ValueError(f"Campaign {campaign_num} ({campaign_id}) not found in revised file")
    
    start_idx = start_match.start()
    
    # Find next campaign section or end
    next_campaign = re.search(r"\n## Campaign \d+:", content[start_idx + 1:])
    if next_campaign:
        end_idx = start_idx + 1 + next_campaign.start()
    else:
        end_idx = len(content)
    
    section = content[start_idx:end_idx]
    
    result = {"variations": {}}
    
    # Parse each variation (A through E)
    for var in ["A", "B", "C", "D", "E"]:
        var_pattern = rf"### Step 1 - Variation {var}\nSubject: (.+?)\n\n(.+?)(?=\n### Step 1 - Variation|\n---|\Z)"
        var_match = re.search(var_pattern, section, re.DOTALL)
        if var_match:
            subject = var_match.group(1).strip()
            body = var_match.group(2).strip()
            body = re.sub(r'\n---$', '', body.strip())
            
            result["variations"][var] = {
                "subject": subject,
                "body": body
            }
    
    return result


def build_steps(campaign_data: dict, followup_from_original: dict = None) -> list:
    """Build steps array for EmailBison create_full_sequence."""
    steps = []
    
    variations = list(campaign_data["variations"].items())
    
    # First variation - not a variant
    if variations:
        first_var_name, first_var = variations[0]
        steps.append({
            "email_subject": first_var["subject"],
            "email_body": first_var["body"],
            "order": 1,
            "wait_in_days": 1,
            "variant": False,
            "thread_reply": False
        })
        
        # Remaining variations - are variants
        for var_name, var_data in variations[1:]:
            steps.append({
                "email_subject": var_data["subject"],
                "email_body": var_data["body"],
                "order": 1,
                "wait_in_days": 1,
                "variant": True,
                "variant_from_step": 1,
                "thread_reply": False
            })
    
    # Add follow-up if available
    followup = campaign_data.get("followup") or followup_from_original
    if followup:
        steps.append({
            "email_subject": followup["subject"],
            "email_body": followup["body"],
            "order": 2,
            "wait_in_days": 3,
            "variant": False,
            "thread_reply": True
        })
    
    return steps


async def deploy_campaign(campaign_num: int, config: dict, original_content: str, revised_content: str, confirm: bool = False):
    """Deploy a single campaign."""
    print(f"\n{'='*60}")
    print(f"Campaign {campaign_num}: {config['id']} - {config['name']}")
    print(f"Source: {config['source']}, Variations: {config['variations']}")
    print(f"{'='*60}")
    
    try:
        if config["source"] == "original":
            campaign_data = parse_original_campaign(
                original_content, 
                campaign_num, 
                config["id"], 
                config["variations"]
            )
            followup = campaign_data.get("followup")
        else:
            # Revised campaigns need follow-up from original
            campaign_data = parse_revised_campaign(
                revised_content,
                campaign_num,
                config["id"]
            )
            # Get follow-up from original file
            original_data = parse_original_campaign(
                original_content,
                campaign_num,
                config["id"],
                ["A"]  # Just need to parse enough to get followup
            )
            followup = original_data.get("followup")
        
        # Build steps
        steps = build_steps(campaign_data, followup)
        
        print(f"Steps to create: {len(steps)}")
        for i, step in enumerate(steps):
            var_info = f"(variant of step 1)" if step.get("variant") else ""
            thread_info = "(thread reply)" if step.get("thread_reply") else ""
            print(f"  Step {i+1}: order={step['order']}, subject='{step['email_subject'][:50]}...' {var_info} {thread_info}")
        
        # Create campaign
        result = await create_full_sequence(
            name=config["name"],
            steps=steps,
            workspace=WORKSPACE,
            confirm=confirm
        )
        
        if result.get("success"):
            print(f"✅ SUCCESS: Campaign ID {result['campaign_id']}, {result['steps_created']} steps created")
            return {"success": True, "campaign_id": result["campaign_id"], "steps": result["steps_created"]}
        elif result.get("dry_run"):
            print(f"🔄 DRY RUN: Would create {result['step_count']} steps")
            return {"success": True, "dry_run": True, "steps": result["step_count"]}
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return {"success": False, "error": result.get("error")}
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


async def main():
    """Deploy all 15 campaigns."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", action="store_true", help="Actually create campaigns (not dry-run)")
    parser.add_argument("--campaign", type=int, help="Deploy specific campaign number only")
    args = parser.parse_args()
    
    # Load source files
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/15-campaign-matrix-FINAL.md", "r") as f:
        original_content = f.read()
    
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/REVISED-6-CAMPAIGNS.md", "r") as f:
        revised_content = f.read()
    
    results = []
    campaigns_to_deploy = [args.campaign] if args.campaign else list(CAMPAIGNS.keys())
    
    for campaign_num in campaigns_to_deploy:
        config = CAMPAIGNS[campaign_num]
        result = await deploy_campaign(
            campaign_num,
            config,
            original_content,
            revised_content,
            confirm=args.confirm
        )
        result["campaign_num"] = campaign_num
        result["name"] = config["name"]
        results.append(result)
    
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
    with open("/root/clawd/intelligence/clients/hygraph/campaigns/deployment_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to deployment_results.json")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
