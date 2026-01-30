#!/usr/bin/env python3
"""Create C2 Experience campaigns in EmailBison - v2 with correct variant linking."""
import json
import time
import httpx

API_KEY = "28|MObIGmIL27bR6CzDnxvarnWL5WfyUzp3Uj7PqdcJec05fb7f"
BASE_URL = "https://send.leadsthat.show/api"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# ============================================================================
# Campaign 1: Central Bank
# ============================================================================
CENTRAL_BANK = {
    "name": "C2 - Central Bank - Digital Leaders",
    "step1_main": {
        "subject": "{digital account opening|online account setup|new account flow} at {COMPANY}",
        "body": "<p>{FIRST_NAME}, what if {customers|people} at {COMPANY} could open an account online without {getting lost|dropping off|abandoning mid-flow}?</p><p><br></p><p>We {redesigned|rebuilt|streamlined} the {enrollment|onboarding|sign-up} journey for a 79,000-{user|person} organization and watched completion rates climb.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That organization {awarded|processed} over 10,000 {completions|conversions} last year - their site finally {keeps pace|keeps up} with demand.</p>",
    },
    "step1_variants": [
        {
            "subject": "{site navigation|product findability} question",
            "body": "<p>{FIRST_NAME}, can customers at {COMPANY} actually find {the right account|what they need|the product that fits} on your {website|site}?</p><p><br></p><p>We rebuilt {search and navigation|navigation and search|product discovery} for a major organization - made {350+ programs|hundreds of offerings} discoverable instead of buried.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. After {10 years|a decade} together, they still {trust us|rely on us} with their digital experience.</p>",
        },
        {
            "subject": "{accessibility and your site|digital accessibility|website accessibility}",
            "body": "<p>{FIRST_NAME}, how confident is {COMPANY} in your {website's|site's} accessibility compliance?</p><p><br></p><p>We made a {79,000-user|large} organization's site fully accessible - {content|pages}, navigation, {search|product finder}, everything.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. {Every|All} {2,000+|thousands of} {users|customers} who {rely on|use} assistive technology can now {navigate|browse} the site {easily|without friction}.</p>",
        },
        {
            "subject": "what {similar organizations|others in your space} did differently",
            "body": "<p>{FIRST_NAME}, a {79,000-user|large} organization across {350+ programs|multiple service lines} had a website that was {a maze|confusing|hard to navigate}.</p><p><br></p><p>We've spent {10 years|a decade} making it {work|seamless} - streamlined {enrollment|onboarding}, {relevant|accurate} search, accessible content.</p><p><br></p><p>Would {COMPANY} benefit from {a similar approach|the same treatment}?</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. They {processed|completed} over 10,000 {conversions|signups} in 2023. The site finally matches that {scale|volume}.</p>",
        },
        {
            "subject": "{quick question|question} about your digital experience",
            "body": "<p>{FIRST_NAME}, we just won Optimizely's 2024 Partner of the Year award for our {digital experience|UX|customer experience} work.</p><p><br></p><p>Our longest partnership? A {79,000-user|large} organization - {10+ years|over a decade} of making their digital experience actually serve {customers|users}.</p><p><br></p><p>Worth a conversation for {COMPANY}?</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That same organization went from {confusing site|fragmented experience} to streamlined {customer|user} journey.</p>",
        },
        {
            "subject": "{customers|visitors} dropping off your site",
            "body": "<p>{FIRST_NAME}, how many {prospective customers|visitors} give up on {COMPANY}'s website before they {find what they need|complete an application|open an account}?</p><p><br></p><p>We fixed this for an organization with {350+ offerings|hundreds of products} - made every {product|service|option} discoverable, every path clear.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. They've {processed|completed} over 10,000 {applications|conversions} annually since we streamlined their {customer|user} journey.</p>",
        },
        {
            "subject": "{your website working hard enough?|is your site pulling its weight?}",
            "body": "<p>{FIRST_NAME}, is {COMPANY}'s website actually helping customers {find the right product|open accounts|get answers} - or just getting in the way?</p><p><br></p><p>We've spent {a decade|10 years} making one organization's site do the heavy lifting: clear navigation, {relevant|accurate} search, accessible content.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That organization serves {79,000+ users|tens of thousands of customers}. Their site finally keeps up.</p>",
        },
    ],
    "step2": {
        "subject": "Re: {digital account opening|site navigation question|accessibility and your site|quick question about your digital experience}",
        "body": "<p>{FIRST_NAME}, {wanted to bump this up|circling back on this} in your inbox.</p><p><br></p><p>We've helped a {major|large} organization {grow|evolve} from a confusing site to a streamlined {customer|user} {journey|experience} machine - 10,000+ {completions|conversions} {processed|completed} last year.</p><p><br></p><p>If improving how customers find and {choose products|open accounts|navigate services} at {COMPANY} is on your radar, I'd {love|welcome} 15 minutes.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>",
        "wait_in_days": 3
    }
}

# ============================================================================
# Campaign 2: CCC Nebraska
# ============================================================================
CCC_NEBRASKA = {
    "name": "C2 - CCC Nebraska - Higher Ed Leaders",
    "step1_main": {
        "subject": "{student enrollment|enrollment experience|the enrollment journey} at {COMPANY}",
        "body": "<p>{FIRST_NAME}, what if {prospective students|future students|incoming students} at {COMPANY} could find their program and enroll without {getting lost in your site|struggling with navigation|hitting dead ends}?</p><p><br></p><p>We {redesigned|rebuilt|transformed} the enrollment journey for a {79,000-student college district|major community college system|large multi-campus district} and watched {completion rates climb|enrollment improve|conversion rates rise}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That district {awarded|granted|conferred} over 10,000 degrees last year - their site {finally keeps pace with demand|now matches their scale|actually supports that volume}.</p>",
    },
    "step1_variants": [
        {
            "subject": "{site navigation question|quick navigation question|finding programs on your site}",
            "body": "<p>{FIRST_NAME}, can students at {COMPANY} {actually find what they're looking for|easily discover programs|navigate to the right information} on your website?</p><p><br></p><p>We {rebuilt|redesigned|reworked} search and navigation for a {major college district|large community college system|79,000-student district} - made {350+ programs discoverable|hundreds of programs easy to find|every program accessible} instead of {buried|hidden|lost in menus}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. After {10 years together|a decade of partnership|10+ years}, they still {trust us with their digital experience|rely on us for their website|count on us for improvements}.</p>",
        },
        {
            "subject": "{accessibility and your site|website accessibility|accessibility compliance}",
            "body": "<p>{FIRST_NAME}, how confident is {COMPANY} in your website's {accessibility compliance|accessibility standards|ADA compliance}?</p><p><br></p><p>We made a {79,000-student district's site|major college's website|large community college's platform} {fully accessible|completely accessible|accessible end-to-end} - {content, navigation, search|every page, every feature|the whole experience}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. They {awarded|granted} 2,188 scholarships last year. Every one of those students could {navigate the site to apply|find and complete their applications|access what they needed}.</p>",
        },
        {
            "subject": "{6 locations, one website|multi-campus digital experience|serving students across Nebraska}",
            "body": "<p>{FIRST_NAME}, {COMPANY} serves students across {6 locations|multiple campuses|central Nebraska}. {Does your website feel unified - or fragmented?|Is the experience consistent everywhere?|Can every student find what they need?}</p><p><br></p><p>We've spent {10 years|a decade|10+ years} helping a {79,000-student district|large multi-campus college|major community college system} {deliver one seamless experience|unify their digital presence|make every campus feel connected}.</p><p><br></p><p>{Worth a conversation?|Would that approach help?|Interested in learning more?}</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That same district {went from confusing to streamlined|transformed their enrollment journey|now converts more prospective students than ever}.</p>",
        },
        {
            "subject": "{quick question about your digital experience|your website strategy|a question for you}",
            "body": "<p>{FIRST_NAME}, we {just won|recently received|were awarded} Optimizely's 2024 Partner of the Year {award|recognition} for our higher ed work.</p><p><br></p><p>Our {longest partnership|flagship client|signature relationship}? A {79,000-student college district|major community college system|large multi-campus district} - {10+ years of making their digital experience actually serve students|a decade of continuous improvement|10 years of measurable results}.</p><p><br></p><p>{Worth a conversation for {COMPANY}?|Would this approach fit {COMPANY}?|Could {COMPANY} benefit from similar work?}</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That district {went from confusing site to streamlined enrollment|now sees students complete enrollment faster|finally has a website that works as hard as their staff}.</p>",
        },
        {
            "subject": "{students dropping off your site|prospective students leaving|losing students at the website}",
            "body": "<p>{FIRST_NAME}, how many {prospective students|future Raiders|interested students} give up on {COMPANY}'s website before they {find what they need|complete enrollment|discover the right program}?</p><p><br></p><p>We {fixed this|solved this problem|addressed this} for a district with {350+ programs|hundreds of offerings|dozens of locations} - made {every program discoverable|every path clear|navigation intuitive}, {every path clear|every step obvious|friction disappear}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. They've {awarded|granted|conferred} over 10,000 degrees annually since we {streamlined their enrollment journey|rebuilt their site|fixed their user experience}.</p>",
        },
        {
            "subject": "{your website working hard enough?|is your site helping or hurting?|website as enrollment tool}",
            "body": "<p>{FIRST_NAME}, is {COMPANY}'s website {actually helping students enroll|supporting your enrollment goals|working for you} - or {just getting in the way|creating friction|making things harder}?</p><p><br></p><p>We've spent {a decade|10 years|10+ years} making one college district's site {do the heavy lifting|work harder|actually perform}: {clear navigation|intuitive menus|easy wayfinding}, {relevant search|smart search|search that works}, {accessible content|content everyone can use|full accessibility}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That district serves {79,000+ students|nearly 80,000 students|79K learners}. Their site {finally keeps up|now matches that scale|actually supports their mission}.</p>",
        },
    ],
    "step2": {
        "subject": "Re: {student enrollment|enrollment experience|the enrollment journey} at {COMPANY}",
        "body": "<p>{FIRST_NAME}, {wanted to bump this up in your inbox|circling back on this|following up}.</p><p><br></p><p>We've helped a {major college district|large community college system|79,000-student district} grow from a {confusing site|frustrating website|fragmented experience} to a {streamlined enrollment machine|conversion-focused platform|site that actually works} - {10,000+ degrees awarded last year|over 10K graduates annually|real measurable results}.</p><p><br></p><p>If {improving how students find and choose programs|streamlining enrollment|fixing your digital experience} at {COMPANY} is on your radar, {I'd love 15 minutes|let's find time to talk|happy to share what worked}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>",
        "wait_in_days": 3
    }
}

# ============================================================================
# Campaign 3: Certinia
# ============================================================================
CERTINIA = {
    "name": "C2 - Certinia - Digital Leaders",
    "step1_main": {
        "subject": "{finding the right solution|product navigation|site navigation question}",
        "body": "<p>{FIRST_NAME}, can prospects at {COMPANY} actually {find|discover|navigate to} the right {solution|product|cloud} for their {needs|business|situation}?</p><p><br></p><p>We {rebuilt|redesigned|overhauled} {product discovery|navigation|the buyer journey} for a {multi-product|complex|enterprise} portfolio - {made|helped} {hundreds of|350+} {offerings|solutions|options} {discoverable|findable|easy to explore} instead of {buried|hidden|overwhelming}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. {That client|They}'ve trusted us with their digital experience for {over a decade|10+ years}.</p>",
    },
    "step1_variants": [
        {
            "subject": "{your website|prospect journey at {COMPANY}|quick question}",
            "body": "<p>{FIRST_NAME}, what if enterprise prospects at {COMPANY} could {self-qualify|find their fit|navigate your solutions} without {getting lost|needing a sales call|confusion}?</p><p><br></p><p>We {streamlined|redesigned|optimized} the buyer journey for a {complex|multi-product} {organization|company} - {watch|saw} conversion rates {climb|improve|increase}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. {We just won|Recognized as} Optimizely's 2024 Partner of the Year for {work like this|our digital experience work|B2B impact}.</p>",
        },
        {
            "subject": "{customer portal|self-service question|customer experience}",
            "body": "<p>{FIRST_NAME}, how {easy|simple|intuitive} is it for {COMPANY}'s customers to {find answers|get help|navigate your portal} without {filing a ticket|calling support|waiting}?</p><p><br></p><p>We've {spent years|built expertise} {optimizing|improving|redesigning} {self-service experiences|customer portals|support journeys} for {enterprise|B2B|complex} {platforms|products}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. One {client|partner} saw their {support deflection|self-service adoption|portal engagement} {jump|improve significantly} after we {rebuilt|redesigned} their {customer experience|portal}.</p>",
        },
        {
            "subject": "{what|how} {other|similar} B2B SaaS {companies are|platforms} {doing|approaching this}",
            "body": "<p>{FIRST_NAME}, we work with {enterprise|B2B} {platforms|companies} that have {complex|multi-product} {portfolios|offerings} - {helping|making sure} {prospects|buyers|users} {find their fit|navigate|self-qualify} without {friction|confusion|overwhelm}.</p><p><br></p><p>{Would|Could} {COMPANY} benefit from a similar {approach|lens|perspective}?</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. Our longest {partnership|client relationship}? {Over|More than} {a decade|10 years} {helping|optimizing} their digital experience.</p>",
        },
        {
            "subject": "{quick question about|thoughts on} {your digital experience|{COMPANY}'s website}",
            "body": "<p>{FIRST_NAME}, we just won Optimizely's 2024 Partner of the Year award {for our|recognizing our} {enterprise|B2B} {digital experience work|web experience projects}.</p><p><br></p><p>Our {approach|specialty}? {Making|Helping} complex {product portfolios|solutions|offerings} {feel simple|easy to navigate|discoverable} to {prospects|buyers|visitors}.</p><p><br></p><p>{Worth a conversation|Open to a quick chat} about {COMPANY}?</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. {One|Our longest} {client|partnership} has trusted us for {10+ years|over a decade} - {from|through} {confusing site|complex legacy} to {streamlined|optimized} buyer journey.</p>",
        },
        {
            "subject": "{prospects|buyers} {dropping off|leaving} your site",
            "body": "<p>{FIRST_NAME}, how many {qualified|enterprise} prospects {give up|leave|drop off} on {COMPANY}'s {website|site} before they {find what they need|request a demo|engage}?</p><p><br></p><p>We {fixed this|solved this problem} for a {platform|company} with {hundreds of|350+} {offerings|products} across {multiple|several} {segments|verticals} - {made|helped} every {path|journey|option} {clear|discoverable|obvious}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. {They've|That company has} {seen|experienced} {thousands of|10K+} {conversions|completions} {since|after} we {streamlined|optimized} their {experience|journey}.</p>",
        },
        {
            "subject": "{is|your website} {working hard enough|pulling its weight}",
            "body": "<p>{FIRST_NAME}, is {COMPANY}'s {website|site} actually {helping|enabling} {prospects|buyers} {convert|engage|self-qualify} - or {just|mostly} getting in the way?</p><p><br></p><p>We've {spent|invested} {a decade|10+ years} {making|helping} one {enterprise|B2B} {company's|organization's} {site|digital experience} do the heavy lifting: {clear|intuitive} navigation, {relevant|smart} search, {accessible|compliant} content.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p><p><br></p><p>P.S. That {company|organization} serves {79K+|enterprise-scale} users. Their {site|digital experience} finally {keeps up|matches their scale}.</p>",
        },
    ],
    "step2": {
        "subject": "Re: {finding the right solution|product navigation|site navigation question}",
        "body": "<p>{FIRST_NAME}, wanted to {bump this up|follow up|bring this back} in your inbox.</p><p><br></p><p>We've helped {enterprise|B2B} {companies|platforms} with {complex|multi-product} portfolios {go from|transform} {confusing|overwhelming} {sites|experiences} to {streamlined|optimized} {buyer|customer} journeys.</p><p><br></p><p>If {improving|optimizing} how {prospects|buyers} {find and choose|navigate|discover} {solutions|products} at {COMPANY} is {on your radar|something you're thinking about}, I'd {love|welcome} {15 minutes|a quick chat}.</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>",
        "wait_in_days": 3
    }
}


def create_campaign(campaign_data: dict) -> dict:
    """Create a campaign with all steps using 2-step approach."""
    with httpx.Client(timeout=30.0, headers=headers) as client:
        print(f"\n{'='*60}")
        print(f"Creating campaign: {campaign_data['name']}")
        print(f"{'='*60}")
        
        # Step 1: Create campaign
        resp = client.post(f"{BASE_URL}/campaigns", json={"name": campaign_data['name']})
        resp.raise_for_status()
        campaign = resp.json()["data"]
        campaign_id = campaign["id"]
        print(f"  ✓ Created campaign ID: {campaign_id}")
        
        # Step 2: Create ONLY the main Step 1 first
        main_step = campaign_data["step1_main"]
        initial_payload = {
            "title": campaign_data["name"],
            "sequence_steps": [
                {
                    "email_subject": main_step["subject"],
                    "email_body": main_step["body"],
                    "order": 1,
                    "wait_in_days": 1,
                    "variant": False,
                    "thread_reply": False
                }
            ]
        }
        
        resp = client.post(
            f"{BASE_URL}/campaigns/v1.1/{campaign_id}/sequence-steps",
            json=initial_payload
        )
        resp.raise_for_status()
        seq_data = resp.json()["data"]
        sequence_id = seq_data["id"]
        main_step_id = seq_data["sequence_steps"][0]["id"]
        print(f"  ✓ Created sequence ID: {sequence_id}")
        print(f"  ✓ Created main Step 1: ID {main_step_id}")
        
        # Step 3: Build full step list with variants linked to main step
        all_steps = [
            {
                "id": main_step_id,
                "email_subject": main_step["subject"],
                "email_body": main_step["body"],
                "order": 1,
                "wait_in_days": 1,
                "variant": False,
                "thread_reply": False
            }
        ]
        
        # Add Step 1 variants (order 2-7)
        for i, var in enumerate(campaign_data["step1_variants"]):
            all_steps.append({
                "email_subject": var["subject"],
                "email_body": var["body"],
                "order": i + 2,
                "wait_in_days": 1,
                "variant": True,
                "variant_from_step_id": main_step_id,
                "thread_reply": False
            })
        
        # Add Step 2 (follow-up, order 8)
        step2 = campaign_data["step2"]
        all_steps.append({
            "email_subject": step2["subject"],
            "email_body": step2["body"],
            "order": 8,
            "wait_in_days": step2["wait_in_days"],
            "variant": False,
            "thread_reply": True
        })
        
        # Step 4: PUT to add all steps with correct variant linking
        full_payload = {
            "title": campaign_data["name"],
            "sequence_steps": all_steps
        }
        
        resp = client.put(
            f"{BASE_URL}/campaigns/v1.1/sequence-steps/{sequence_id}",
            json=full_payload
        )
        resp.raise_for_status()
        final_data = resp.json()["data"]
        
        steps = final_data["sequence_steps"]
        print(f"  ✓ Created {len(steps)} steps:")
        
        for step in sorted(steps, key=lambda x: x["order"]):
            variant_marker = " (A/B variant)" if step.get("variant") else ""
            thread_marker = " [thread reply]" if step.get("thread_reply") else ""
            parent = f" → links to {step.get('variant_from_step_id')}" if step.get("variant") else ""
            print(f"    - Order {step['order']}: ID {step['id']}{variant_marker}{thread_marker}{parent}")
        
        return {
            "campaign_id": campaign_id,
            "sequence_id": sequence_id,
            "name": campaign_data["name"],
            "steps": len(steps),
            "main_step_id": main_step_id,
            "step_ids": [s["id"] for s in steps]
        }


def main():
    """Create all 3 C2 campaigns."""
    print("\n" + "=" * 60)
    print("C2 EXPERIENCE - EMAILBISON CAMPAIGN CREATION v2")
    print("=" * 60)
    
    results = []
    
    for campaign in [CENTRAL_BANK, CCC_NEBRASKA, CERTINIA]:
        try:
            result = create_campaign(campaign)
            results.append(result)
            time.sleep(1)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append({"name": campaign["name"], "error": str(e)})
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    success_count = 0
    for r in results:
        if "error" in r:
            print(f"✗ {r['name']}: FAILED - {r['error']}")
        else:
            success_count += 1
            print(f"✓ {r['name']}")
            print(f"  Campaign ID: {r['campaign_id']}")
            print(f"  Sequence ID: {r['sequence_id']}")
            print(f"  Main Step ID: {r['main_step_id']}")
            print(f"  Total Steps: {r['steps']}")
    
    print(f"\n{success_count}/{len(results)} campaigns created successfully")
    
    # Save results to file
    return results


if __name__ == "__main__":
    results = main()
    
    # Save summary
    summary = {
        "workspace": "C2 Experience",
        "created_at": "2026-01-29",
        "campaigns": results
    }
    
    with open("/root/clawd/c2-campaigns-created.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to /root/clawd/c2-campaigns-created.json")
