# Content Strategy Context

## Content Files Location
Local machine: `/Users/liamsheridan/Library/Mobile Documents/com~apple~CloudDocs/Flare Finance/Skool/ExecLytix/Claude Code/intelligence/content/`

## Key Files
| File | Contents |
|------|----------|
| outbound_that_works_newsletter_drafts.md | 20 newsletter issues + 2 welcome emails |
| x_content_2_weeks.md | 42 X posts + 6 lead magnet posts |
| schedule_newsletters.py | Script that pushed newsletters to Kit |
| schedule_x_posts.py | Script that pushed 42 posts to Typefully |
| schedule_x_filler.py | Script for Jan 22-26 filler posts |
| schedule_x_remaining.py | 7 pending posts (run when rate limit resets) |
| lead_magnets/tam_coverage_system.md | TAM Coverage lead magnet content |
| lead_magnets/infrastructure_breakdown.md | Infrastructure lead magnet content |

## Newsletter Format (~500 words, 3-5 min read)
```
Hey {{ subscriber.first_name | default: "there" }},

[Hook - 1-2 sentences, the problem]

[Issue - what's going wrong, 2-3 paragraphs]

[Take - the contrarian angle, what actually works]

[Action - what to do about it]

Talk soon,
Liam

P.S. [Soft CTA or additional thought]
```

## 5 Content Pillars
1. Full TAM Coverage (the core methodology)
2. Deliverability & Infrastructure
3. Messaging & Copy
4. Targeting & ICP
5. Operations & Execution

## X Content Style Guide
- All lowercase
- Profanity allowed (fuck, shit, etc.)
- Short sentences, line breaks between thoughts
- Stream of consciousness feel
- No threads - single posts only
- No emojis
- No hashtags

## Lead Magnet Posts (4 keywords)
- BENCHMARK → Cold Email Benchmark Report summary
- CLAUDE → Claude AI research copilot breakdown
- TAM → Full TAM Coverage System doc
- INFRA → Infrastructure Breakdown doc

Format: "like + comment '[KEYWORD]' and i'll DM you. (must be following)"

## YouTube Strategy (Not Yet Executed)
Format:
- Loom-style: face in corner + slides/deck OR just face
- 5-8 minutes per video
- No fancy editing, natural conversational tone
- Batch record 2-5 in one session
- Upload weekly (Saturday/Sunday)

First 10 Topics:
1. Why Your Cold Email Lands in Spam (Infrastructure Fix)
2. How to Reach Every Buyer in Your Market Every 45 Days
3. The Perfect Cold Email is Under 80 Words
4. Intent Data is Dead. Here's What Works Instead
5. Cold Email Infrastructure: Send 1,500/Day Without Spam
6. Stop Personalising Cold Emails (Do This Instead)
7. Is Cold Email Dead in 2026? (The Data Says No)
8. Your SDR Costs $50K Before They Book a Meeting
9. The Only 3 Metrics That Matter in Cold Email
10. How to Warm Up Domains: The 4-Week Process

## Lead Magnets Status
| Keyword | Lead Magnet | Status |
|---------|-------------|--------|
| BENCHMARK | 2026 Cold Email Benchmark Report Summary | Content exists, needs Notion/Doc |
| CLAUDE | Claude AI Research Copilot Breakdown | Content exists, needs Notion/Doc |
| TAM | Full TAM Coverage System | .md file done, needs conversion |
| INFRA | Cold Email Infrastructure Breakdown | .md file done, needs conversion |

Delivery: User comments keyword → Manual DM with Notion/Google Doc link

## Pending Tasks
1. Run schedule_x_remaining.py - 7 posts pending
2. Convert lead magnets to shareable format (Notion/Google Docs)
3. LinkedIn content - not started, repurpose X with more professional tone
4. Welcome sequence setup - copy written, needs Kit automation setup
5. YouTube execution - strategy done, needs batch recording

## Posting Schedule
- X: 8am, 12pm, 5pm ET (13:00, 17:00, 22:00 UTC)
- Newsletter: 9am ET Tue + Thu (14:00 UTC)

## Key Rules
- Never send cold email from primary domain (leadsthat.show is for newsletter only)
- Newsletter sends from liam@leadsthat.show
- Full TAM coverage = reach 100% of market every 45-60 days
- Only 3% ready to buy at any time → catch different 3% each cycle

## API Keys (for testing)
- Kit: kit_4ee5022bd8f9f3a0dbbbc745f03d2d3e
- Typefully: ctRNo9rPodWnQwGyqyAs3IMW24LGg4jd

## Stats
- 50 people on newsletter from LinkedIn lead magnets (as of Jan 27)
- 42 X posts scheduled
- 20 newsletter issues drafted
