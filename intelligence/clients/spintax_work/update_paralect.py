#!/usr/bin/env python3
"""
Update Paralect campaigns with spintax versions
"""
import requests
import json

API_KEY = "37|piFvS64k4ynhA1KGtlvb8ODPW6uqL0GuuPbdE1OA29a41ea3"
BASE_URL = "https://send.leadsthat.show/api"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Spintax versions for Campaign 514 (Early Stage)
UPDATES_514 = {
    3288: {
        "email_body": "<p>{Hi|Hey|Hello} {FIRST_NAME}, Premedgo {came to us with|approached us with|brought us} an idea and we {built|developed|created} their {entire|complete|full} MVP (web app, mobile app, and admin panel) in {2 months|about 8 weeks|under 3 months}.</p><p><br></p><p>We put together a pre-build checklist based on launches like this. {Want me to send it?|Mind if I send it over?|Should I share it?}</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>"
    },
    3289: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, hiring devs {takes|requires|needs} 3-6 months and costs 150K+ per hire. {Most|Many|A lot of} early-stage founders can't afford that.<br><br>We gave Premedgo a full product team and shipped their MVP in 2 months for a fraction of the cost.<br><br>{Worth discussing how we'd approach {COMPANY}'s build?|Interested in seeing how we'd approach {COMPANY}'s build?|Makes sense to discuss {COMPANY}'s roadmap?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3290: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, TernWheel {came to us with|approached us with|brought us} an idea and we built their MVP in 3 months. They're {since|now} backed by a16z.<br><br>If {COMPANY} is targeting tier-1 investors, {worth discussing how we'd approach your product?|interested in seeing how we'd approach your product?|makes sense to chat about your product?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3291: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, the {fastest|quickest|most efficient} way to validate your idea is to ship an MVP and test it with real users.<br><br>We helped Grid Discovery go from idea to live MVP in 3 months. They raised 300K {right after|shortly after|following} launch.<br><br>{Worth 15 minutes to discuss {COMPANY}'s validation plan?|Makes sense to chat about {COMPANY}'s approach?|Interested in a brief conversation about {COMPANY}'s plan?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3292: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {most|many|a lot of} founders sit on their idea for 6+ months because they can't code or can't afford to hire a full team.<br><br>We built Premedgo's full MVP in 2 months. Grid Discovery raised 300K in 3 months. TernWheel (backed by a16z) shipped in 3 months.<br><br>If {COMPANY} is ready to move, {worth discussing how we'd approach your build?|interested in seeing how we'd approach your build?|makes sense to chat about your build?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3293: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {circling back|following up|checking in} - any interest in discussing your MVP timeline?<br><br>We can typically ship in 2-3 months.<br><br>{SENDER_EMAIL_SIGNATURE}"
    }
}

# Spintax versions for Campaign 515 (Mature Startups)
UPDATES_515 = {
    3294: {
        "email_body": "<p>{Hi|Hey|Hello} {FIRST_NAME}, {most|many|a lot of} founders in your position have 6-12 months of runway left and their team is missing deadlines.</p><p><br></p><p>VeroSkills was in the same spot. We replaced their team, shipped a working product, and they hit 700K ARR in 4 months. They raised 5.3M.</p><p><br></p><p>Put together a recovery playbook for teams in this situation. {Want me to send it?|Mind if I send it over?|Should I share it?}</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>"
    },
    3295: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, VeroSkills came to us with a stalled product and hit 700K ARR within 4 months of working with us. They raised 5.3M.<br><br>If {COMPANY} needs similar revenue traction, {worth a 15-minute conversation to see if we can help?|makes sense to chat about how we can help?|interested in discussing how we'd approach this?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3296: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {most|many} investors want to see product traction before they write checks.<br><br>VeroSkills shipped their product with us, hit 700K ARR in 4 months, and raised 5.3M. LightHouse raised 8M post-build.<br><br>{Worth discussing how we'd help {COMPANY} become investor-ready?|Makes sense to chat about {COMPANY}'s path to investor-readiness?|Interested in discussing {COMPANY}'s approach?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3297: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {most|many} MVPs aren't built to scale. They work for early traction but break at 10K+ users.<br><br>LightHouse had this exact issue. We rebuilt their product for scale and they grew 10x. They raised 8M seed round.<br><br>{Worth discussing how we'd help {COMPANY} scale?|Makes sense to chat about {COMPANY}'s scaling needs?|Interested in exploring this for {COMPANY}?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3298: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {most|many} founders who've been burned by contractors are hesitant to try again.<br><br>VeroSkills came to us after their previous team wasted 6 months and burned budget. We replaced them, shipped a working product, and they hit 700K ARR in 4 months.<br><br>{Worth discussing how we'd approach {COMPANY}'s situation?|Makes sense to chat about {COMPANY}'s needs?|Interested in seeing how we'd help {COMPANY}?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3299: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {circling back|following up|checking in} - any interest in discussing how we'd help {COMPANY} ship faster?<br><br>{SENDER_EMAIL_SIGNATURE}"
    }
}

# Spintax versions for Campaign 516 (Corporates)
UPDATES_516 = {
    3300: {
        "email_body": "<p>{Hi|Hey|Hello} {FIRST_NAME}, pharosIQ (100+ person MarTech company) hired us to launch their AI product. We shipped it working with big data sets and AI-powered insights.</p><p><br></p><p>Mapped out an AI opportunity framework based on pharosIQ's approach. {Mind if I share it?|Want me to send it over?|Should I send it?}</p><p><br></p><p>{SENDER_EMAIL_SIGNATURE}</p>"
    },
    3301: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, pharosIQ (100+ team) needed overflow capacity to launch a new product. We gave them a dedicated pod that shipped in bi-weekly sprints.<br><br>If {COMPANY}'s internal team is maxed out, {worth discussing how we'd add capacity without hiring?|makes sense to chat about adding capacity?|interested in exploring this?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3302: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, FormelSkin hired us to build and launch an app as a lead magnet for their main business. We delivered a full product ready to drive user acquisition.<br><br>If {COMPANY} needs to launch a product or tool {fast|soon|quickly}, {worth 15 minutes to discuss your timeline?|makes sense to chat about your roadmap?|interested in a brief conversation?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3303: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {most|many} boards are pushing for AI integration but internal teams don't have the capacity or expertise to ship {fast|quickly|on time}.<br><br>We helped pharosIQ launch their AI product with a dedicated pod. FormelSkin and Exopulse hired us for similar innovation projects.<br><br>If {COMPANY} has an AI initiative on the roadmap, {worth 15 minutes to discuss your timeline?|makes sense to chat about your approach?|interested in exploring this?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3304: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, if your internal team can't keep up with your roadmap, you have two options: hire (takes months) or add a dedicated pod (ships in 2 weeks).<br><br>FormelSkin and Exopulse both hired us to add capacity and ship new products faster.<br><br>Full team: PM, design, dev, QA - shipping in bi-weekly sprints.<br><br>{Worth 15 minutes to discuss {COMPANY}'s roadmap?|Makes sense to chat about {COMPANY}'s needs?|Interested in exploring this?}<br><br>{SENDER_EMAIL_SIGNATURE}"
    },
    3305: {
        "email_body": "{Hi|Hey|Hello} {FIRST_NAME}, {circling back|following up|checking in} - any interest in discussing {COMPANY}'s AI initiatives or product roadmap?<br><br>{SENDER_EMAIL_SIGNATURE}"
    }
}

def update_sequence_step(step_id, email_body):
    """Update a single sequence step"""
    url = f"{BASE_URL}/campaigns/v1.1/sequence-steps/{step_id}"
    payload = {"email_body": email_body}
    
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.status_code, response.text

def main():
    results = []
    
    # Update Campaign 514
    print("Updating Campaign 514 (Early Stage)...")
    for step_id, data in UPDATES_514.items():
        status, resp = update_sequence_step(step_id, data["email_body"])
        result = f"Step {step_id}: {status}"
        print(result)
        results.append(result)
    
    # Update Campaign 515
    print("\nUpdating Campaign 515 (Mature Startups)...")
    for step_id, data in UPDATES_515.items():
        status, resp = update_sequence_step(step_id, data["email_body"])
        result = f"Step {step_id}: {status}"
        print(result)
        results.append(result)
    
    # Update Campaign 516
    print("\nUpdating Campaign 516 (Corporates)...")
    for step_id, data in UPDATES_516.items():
        status, resp = update_sequence_step(step_id, data["email_body"])
        result = f"Step {step_id}: {status}"
        print(result)
        results.append(result)
    
    print("\n=== Summary ===")
    success = sum(1 for r in results if "200" in r)
    print(f"Total updates: {len(results)}")
    print(f"Successful: {success}")
    print(f"Failed: {len(results) - success}")

if __name__ == "__main__":
    main()
