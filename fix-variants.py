#!/usr/bin/env python3
"""Fix variant linking for C2 campaigns."""
import httpx

API_KEY = "28|MObIGmIL27bR6CzDnxvarnWL5WfyUzp3Uj7PqdcJec05fb7f"
BASE_URL = "https://send.leadsthat.show/api"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Campaign mappings: campaign_id -> (sequence_id, first_step_id)
CAMPAIGNS = {
    768: {"name": "C2 - Central Bank - Digital Leaders", "sequence_id": 662, "first_step_id": 4556},
    769: {"name": "C2 - CCC Nebraska - Higher Ed Leaders", "sequence_id": 663, "first_step_id": 4564},
    770: {"name": "C2 - Certinia - Digital Leaders", "sequence_id": 664, "first_step_id": 4572},
}

def fix_campaign(campaign_id: int, info: dict):
    """Fix variant linking for a campaign."""
    with httpx.Client(timeout=30.0, headers=headers) as client:
        print(f"\n{'='*60}")
        print(f"Fixing: {info['name']}")
        print(f"{'='*60}")
        
        # Get current steps
        resp = client.get(f"{BASE_URL}/campaigns/v1.1/{campaign_id}/sequence-steps")
        resp.raise_for_status()
        data = resp.json()["data"]
        
        current_steps = data["sequence_steps"]
        first_step_id = info["first_step_id"]
        
        # Build updated steps with correct variant linking
        updated_steps = []
        for step in current_steps:
            updated_step = {
                "id": step["id"],
                "email_subject": step["email_subject"],
                "email_body": step["email_body"],
                "order": step["order"],
                "wait_in_days": step["wait_in_days"],
                "variant": step.get("variant", False),
                "thread_reply": step.get("thread_reply", False),
            }
            
            # If it's a variant and not the main step or follow-up, link to first step
            if step.get("variant") and step["id"] != first_step_id:
                updated_step["variant_from_step_id"] = first_step_id
                print(f"  → Linking step {step['id']} (order {step['order']}) to main step {first_step_id}")
            
            updated_steps.append(updated_step)
        
        # PUT to update
        payload = {
            "title": info["name"],
            "sequence_steps": updated_steps
        }
        
        resp = client.put(
            f"{BASE_URL}/campaigns/v1.1/sequence-steps/{info['sequence_id']}",
            json=payload
        )
        
        if resp.status_code == 200:
            print(f"  ✓ Successfully updated")
            return True
        else:
            print(f"  ✗ Error: {resp.status_code}")
            print(f"    {resp.text[:500]}")
            return False


def main():
    """Fix all campaigns."""
    print("\n" + "=" * 60)
    print("FIXING VARIANT LINKING FOR C2 CAMPAIGNS")
    print("=" * 60)
    
    for campaign_id, info in CAMPAIGNS.items():
        try:
            fix_campaign(campaign_id, info)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")


if __name__ == "__main__":
    main()
