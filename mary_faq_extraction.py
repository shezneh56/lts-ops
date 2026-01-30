#!/usr/bin/env python3
"""Extract FAQ questions from positive replies across all workspaces."""

import json
import re
import sys
import requests
from html import unescape
from pathlib import Path

def p(msg):
    print(msg, flush=True)

# Load workspace keys
with open('/root/clawd/claude-code-projects/config/workspace_keys.json') as f:
    config = json.load(f)

WORKSPACES = config['workspaces']

# Question patterns to detect positive interest
POSITIVE_PATTERNS = [
    r'how much', r'what.*(cost|price|pricing|rate|fee)',
    r'how does.*(work|it work)', r'what.*(process|approach)',
    r'can you (tell|share|explain|send)', r'tell me more', r'more info',
    r'interested', r"i'?d like to",
    r'like to (learn|know|hear|chat|talk|meet|discuss)',
    r'(schedule|book|set up).*(call|meeting|time)',
    r'when.*(available|can we)', r'timeline', r'how (long|quickly|fast)',
    r'example|case study|proof|results',
    r'who.*(work with|worked with|clients)', r'what.*(include|included)',
    r'next step', r'how (do|would) (we|I) (get started|start|begin)',
    r'can you (help|do|handle)',
]

NEGATIVE_PATTERNS = [
    r'unsubscribe', r'remove (me|us)', r'take (me|us) off',
    r'stop (email|contact)', r'not interested', r'no thank', r'\bpass\b',
    r'not (for us|a fit|right now|at this time)', r'out of office', r'\booo\b',
    r'automatic reply', r'auto.?reply', r'on (vacation|leave|holiday|pto)',
    r'wrong person', r'don.t handle', r'not my (area|department|responsibility)',
    r'left the company', r'no longer (work|with)', r'moved on from', r'have moved on',
]

def strip_html(html):
    if not html: return ""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<br\s*/?>|</p>|</div>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_positive(text, interested=False, automated=False):
    if automated: return False
    if interested: return True
    t = text.lower()
    for p in NEGATIVE_PATTERNS:
        if re.search(p, t): return False
    for p in POSITIVE_PATTERNS:
        if re.search(p, t): return True
    return '?' in text and len(text) > 20

def extract_questions(text):
    questions = []
    for s in re.split(r'[.!?\n]+', text):
        s = s.strip()
        if len(s) < 10: continue
        sl = s.lower()
        if any(re.search(pat, sl) for pat in POSITIVE_PATTERNS) or \
           any(w in sl for w in ['what','how','when','where','why','who','can you','could you','would you','do you']):
            questions.append(s)
    return questions

def categorize(q):
    ql = q.lower()
    if any(w in ql for w in ['cost','price','pricing','rate','fee','how much','investment','budget','charge','pay']):
        return 'pricing'
    if any(w in ql for w in ['process','work','approach','how do','how does','what do you','what does','tell me more','more info','explain']):
        return 'process'
    if any(w in ql for w in ['timeline','long','quickly','fast','when','time frame','turnaround','how soon','duration']):
        return 'timeline'
    if any(w in ql for w in ['example','case study','proof','results','success','roi','testimonial','reference']):
        return 'proof'
    if any(w in ql for w in ['who do you','work with','industry','companies','typical client','your clients','similar to']):
        return 'who_you_work_with'
    if any(w in ql for w in ['next step','get started','start','begin','available','schedule','call','meeting','chat','talk']):
        return 'next_steps'
    if any(w in ql for w in ['integrate','technical','technology','platform','system','api','software','tools','stack']):
        return 'technical'
    return 'other'

def get_replies(ws):
    """Fetch replies using default page size (15 per page)."""
    headers = {'Authorization': f'Bearer {ws["api_key"]}', 'Accept': 'application/json'}
    all_r = []
    page = 1
    while True:
        try:
            r = requests.get(f'{ws["base_url"]}/replies?page={page}', headers=headers, timeout=15)
            if r.status_code != 200:
                p(f"  Err {r.status_code} on page {page}")
                break
            data = r.json()
            replies = data.get('data', [])
            if not replies: break
            all_r.extend(replies)
            if page % 20 == 0: p(f"  ...page {page}")
            meta = data.get('meta', {})
            if page >= meta.get('last_page', 1): break
            page += 1
        except Exception as e:
            p(f"  Err page {page}: {e}")
            break
    p(f"  Fetched {len(all_r)} replies from {page} pages")
    return all_r

def main():
    pf = Path('/root/clawd/mary_faq_analysis.json')
    if pf.exists():
        with open(pf) as f: results = json.load(f)
        p("Resuming...")
        done = set(results.get('processed_workspaces', []))
    else:
        results = {
            'categories': {k: [] for k in ['pricing','process','timeline','proof','who_you_work_with','next_steps','technical','other']},
            'total_questions': 0,
            'by_workspace': {},
            'raw_positive_replies': [],
            'processed_workspaces': [],
        }
        done = set()
    
    for ws in WORKSPACES:
        sn = ws['short_name']
        if sn in done:
            p(f"\nSkip {sn}")
            continue
        p(f"\n=== {sn} ===")
        replies = get_replies(ws)
        wq = 0; wp = 0
        for r in replies:
            text = strip_html(r.get('html_body', ''))
            if len(text) < 20: continue
            if not is_positive(text, r.get('interested'), r.get('automated_reply')): continue
            wp += 1
            results['raw_positive_replies'].append({'workspace': sn, 'text': text[:500], 'interested': r.get('interested'), 'id': r.get('id')})
            for q in extract_questions(text):
                cat = categorize(q)
                results['categories'][cat].append({'question': q[:300], 'workspace': sn, 'reply_snippet': text[:200]})
                wq += 1
                results['total_questions'] += 1
        results['by_workspace'][sn] = wq
        results['processed_workspaces'].append(sn)
        p(f"  Positive: {wp}, Questions: {wq}")
        with open(pf, 'w') as f: json.dump(results, f, indent=2)
        p(f"  Saved.")
    
    p(f"\n=== DONE ===")
    p(f"Total: {results['total_questions']}")
    for c, items in results['categories'].items():
        p(f"  {c}: {len(items)}")

if __name__ == '__main__':
    main()
