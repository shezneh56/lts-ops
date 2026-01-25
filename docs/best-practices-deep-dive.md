# Clawdbot Best Practices - Deep Dive

*Compiled from official docs + community patterns: 2026-01-25*

## 📚 Table of Contents
1. [Memory Management](#memory-management)
2. [Session Strategy](#session-strategy)
3. [Heartbeats vs Cron](#heartbeats-vs-cron)
4. [Skills & Tools](#skills--tools)
5. [Security & Safety](#security--safety)
6. [Performance & Costs](#performance--costs)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)

---

## 🧠 Memory Management

### File Structure (Best Practices)

**Two-tier memory system:**
1. **`memory/YYYY-MM-DD.md`** - Daily append-only logs
   - Raw notes, decisions, conversations
   - Auto-loaded: today + yesterday
   - Rotates daily at 4 AM (configurable)

2. **`MEMORY.md`** - Curated long-term memory
   - Distilled insights, preferences, key facts
   - **ONLY loaded in main/private sessions** (never groups for security)
   - Think: "refined knowledge base" vs raw logs

### Golden Rules

**✅ DO:**
- Write immediately when someone says "remember this"
- Store decisions, preferences, API keys in MEMORY.md
- Use daily files for running context
- Review daily files → update MEMORY.md periodically (via heartbeat)
- Keep MEMORY.md focused (distilled, not exhaustive)

**❌ DON'T:**
- Keep things "in your head" — memory is files, not RAM
- Put secrets in HEARTBEAT.md (it's in every prompt)
- Load MEMORY.md in group chats (privacy leak)
- Let MEMORY.md grow unbounded (impacts token costs)

### Memory Search (Vector + BM25)

**Hybrid search is enabled by default:**
- **Vector (70%):** Semantic similarity ("Mac Studio" ≈ "gateway host")
- **BM25 (30%):** Exact tokens (IDs, code symbols, error strings)

**Best practices:**
- Use `memory_search` before answering questions about past work
- Follow up with `memory_get` to pull specific snippets (keeps context small)
- For large memory bases: use OpenAI batch embeddings (fast + cheap)
- Local embeddings: good for privacy, but slower initial indexing

**Config tip:**
```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "openai",
        "model": "text-embedding-3-small",
        "remote": {
          "batch": { "enabled": true, "concurrency": 2 }
        },
        "query": {
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3
          }
        }
      }
    }
  }
}
```

### Automatic Memory Flush (Pre-Compaction)

**How it works:**
- When session nears compaction, Clawdbot triggers a silent turn
- Model writes important memories to disk
- Usually responds with `NO_REPLY` (user never sees it)
- Happens once per compaction cycle

**Why it matters:**
- Prevents loss of context when old messages are compacted
- Ensures continuity across long conversations
- Automatic, no user intervention needed

---

## 🔄 Session Strategy

### Session Scopes

**Three main patterns:**

1. **`dmScope: "main"` (default)**
   - All DMs collapse to one continuous session
   - Best for: personal assistant, continuity across devices
   - Example: WhatsApp + Telegram + Discord all share context

2. **`dmScope: "per-peer"`**
   - Isolate by sender ID across all channels
   - Best for: multi-user support, client work
   - Example: Alice's DMs stay separate from Bob's

3. **`dmScope: "per-channel-peer"`**
   - Isolate by channel + sender
   - Best for: shared inboxes, team accounts
   - Example: Alice on WhatsApp ≠ Alice on Telegram

**Identity linking (cross-channel continuity):**
```json
{
  "session": {
    "dmScope": "per-peer",
    "identityLinks": {
      "alice": ["telegram:123456789", "discord:987654321012345678"]
    }
  }
}
```
Now Alice's Telegram + Discord DMs share one session.

### Reset Policies

**Daily reset (default):**
- Expires at 4 AM local time
- Fresh context each day
- Good for: daily workflows, avoiding stale context

**Idle reset:**
- Sliding window (e.g., 120 min of inactivity)
- Good for: bursty conversations, client work

**Per-type overrides:**
```json
{
  "session": {
    "resetByType": {
      "dm": { "mode": "idle", "idleMinutes": 240 },
      "group": { "mode": "idle", "idleMinutes": 120 },
      "thread": { "mode": "daily", "atHour": 4 }
    }
  }
}
```

**Per-channel overrides:**
```json
{
  "session": {
    "resetByChannel": {
      "discord": { "mode": "idle", "idleMinutes": 10080 }  // 7 days
    }
  }
}
```

### Manual Session Control

**Commands:**
- `/new` - Start fresh session (pass model alias: `/new opus`)
- `/reset` - Same as /new
- `/status` - See token usage, thinking level, context size
- `/context list` - What's in system prompt + workspace files
- `/context detail` - Biggest context contributors
- `/compact` - Force summarize older context
- `/stop` - Abort current run + clear queue

**Tip:** Send these as standalone messages.

---

## ⏰ Heartbeats vs Cron

### When to Use Each

| **Use Case** | **Tool** | **Why** |
|--------------|----------|---------|
| Batch periodic checks (inbox + calendar) | Heartbeat | Combines context, conversational |
| Exact timing ("9 AM every Monday") | Cron | Precise scheduling |
| Isolated background task | Cron (isolated) | Doesn't spam main history |
| One-shot reminder ("in 20 min") | Cron (at + deleteAfterRun) | Fire-and-forget |
| Main context needed | Heartbeat | Runs in main session |
| Deliver to specific channel | Cron | Supports channel + target |

**Golden rule:** Batch similar checks into `HEARTBEAT.md` instead of multiple cron jobs.

### Heartbeat Best Practices

**HEARTBEAT.md structure:**
```markdown
# Heartbeat checklist

- Scan inbox for urgent messages (>1h old, unanswered)
- Check calendar for events in next 24h
- Review follow-up tracker (overdue items)
- If daytime (8 AM - 10 PM), lightweight check-in
```

**Keep it tiny:**
- Short checklist (5-10 items max)
- No secrets/API keys
- Safe to include every 30 min

**Empty HEARTBEAT.md?**
- Clawdbot skips the run (saves API calls)
- Blank file = effectively disabled

**Visibility control:**
```json
{
  "channels": {
    "defaults": {
      "heartbeat": {
        "showOk": false,      // Hide "HEARTBEAT_OK" acks
        "showAlerts": true,   // Show real alerts
        "useIndicator": true  // Emit status events
      }
    },
    "telegram": {
      "heartbeat": { "showOk": true }  // Override for Telegram
    }
  }
}
```

**Active hours (avoid night spam):**
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "activeHours": { "start": "08:00", "end": "23:00" }
      }
    }
  }
}
```

### Cron Best Practices

**One-shot reminder:**
```bash
clawdbot cron add \
  --name "Send proposal to Alice" \
  --at "20m" \
  --session main \
  --system-event "Reminder: send proposal to Alice." \
  --wake now \
  --delete-after-run
```

**Recurring report (isolated session, WhatsApp delivery):**
```bash
clawdbot cron add \
  --name "Morning briefing" \
  --cron "0 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize inbox + calendar for today." \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"
```

**Model + thinking override (isolated job only):**
```bash
clawdbot cron add \
  --name "Weekly analysis" \
  --cron "0 18 * * 5" \
  --session isolated \
  --message "Deep analysis of campaign performance this week." \
  --model "opus" \
  --thinking high \
  --deliver \
  --channel whatsapp \
  --to "+15551234567"
```

**Telegram topic delivery:**
```bash
clawdbot cron add \
  --name "Nightly summary" \
  --cron "0 22 * * *" \
  --session isolated \
  --message "Daily summary for ops team." \
  --deliver \
  --channel telegram \
  --to "-1001234567890:topic:123"
```

---

## 🛠️ Skills & Tools

### Skill Loading (Precedence)

**Three locations:**
1. `<workspace>/skills` (highest priority) - per-agent overrides
2. `~/.clawdbot/skills` - shared across all agents
3. Bundled skills (lowest) - shipped with Clawdbot

**If same name exists:** workspace → managed → bundled

### Gating (Load-Time Filters)

**Use metadata to gate skills:**
```yaml
---
name: nano-banana-pro
description: Generate or edit images via Gemini
metadata: {
  "clawdbot": {
    "requires": {
      "bins": ["uv"],
      "env": ["GEMINI_API_KEY"],
      "config": ["browser.enabled"]
    },
    "primaryEnv": "GEMINI_API_KEY"
  }
}
---
```

**Gating rules:**
- `requires.bins` - all must exist on PATH
- `requires.anyBins` - at least one must exist
- `requires.env` - env var must exist or be in config
- `requires.config` - config path must be truthy
- `os` - limit to specific platforms (darwin, linux, win32)

**Skip a bundled skill:**
```json
{
  "skills": {
    "entries": {
      "sag": { "enabled": false }
    }
  }
}
```

### Token Impact

**Skills list = XML in system prompt:**
- Base overhead: **195 chars** (when ≥1 skill)
- Per skill: **97 chars** + name + description + location

**Example:**
- 10 skills × ~150 chars each = ~1,700 chars = ~425 tokens

**Best practices:**
- Disable unused bundled skills (`enabled: false`)
- Keep descriptions concise
- Use `allowBundled` to allowlist only needed skills

**Config example:**
```json
{
  "skills": {
    "allowBundled": ["github", "slack", "weather"],
    "entries": {
      "peekaboo": { "enabled": true },
      "sag": { "enabled": false }
    }
  }
}
```

### ClawdHub (Skill Registry)

**Install skills:**
```bash
clawdhub install <skill-name>
clawdhub update --all
clawdhub sync --all
```

**Browse:** https://clawdhub.com

**Auto-install (macOS Skills UI):**
- Skills can define `install` blocks (brew, npm, go, download)
- macOS app shows "Install" button when deps missing
- Gateway picks preferred installer (brew > node > download)

---

## 🔐 Security & Safety

### Boundaries

**Safe to do freely:**
- Read files in workspace
- Search the web
- Check calendar/email
- Organize internal data

**Ask first:**
- Send emails/messages
- Post to social media
- Run destructive commands
- Delete/modify production data

### Group Chat Privacy

**Memory separation:**
- **NEVER** load `MEMORY.md` in group chats
- It contains personal context (API keys, preferences, private notes)
- Only load in main/private DM sessions

**Config enforcement:**
```json
{
  "session": {
    "dmScope": "main",  // DM continuity
    "scope": "per-sender"  // Groups isolated
  }
}
```

**Best practice:**
- Main session = private, full memory access
- Group sessions = isolated, no MEMORY.md

### Allowlists

**WhatsApp example:**
```json
{
  "channels": {
    "whatsapp": {
      "allowFrom": ["+15555550123", "+447716953711"],
      "groups": {
        "*": { "requireMention": true }
      }
    }
  },
  "messages": {
    "groupChat": {
      "mentionPatterns": ["@clawd", "@bot"]
    }
  }
}
```

**Tip:** Start strict, open up as needed.

### Sandboxing

**Three modes:**
1. **Deny** - No exec/elevated tools
2. **Allowlist** - Only approved tools
3. **Full** - All tools (careful!)

**Config:**
```json
{
  "agents": {
    "defaults": {
      "toolPolicy": "allowlist",
      "exec": {
        "enabled": true,
        "allowCommands": ["git", "npm", "node"]
      }
    }
  }
}
```

**For production:**
- Use Docker sandbox (`sandbox.docker.enabled: true`)
- Read-only workspace for untrusted contexts
- Separate agent for risky operations

---

## ⚡ Performance & Costs

### Token Optimization

**1. Session Pruning (automatic)**
- Old tool results trimmed before LLM calls
- Keeps context window manageable
- Doesn't rewrite JSONL history

**2. Compaction**
- Summarizes older messages when nearing limit
- Configurable reserve tokens: `reserveTokensFloor: 20000`
- Memory flush happens before compaction

**3. Heartbeat Cost**
- Every heartbeat = full agent turn
- 30 min interval = ~48 turns/day
- Use cheaper model: `heartbeat.model: "anthropic/claude-haiku-4"`
- Or disable: `heartbeat.every: "0m"`

**4. Skills List**
- Disable unused bundled skills
- Keep skill descriptions short
- Use `allowBundled` allowlist

**Cost comparison (per 1M tokens):**
| Model | Input | Output |
|-------|-------|--------|
| Claude Haiku 4 | $0.80 | $4.00 |
| Claude Sonnet 4.5 | $3.00 | $15.00 |
| Claude Opus 4.5 | $15.00 | $75.00 |

**Heartbeat cost example:**
- 48 heartbeats/day × 5,000 tokens/turn = 240k tokens/day = 7.2M/month
- Sonnet: 7.2M × $3 = **$21.60/mo** (input only)
- Haiku: 7.2M × $0.80 = **$5.76/mo** (input only)

**Optimization:**
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "1h",  // Reduce frequency
        "model": "anthropic/claude-haiku-4"  // Cheaper model
      }
    }
  }
}
```

### Memory Search Costs

**Local embeddings:**
- Free (after initial download ~0.6 GB)
- Slower indexing
- Privacy-friendly

**OpenAI embeddings:**
- `text-embedding-3-small`: **$0.02 per 1M tokens**
- Batch API: 50% discount = **$0.01 per 1M tokens**
- Fast, great quality

**Example:**
- 100 daily files × 2,000 tokens each = 200k tokens
- OpenAI batch: 200k × $0.01 / 1M = **$0.002** (basically free)

**Best practice:** Use OpenAI batch for large initial indexing, then incremental updates are minimal.

---

## 🎯 Common Patterns

### 1. Daily Briefing (Heartbeat)

**HEARTBEAT.md:**
```markdown
# Daily Briefing

Once per day (8-9 AM only):
- Summarize unread emails (last 24h)
- Upcoming calendar events (next 48h)
- Outstanding follow-ups from memory

Reply HEARTBEAT_OK if outside 8-9 AM or nothing urgent.
```

**Config:**
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",
        "activeHours": { "start": "08:00", "end": "09:00" }
      }
    }
  }
}
```

### 2. Weekly Report (Cron, Isolated)

```bash
clawdbot cron add \
  --name "Friday summary" \
  --cron "0 17 * * 5" \
  --tz "Europe/Madrid" \
  --session isolated \
  --message "Weekly summary: calls booked, show rate, closes, top actions for next week." \
  --deliver \
  --channel whatsapp \
  --to "+447716953711"
```

### 3. Post-Call Automation (Cron + System Event)

**After Fathom call ends:**
```bash
# Triggered by webhook or detection
clawdbot cron add \
  --name "Post-call: Alice" \
  --at "5m" \
  --session main \
  --system-event "Generate summary for call with Alice, draft follow-up email." \
  --wake now \
  --delete-after-run
```

**Alternative:** Immediate system event (no job):
```bash
clawdbot system event \
  --mode now \
  --text "Call with Alice just ended. Summarize and draft follow-up."
```

### 4. Pre-Call Research (Calendly Webhook)

**Webhook handler script:**
```bash
#!/bin/bash
NAME="$1"
EMAIL="$2"
CALL_TIME="$3"

clawdbot system event --mode now --text "
Call with ${NAME} booked for ${CALL_TIME}.

Research:
- Company (domain from email)
- Role (LinkedIn via LeadMagic)
- ICP
- Leadership team
- Recent news

Format as brief for me.
"
```

### 5. Client Health Monitoring (Heartbeat)

**HEARTBEAT.md:**
```markdown
# Client Health Monitor

Every 6 hours:
- Check EmailBison reply rates (last 7 days per campaign)
- Flag campaigns with >30% drop vs prior week
- Check for any campaigns with 0 sends in last 24h

If issues found, list them. Otherwise HEARTBEAT_OK.
```

**Rotate through checks:**
```markdown
# Heartbeat rotation

Check ONE of these per run (rotate):
1. Client health (EmailBison stats)
2. Inbox follow-ups (>24h old, no reply)
3. Calendar events (next 48h)
4. Memory review (update MEMORY.md from recent daily files)

Track last check in memory/heartbeat-state.json
```

### 6. Multi-Instance Per Client

**Run separate Clawdbots for major clients:**

```bash
# Client A
CLAWDBOT_STATE_DIR=~/.clawdbot-clientA \
clawdbot gateway --port 19001 &

# Client B
CLAWDBOT_STATE_DIR=~/.clawdbot-clientB \
clawdbot gateway --port 19002 &
```

**Benefits:**
- Isolated memory (no cross-contamination)
- Different models per client
- Separate API limits

---

## 🩺 Troubleshooting

### "Heartbeats aren't running"

**Check:**
1. `heartbeat.every` not set to `0m`
2. Gateway is running continuously (not just one-off commands)
3. Active hours config (might be outside window)
4. HEARTBEAT.md isn't effectively empty

**Debug:**
```bash
clawdbot status  # Shows heartbeat schedule
clawdbot system event --mode now --text "Test heartbeat"
```

### "Cron jobs not firing"

**Check:**
1. `cron.enabled: true` (default)
2. Gateway running
3. Timezone correct (`--tz` vs host timezone)
4. Schedule valid (test with `--at "1m"`)

**Debug:**
```bash
clawdbot cron list
clawdbot cron runs --id <jobId> --limit 10
clawdbot cron run <jobId> --force  # Manual trigger
```

### "Memory search not working"

**Check:**
1. API key configured (OpenAI/Gemini)
2. Index built (`~/.clawdbot/memory/<agentId>.sqlite` exists)
3. Files exist (`MEMORY.md`, `memory/YYYY-MM-DD.md`)

**Debug:**
```bash
clawdbot memory search "test query"
clawdbot memory rebuild  # Force reindex
```

### "Sessions resetting unexpectedly"

**Check:**
1. Reset policy (`session.reset.mode` + `resetByType`)
2. Last activity time (`clawdbot sessions --json`)
3. Manual `/new` or `/reset` commands

**Inspect:**
```bash
clawdbot sessions --json | jq '.[] | select(.sessionKey == "agent:main:main")'
```

### "Skills not loading"

**Check:**
1. Metadata requirements (`requires.bins`, `requires.env`)
2. Skill files valid (`SKILL.md` with frontmatter)
3. Config enablement (`skills.entries.<name>.enabled`)

**Debug:**
```bash
clawdbot skills list --json
clawdbot doctor  # Checks skill issues
```

---

## 📋 Quick Reference Card

### File Structure
```
~/clawd/
├── AGENTS.md         # Workspace conventions
├── SOUL.md           # Persona & tone
├── USER.md           # About your human
├── IDENTITY.md       # Your name, emoji, vibe
├── HEARTBEAT.md      # Heartbeat checklist (optional)
├── MEMORY.md         # Long-term curated memory (main session only)
├── memory/
│   ├── YYYY-MM-DD.md # Daily logs (today + yesterday auto-loaded)
│   └── heartbeat-state.json  # Rotation tracker
├── docs/             # Documentation
└── skills/           # Per-agent skill overrides
```

### Config Locations
- **Main:** `~/.clawdbot/clawdbot.json`
- **Cron store:** `~/.clawdbot/cron/jobs.json`
- **Sessions:** `~/.clawdbot/agents/<agentId>/sessions/sessions.json`
- **Memory index:** `~/.clawdbot/memory/<agentId>.sqlite`

### Essential Commands
```bash
# Status
clawdbot status
clawdbot health
clawdbot sessions --json

# Heartbeat
clawdbot system event --mode now --text "Check inbox"

# Cron
clawdbot cron add --at "20m" --session main --system-event "Reminder text" --wake now
clawdbot cron list
clawdbot cron runs --id <jobId>

# Memory
clawdbot memory search "query"
clawdbot memory rebuild

# Skills
clawdbot skills list
clawdhub install <skill>
clawdhub update --all

# Troubleshooting
clawdbot doctor
clawdbot logs --follow
```

### Chat Commands
```
/new [model]    - Fresh session
/status         - Token usage + context size
/context list   - What's loaded
/compact        - Summarize old messages
/stop           - Abort current run
/reasoning on   - Show thinking process
```

---

## 🎯 For Your Business (Lead Gen)

### Immediate Quick Wins

1. **Post-call summaries** - Fathom automation
2. **Pre-call research** - Calendly → LeadMagic → brief
3. **Email reply agent** - Inbox monitoring + responses
4. **Campaign health heartbeat** - EmailBison monitoring

### Advanced Patterns

5. **Auto-proposal generation** - Call summary → customized proposal
6. **Follow-up sequences** - Memory-tracked, auto-drafted
7. **Client churn detection** - Reply rate drops → proactive outreach
8. **Multi-instance isolation** - Per-client Clawdbots

### Cost Optimization

- Heartbeat on Haiku (~$6/mo vs $22/mo on Sonnet)
- Cron isolated jobs (don't spam main history)
- OpenAI batch embeddings (50% cheaper)
- Disable unused bundled skills

### ROI

**Time savings:** 2-4 hours/day  
**Cost savings:** $2,056/month (Mary + Sharia)  
**Build investment:** ~2 weeks  
**Payback:** Month 1

---

**Last updated:** 2026-01-25  
**Version:** 1.0  
**Source:** Official Clawdbot docs + community patterns
