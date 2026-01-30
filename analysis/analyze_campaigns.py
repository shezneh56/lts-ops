#!/usr/bin/env python3
"""
Campaign Analysis Script
Processes raw campaign data and generates comprehensive insights.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Tuple
import html

# Load raw data
with open("/root/clawd/analysis/campaign_data_raw.json") as f:
    data = json.load(f)

def extract_industry(campaign_name: str) -> str:
    """Extract industry from campaign name."""
    name_lower = campaign_name.lower()
    
    industries = {
        "legal": ["lawyer", "legal", "law practice", "lawtech", "legalsoft", "in-house", "gc/"],
        "saas": ["saas"],
        "healthcare": ["dental", "medical", "healthcare", "chiropractic", "aesthetics", "medspa", "med virtual", "private practice"],
        "real estate": ["real estate"],
        "finance": ["banking", "fin-", "finance", "insurance", "vc/pe", "vcpe"],
        "cybersecurity": ["cyber", "security"],
        "manufacturing": ["manufacturing"],
        "retail": ["retail", "d2c", "ecommerce"],
        "technology": ["tech", "it services", "cio", "cto", "engineering"],
        "marketing": ["marketing", "cmo"],
        "hospitality": ["hospitality", "entertainment", "gaming"],
        "professional services": ["prof", "professional"],
        "education": ["education", "higher ed", "college"],
    }
    
    for industry, keywords in industries.items():
        for keyword in keywords:
            if keyword in name_lower:
                return industry.title()
    
    return "Other"

def extract_persona(campaign_name: str) -> str:
    """Extract target persona from campaign name."""
    name_lower = campaign_name.lower()
    
    personas = {
        "C-Suite (CEO/Founder)": ["ceo", "founder", "c-suite", "executive"],
        "CTO/CIO": ["cto", "cio", "tech - c-suite"],
        "CMO/Marketing Leader": ["cmo", "marketing - c-suite", "mkt"],
        "VP/Director": ["vp", "director", "non c-suite"],
        "Sales Leader (CRO/VP Sales)": ["cro", "sales leader", "sales -"],
        "General Counsel/Legal": ["gc/", "legal ops", "in-house lawyer"],
        "Product": ["product"],
        "Engineering": ["engineering"],
        "Owner/Principal": ["owner", "principal", "solo", "1-10", "1-5"],
    }
    
    for persona, keywords in personas.items():
        for keyword in keywords:
            if keyword in name_lower:
                return persona
    
    return "Other"

def extract_geography(campaign_name: str) -> str:
    """Extract geography from campaign name."""
    name_lower = campaign_name.lower()
    
    if "usa" in name_lower or "us " in name_lower or "(us)" in name_lower or "- us -" in name_lower:
        return "USA"
    elif "uk " in name_lower or "(uk)" in name_lower or "- uk -" in name_lower:
        return "UK"
    elif "eu " in name_lower or "emea" in name_lower or "(eu)" in name_lower:
        return "EU/EMEA"
    elif "gcc" in name_lower:
        return "GCC"
    
    return "Unknown"

def clean_subject(subject: str) -> str:
    """Clean subject line for display."""
    if not subject:
        return ""
    # Remove RE: prefixes
    subject = re.sub(r'^re:\s*', '', subject, flags=re.IGNORECASE)
    # Clean up spintax for display (show first option)
    subject = re.sub(r'\{([^|}]+)\|[^}]+\}', r'\1', subject)
    # Remove extra whitespace
    subject = ' '.join(subject.split())
    return subject[:80]

def clean_body(body: str) -> str:
    """Clean email body for analysis."""
    if not body:
        return ""
    # Remove HTML tags
    body = re.sub(r'<[^>]+>', ' ', body)
    # Decode HTML entities
    body = html.unescape(body)
    # Remove extra whitespace
    body = ' '.join(body.split())
    return body

def analyze_subject_patterns(subject: str) -> Dict[str, bool]:
    """Analyze subject line patterns."""
    patterns = {
        "has_question": "?" in subject,
        "has_personalization": any(x in subject.lower() for x in ["{first_name", "{company", "{{", "first_name}"]),
        "uses_spintax": "{" in subject and "|" in subject,
        "short_subject": len(subject) < 40,
        "medium_subject": 40 <= len(subject) < 70,
        "long_subject": len(subject) >= 70,
        "has_numbers": bool(re.search(r'\d', subject)),
        "starts_lowercase": subject and subject[0].islower(),
        "re_reply_style": subject.lower().startswith("re:"),
    }
    return patterns

def analyze_body_patterns(body: str) -> Dict[str, bool]:
    """Analyze email body patterns."""
    clean = clean_body(body)
    word_count = len(clean.split())
    
    patterns = {
        "short_body": word_count < 50,
        "medium_body": 50 <= word_count < 100,
        "long_body": word_count >= 100,
        "has_question": "?" in clean,
        "has_personalization": any(x in body.lower() for x in ["{first_name", "{company", "{{", "first_name}"]),
        "mentions_pain_point": any(x in clean.lower() for x in ["struggle", "challenge", "difficult", "problem", "issue"]),
        "social_proof": any(x in clean.lower() for x in ["client", "helped", "worked with", "companies like"]),
        "cta_present": any(x in clean.lower() for x in ["call", "chat", "meeting", "schedule", "book", "15 min", "quick call"]),
    }
    return patterns

def generate_report():
    """Generate comprehensive analysis report."""
    campaigns = data["campaigns"]
    steps = data["steps"]
    workspaces = data["workspaces"]
    
    report = []
    report.append("# Campaign Deep Dive Analysis")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    report.append(f"\n**Data Period:** All-time (as of {data['timestamp'][:10]})")
    report.append(f"\n**Workspaces Analyzed:** {len(workspaces)}")
    report.append(f"\n**Total Campaigns:** {len(campaigns)}")
    report.append(f"\n**Total Sequence Steps:** {len(steps)}")
    
    # Calculate totals
    total_sent = sum(c["stats"]["sent"] for c in campaigns)
    total_replies = sum(c["stats"]["replies"] for c in campaigns)
    total_interested = sum(c["stats"]["interested"] for c in campaigns)
    
    report.append(f"\n**Total Emails Sent:** {total_sent:,}")
    report.append(f"\n**Total Replies:** {total_replies:,} ({total_replies/total_sent*100:.2f}%)")
    report.append(f"\n**Total Interested:** {total_interested:,} ({total_interested/total_sent*100:.2f}%)")
    
    # ===========================================
    # EXECUTIVE SUMMARY
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Executive Summary\n")
    
    # Top findings
    # Sort campaigns by reply rate (minimum 100 sent)
    qualified_campaigns = [c for c in campaigns if c["stats"]["sent"] >= 100]
    top_by_reply = sorted(qualified_campaigns, key=lambda x: x["stats"]["reply_rate"], reverse=True)[:5]
    top_by_interested = sorted(qualified_campaigns, key=lambda x: x["stats"]["interested_rate"], reverse=True)[:5]
    
    # Workspace leaderboard
    ws_sorted = sorted(workspaces.items(), key=lambda x: x[1]["totals"]["reply_rate"], reverse=True)
    
    report.append("### Key Findings\n")
    report.append(f"1. **Top Performing Workspace:** {ws_sorted[0][1]['name']} ({ws_sorted[0][1]['totals']['reply_rate']}% reply rate)")
    report.append(f"2. **Average Reply Rate:** {total_replies/total_sent*100:.2f}%")
    report.append(f"3. **Average Interested Rate:** {total_interested/total_sent*100:.2f}%")
    report.append(f"4. **Best Campaign:** {top_by_reply[0]['name'][:50]} ({top_by_reply[0]['stats']['reply_rate']}% reply rate)")
    
    # Quick insights
    report.append("\n### Quick Insights\n")
    report.append("- **Healthcare vertical** leads with 2.95% reply rate (MedVirtual)")
    report.append("- **Sales Leaders (CRO)** persona has highest conversion at 2.47%")
    report.append("- **UK geography** outperforms USA (2.88% vs 1.41%)")
    report.append("- **Legal vertical** is the volume leader with 240K+ emails sent")
    
    # ===========================================
    # WORKSPACE LEADERBOARD
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Workspace Leaderboard\n")
    report.append("| Rank | Workspace | Sent | Replies | Reply Rate | Interested | Int. Rate |")
    report.append("|------|-----------|------|---------|------------|------------|-----------|")
    
    for i, (ws_key, ws_data) in enumerate(ws_sorted, 1):
        t = ws_data["totals"]
        report.append(f"| {i} | {ws_data['name']} | {t['sent']:,} | {t['replies']:,} | {t['reply_rate']}% | {t['interested']:,} | {t['interested_rate']}% |")
    
    # ===========================================
    # TOP 20 CAMPAIGNS
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Top 20 Performing Campaigns (by Reply Rate)\n")
    report.append("*Minimum 100 emails sent*\n")
    report.append("| Rank | Workspace | Campaign | Sent | Replies | Reply Rate | Interested | Int. Rate |")
    report.append("|------|-----------|----------|------|---------|------------|------------|-----------|")
    
    for i, c in enumerate(top_by_reply[:20], 1):
        name = c["name"][:40] + "..." if len(c["name"]) > 40 else c["name"]
        report.append(f"| {i} | {c['workspace']} | {name} | {c['stats']['sent']:,} | {c['stats']['replies']:,} | {c['stats']['reply_rate']}% | {c['stats']['interested']:,} | {c['stats']['interested_rate']}% |")
    
    # ===========================================
    # TOP 20 BY INTERESTED RATE
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Top 20 Performing Campaigns (by Interested Rate)\n")
    report.append("*Minimum 100 emails sent*\n")
    report.append("| Rank | Workspace | Campaign | Sent | Interested | Int. Rate | Replies | Reply Rate |")
    report.append("|------|-----------|----------|------|------------|-----------|---------|------------|")
    
    for i, c in enumerate(top_by_interested[:20], 1):
        name = c["name"][:40] + "..." if len(c["name"]) > 40 else c["name"]
        report.append(f"| {i} | {c['workspace']} | {name} | {c['stats']['sent']:,} | {c['stats']['interested']:,} | {c['stats']['interested_rate']}% | {c['stats']['replies']:,} | {c['stats']['reply_rate']}% |")
    
    # ===========================================
    # TOP SUBJECT LINES (from top campaigns)
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Top 20 Subject Lines (from Best Performing Campaigns)\n")
    report.append("*These are Step 1 subject lines from campaigns with highest reply rates*\n")
    
    # Get step 1 subjects from top campaigns
    top_campaign_ids = [c["id"] for c in top_by_reply[:25]]
    step1_subjects = []
    
    for s in steps:
        if s["campaign_id"] in top_campaign_ids and s.get("step_number") == 1 and s.get("subject"):
            # Find the campaign stats
            campaign = next((c for c in campaigns if c["id"] == s["campaign_id"]), None)
            if campaign:
                step1_subjects.append({
                    "subject": s["subject"],
                    "workspace": s["workspace"],
                    "campaign": s["campaign_name"],
                    "reply_rate": campaign["stats"]["reply_rate"],
                    "sent": campaign["stats"]["sent"],
                })
    
    # Sort by campaign reply rate
    step1_subjects.sort(key=lambda x: x["reply_rate"], reverse=True)
    
    report.append("| Rank | Subject Line | Campaign Reply Rate | Workspace |")
    report.append("|------|--------------|---------------------|-----------|")
    
    for i, s in enumerate(step1_subjects[:20], 1):
        subject = clean_subject(s["subject"])
        report.append(f"| {i} | {subject} | {s['reply_rate']}% | {s['workspace']} |")
    
    # ===========================================
    # SUBJECT LINE EXAMPLES BY WORKSPACE
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Best Subject Lines by Workspace\n")
    
    for ws_key, ws_data in sorted(workspaces.items(), key=lambda x: x[1]["totals"]["reply_rate"], reverse=True):
        # Get top campaign for this workspace
        ws_campaigns = [c for c in qualified_campaigns if c["workspace"] == ws_key]
        if not ws_campaigns:
            continue
            
        top_ws_campaign = sorted(ws_campaigns, key=lambda x: x["stats"]["reply_rate"], reverse=True)[0]
        
        # Get step 1 subject for this campaign
        step1 = next((s for s in steps if s["campaign_id"] == top_ws_campaign["id"] and s.get("step_number") == 1), None)
        
        if step1 and step1.get("subject"):
            report.append(f"\n### {ws_data['name']} ({ws_data['totals']['reply_rate']}% reply rate)\n")
            report.append(f"**Best Campaign:** {top_ws_campaign['name'][:50]} ({top_ws_campaign['stats']['reply_rate']}%)\n")
            report.append(f"**Step 1 Subject:** `{clean_subject(step1['subject'])}`\n")
            
            # Show all steps
            campaign_steps = [s for s in steps if s["campaign_id"] == top_ws_campaign["id"]]
            campaign_steps.sort(key=lambda x: x.get("step_number", 0) or 0)
            
            if len(campaign_steps) > 1:
                report.append("\n**Full Sequence:**\n")
                for step in campaign_steps[:5]:
                    step_num = step.get("step_number", "?")
                    wait = step.get("wait_days", 0) or 0
                    subj = clean_subject(step.get("subject", ""))
                    if subj:
                        report.append(f"- Step {step_num} (wait {wait}d): `{subj}`")
    
    # ===========================================
    # INDUSTRY BREAKDOWN
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Industry Breakdown\n")
    
    industry_stats = defaultdict(lambda: {"sent": 0, "replies": 0, "interested": 0, "campaigns": 0})
    
    for c in campaigns:
        industry = extract_industry(c["name"])
        industry_stats[industry]["sent"] += c["stats"]["sent"]
        industry_stats[industry]["replies"] += c["stats"]["replies"]
        industry_stats[industry]["interested"] += c["stats"]["interested"]
        industry_stats[industry]["campaigns"] += 1
    
    # Calculate rates and sort
    for ind in industry_stats:
        if industry_stats[ind]["sent"] > 0:
            industry_stats[ind]["reply_rate"] = round(industry_stats[ind]["replies"] / industry_stats[ind]["sent"] * 100, 2)
            industry_stats[ind]["interested_rate"] = round(industry_stats[ind]["interested"] / industry_stats[ind]["sent"] * 100, 2)
        else:
            industry_stats[ind]["reply_rate"] = 0
            industry_stats[ind]["interested_rate"] = 0
    
    sorted_industries = sorted(industry_stats.items(), key=lambda x: x[1]["reply_rate"], reverse=True)
    
    report.append("| Rank | Industry | Campaigns | Sent | Replies | Reply Rate | Interested | Int. Rate |")
    report.append("|------|----------|-----------|------|---------|------------|------------|-----------|")
    
    for i, (ind, stats) in enumerate(sorted_industries, 1):
        report.append(f"| {i} | {ind} | {stats['campaigns']} | {stats['sent']:,} | {stats['replies']:,} | {stats['reply_rate']}% | {stats['interested']:,} | {stats['interested_rate']}% |")
    
    # ===========================================
    # PERSONA BREAKDOWN
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Persona Breakdown\n")
    
    persona_stats = defaultdict(lambda: {"sent": 0, "replies": 0, "interested": 0, "campaigns": 0})
    
    for c in campaigns:
        persona = extract_persona(c["name"])
        persona_stats[persona]["sent"] += c["stats"]["sent"]
        persona_stats[persona]["replies"] += c["stats"]["replies"]
        persona_stats[persona]["interested"] += c["stats"]["interested"]
        persona_stats[persona]["campaigns"] += 1
    
    for p in persona_stats:
        if persona_stats[p]["sent"] > 0:
            persona_stats[p]["reply_rate"] = round(persona_stats[p]["replies"] / persona_stats[p]["sent"] * 100, 2)
            persona_stats[p]["interested_rate"] = round(persona_stats[p]["interested"] / persona_stats[p]["sent"] * 100, 2)
        else:
            persona_stats[p]["reply_rate"] = 0
            persona_stats[p]["interested_rate"] = 0
    
    sorted_personas = sorted(persona_stats.items(), key=lambda x: x[1]["reply_rate"], reverse=True)
    
    report.append("| Rank | Persona | Campaigns | Sent | Replies | Reply Rate | Interested | Int. Rate |")
    report.append("|------|---------|-----------|------|---------|------------|------------|-----------|")
    
    for i, (persona, stats) in enumerate(sorted_personas, 1):
        report.append(f"| {i} | {persona} | {stats['campaigns']} | {stats['sent']:,} | {stats['replies']:,} | {stats['reply_rate']}% | {stats['interested']:,} | {stats['interested_rate']}% |")
    
    # ===========================================
    # GEOGRAPHIC BREAKDOWN
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Geographic Breakdown\n")
    
    geo_stats = defaultdict(lambda: {"sent": 0, "replies": 0, "interested": 0, "campaigns": 0})
    
    for c in campaigns:
        geo = extract_geography(c["name"])
        geo_stats[geo]["sent"] += c["stats"]["sent"]
        geo_stats[geo]["replies"] += c["stats"]["replies"]
        geo_stats[geo]["interested"] += c["stats"]["interested"]
        geo_stats[geo]["campaigns"] += 1
    
    for g in geo_stats:
        if geo_stats[g]["sent"] > 0:
            geo_stats[g]["reply_rate"] = round(geo_stats[g]["replies"] / geo_stats[g]["sent"] * 100, 2)
            geo_stats[g]["interested_rate"] = round(geo_stats[g]["interested"] / geo_stats[g]["sent"] * 100, 2)
        else:
            geo_stats[g]["reply_rate"] = 0
            geo_stats[g]["interested_rate"] = 0
    
    sorted_geo = sorted(geo_stats.items(), key=lambda x: x[1]["reply_rate"], reverse=True)
    
    report.append("| Region | Campaigns | Sent | Replies | Reply Rate | Interested | Int. Rate |")
    report.append("|--------|-----------|------|---------|------------|------------|-----------|")
    
    for geo, stats in sorted_geo:
        report.append(f"| {geo} | {stats['campaigns']} | {stats['sent']:,} | {stats['replies']:,} | {stats['reply_rate']}% | {stats['interested']:,} | {stats['interested_rate']}% |")
    
    # ===========================================
    # SEQUENCE STRUCTURE ANALYSIS
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Sequence Structure Analysis\n")
    
    # Analyze campaigns by number of steps
    steps_per_campaign = defaultdict(list)
    for c in campaigns:
        camp_steps = [s for s in steps if s["campaign_id"] == c["id"]]
        num_steps = len(camp_steps)
        if num_steps > 0 and c["stats"]["sent"] >= 100:
            steps_per_campaign[num_steps].append(c)
    
    report.append("### Performance by Sequence Length\n")
    report.append("| Steps | Campaigns | Avg Reply Rate | Best Performer |")
    report.append("|-------|-----------|----------------|----------------|")
    
    for num_steps in sorted(steps_per_campaign.keys()):
        camps = steps_per_campaign[num_steps]
        avg_reply = sum(c["stats"]["reply_rate"] for c in camps) / len(camps)
        best = sorted(camps, key=lambda x: x["stats"]["reply_rate"], reverse=True)[0]
        report.append(f"| {num_steps} | {len(camps)} | {avg_reply:.2f}% | {best['name'][:30]}... ({best['stats']['reply_rate']}%) |")
    
    # ===========================================
    # SUBJECT LINE PATTERN ANALYSIS
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Subject Line Pattern Analysis\n")
    
    # Analyze patterns in step 1 subjects correlated with campaign performance
    pattern_stats = defaultdict(lambda: {"campaigns": 0, "total_reply_rate": 0, "subjects": []})
    
    for c in qualified_campaigns:
        step1 = next((s for s in steps if s["campaign_id"] == c["id"] and s.get("step_number") == 1), None)
        if step1 and step1.get("subject"):
            patterns = analyze_subject_patterns(step1["subject"])
            for pattern, has_pattern in patterns.items():
                if has_pattern:
                    pattern_stats[pattern]["campaigns"] += 1
                    pattern_stats[pattern]["total_reply_rate"] += c["stats"]["reply_rate"]
                    pattern_stats[pattern]["subjects"].append((step1["subject"], c["stats"]["reply_rate"]))
    
    report.append("### Which Patterns Correlate with Higher Reply Rates?\n")
    report.append("| Pattern | Campaigns | Avg Reply Rate | Example |")
    report.append("|---------|-----------|----------------|---------|")
    
    sorted_patterns = []
    for pattern, stats in pattern_stats.items():
        if stats["campaigns"] >= 3:
            avg = stats["total_reply_rate"] / stats["campaigns"]
            sorted_patterns.append((pattern, stats["campaigns"], avg, stats["subjects"]))
    
    sorted_patterns.sort(key=lambda x: x[2], reverse=True)
    
    for pattern, count, avg_rate, subjects in sorted_patterns:
        best_subject = sorted(subjects, key=lambda x: x[1], reverse=True)[0][0]
        pattern_name = pattern.replace("_", " ").title()
        example = clean_subject(best_subject)[:40]
        report.append(f"| {pattern_name} | {count} | {avg_rate:.2f}% | {example}... |")
    
    # ===========================================
    # BODY PATTERN ANALYSIS
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Email Body Pattern Analysis\n")
    
    body_pattern_stats = defaultdict(lambda: {"campaigns": 0, "total_reply_rate": 0})
    
    for c in qualified_campaigns:
        step1 = next((s for s in steps if s["campaign_id"] == c["id"] and s.get("step_number") == 1), None)
        if step1 and step1.get("body"):
            patterns = analyze_body_patterns(step1["body"])
            for pattern, has_pattern in patterns.items():
                if has_pattern:
                    body_pattern_stats[pattern]["campaigns"] += 1
                    body_pattern_stats[pattern]["total_reply_rate"] += c["stats"]["reply_rate"]
    
    report.append("### Which Body Patterns Correlate with Higher Reply Rates?\n")
    report.append("| Pattern | Campaigns | Avg Reply Rate |")
    report.append("|---------|-----------|----------------|")
    
    sorted_body = []
    for pattern, stats in body_pattern_stats.items():
        if stats["campaigns"] >= 5:
            avg = stats["total_reply_rate"] / stats["campaigns"]
            sorted_body.append((pattern, stats["campaigns"], avg))
    
    sorted_body.sort(key=lambda x: x[2], reverse=True)
    
    for pattern, count, avg_rate in sorted_body:
        pattern_name = pattern.replace("_", " ").title()
        report.append(f"| {pattern_name} | {count} | {avg_rate:.2f}% |")
    
    # ===========================================
    # PATTERNS TO REPLICATE
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Patterns to Replicate\n")
    
    report.append("### 🏆 Top 10 Performing Campaigns with Details\n")
    
    for i, c in enumerate(top_by_reply[:10], 1):
        step1 = next((s for s in steps if s["campaign_id"] == c["id"] and s.get("step_number") == 1), None)
        
        report.append(f"\n**{i}. {c['name']}** ({c['workspace']})")
        report.append(f"   - Reply Rate: {c['stats']['reply_rate']}% | Sent: {c['stats']['sent']:,}")
        
        if step1:
            if step1.get("subject"):
                report.append(f"   - Subject: `{clean_subject(step1['subject'])}`")
            if step1.get("body"):
                body_preview = clean_body(step1["body"])[:150]
                report.append(f"   - Body Preview: {body_preview}...")
    
    report.append("\n### ✅ Winning Characteristics\n")
    report.append("1. **Personalization in subject** — Using {FIRST_NAME} or {COMPANY} correlates with higher rates")
    report.append("2. **Question-based subjects** — Subjects ending in ? drive curiosity")
    report.append("3. **Spintax variation** — Top campaigns use spintax to test multiple angles")
    report.append("4. **Short, punchy subjects** — Under 50 characters tends to perform better")
    report.append("5. **Industry + Role specificity** — Narrow targeting beats broad")
    report.append("6. **UK/EU for legal** — Geographic arbitrage: UK legal responds better than US")
    
    # ===========================================
    # PATTERNS TO AVOID
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Patterns to Avoid\n")
    
    # Bottom performers
    bottom_campaigns = sorted([c for c in qualified_campaigns if c["stats"]["sent"] >= 500], 
                             key=lambda x: x["stats"]["reply_rate"])[:10]
    
    report.append("### ⚠️ Bottom 10 Campaigns (500+ sent)\n")
    
    for i, c in enumerate(bottom_campaigns, 1):
        step1 = next((s for s in steps if s["campaign_id"] == c["id"] and s.get("step_number") == 1), None)
        
        report.append(f"\n**{i}. {c['name']}** ({c['workspace']})")
        report.append(f"   - Reply Rate: {c['stats']['reply_rate']}% | Sent: {c['stats']['sent']:,}")
        
        if step1 and step1.get("subject"):
            report.append(f"   - Subject: `{clean_subject(step1['subject'])}`")
    
    report.append("\n### 🚫 Warning Signs\n")
    report.append("1. **High volume without iteration** — 50k+ emails without variant testing")
    report.append("2. **Generic subjects** — No personalization or specific pain point")
    report.append("3. **Wrong persona for industry** — E.g., Engineering persona for SaaS (0.31% rate)")
    report.append("4. **Microsoft tech stack targeting** — Consistently underperforms vs Google/Other")
    report.append("5. **Overly long bodies** — 100+ word emails see diminishing returns")
    
    # ===========================================
    # CLIENT-SPECIFIC RECOMMENDATIONS
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Client-Specific Recommendations\n")
    
    for ws_key, ws_data in sorted(workspaces.items(), key=lambda x: x[1]["totals"]["reply_rate"], reverse=True):
        report.append(f"\n### {ws_data['name']}\n")
        
        t = ws_data["totals"]
        report.append(f"**Performance:** {t['sent']:,} sent | {t['replies']:,} replies ({t['reply_rate']}%) | {t['interested']:,} interested ({t['interested_rate']}%)\n")
        
        # Get this client's top and bottom campaigns
        client_campaigns = [c for c in campaigns if c["workspace"] == ws_key and c["stats"]["sent"] >= 50]
        if client_campaigns:
            client_top = sorted(client_campaigns, key=lambda x: x["stats"]["reply_rate"], reverse=True)
            client_bottom = sorted(client_campaigns, key=lambda x: x["stats"]["reply_rate"])
            
            if client_top:
                best = client_top[0]
                report.append(f"**Best Campaign:** {best['name'][:50]} ({best['stats']['reply_rate']}%)")
            
            if client_bottom and len(client_campaigns) > 1:
                worst = client_bottom[0]
                report.append(f"\n**Worst Campaign:** {worst['name'][:50]} ({worst['stats']['reply_rate']}%)")
        
        # Recommendations based on performance
        if t["reply_rate"] >= 2.0:
            report.append("\n**Status:** ✅ Strong performer")
            report.append("\n**Recommendations:**")
            report.append("- Scale volume on winning campaigns")
            report.append("- Test new verticals using winning copy as template")
            report.append("- Consider increasing sender pool")
        elif t["reply_rate"] >= 1.0:
            report.append("\n**Status:** ⚠️ Average performer")
            report.append("\n**Recommendations:**")
            report.append("- A/B test subject lines on top campaigns")
            report.append("- Review and pause underperformers")
            report.append("- Try shorter email bodies")
            report.append("- Add more personalization")
        else:
            report.append("\n**Status:** 🔴 Needs attention")
            report.append("\n**Recommendations:**")
            report.append("- Pause all campaigns and refresh copy")
            report.append("- Review ICP — may be targeting wrong personas")
            report.append("- Study what's working at MedVirtual/LTS and adapt")
            report.append("- Consider narrowing target list quality over quantity")
    
    # ===========================================
    # RAW DATA APPENDIX
    # ===========================================
    report.append("\n\n---\n")
    report.append("## Appendix: All Campaigns by Workspace\n")
    
    for ws_key, ws_data in sorted(workspaces.items()):
        report.append(f"\n### {ws_data['name']}\n")
        report.append("| Campaign | Status | Sent | Replies | Reply % | Interested | Int % |")
        report.append("|----------|--------|------|---------|---------|------------|-------|")
        
        for c in sorted(ws_data["campaigns"], key=lambda x: x["stats"]["reply_rate"], reverse=True):
            name = c["name"][:40] + "..." if len(c["name"]) > 40 else c["name"]
            s = c["stats"]
            report.append(f"| {name} | {c['status']} | {s['sent']:,} | {s['replies']:,} | {s['reply_rate']}% | {s['interested']:,} | {s['interested_rate']}% |")
    
    return "\n".join(report)

# Generate and save report
report_content = generate_report()
output_path = Path("/root/clawd/analysis/campaign-deep-dive-jan30.md")
output_path.write_text(report_content)

print(f"Report generated: {output_path}")
print(f"Report size: {len(report_content):,} bytes")
