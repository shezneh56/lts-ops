# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Campaign Management Tools

### EmailBison MCP & Campaign Engine
**Location:** `/root/clawd/claude-code-projects`

**Installed packages:**
- `campaign-engine` - Core campaign engine with deliverability tracking
- `mcp-emailbison` - MCP server for EmailBison API (for Claude CLI)

**Daily Digest:**
```bash
cd /root/clawd/claude-code-projects
python3 -m campaign_engine.deliverability.daily_digest --format json
python3 -m campaign_engine.deliverability.daily_digest --command "REFRESH {STEP_ID}"
```

**Available commands:**
- `REFRESH {STEP_ID}` - Get copy for a flagged step
- `DETAIL {CAMPAIGN_ID}` - Get detailed campaign stats
- `HEALTH` - Check inbox health across workspaces
- `STATUS` - Overall system status

**Config files:**
- API keys: `config/workspace_keys.json`
- Daily digest outputs to console (JSON or text)

**Auto-refresh flow:**
See `/root/clawd/docs/auto-refresh-flow.md` for the complete workflow when variants are flagged for fingerprinting.

**Direct API access (via Python):**
Can use `src/campaign_engine/deliverability/emailbison_client.py` for programmatic access to EmailBison API.

**Workspaces:**
- C2 - C2 Experience
- CGS - CGS Team
- Gestell - Gestell
- Hygraph - Hygraph
- Jampot - Jam Pot
- Lawtech - LawTech
- LTS - Leads That Show
- Legalsoft - LegalSoft
- Medvirtual - Med Virtual
- Paralect - Paralect
- Wow24-7 - Wow 24-7

---

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
