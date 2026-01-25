# EmailBison MCP Setup

## Installation Steps

### 1. Clone/Update Repository
```bash
cd /root/clawd
git clone https://github.com/shezneh56/claude-code-projects.git
# OR if already cloned:
cd claude-code-projects && git pull origin master
```

### 2. Install the MCP
```bash
cd claude-code-projects/mcp-emailbison
pip install -e .
```

### 3. Add MCP to Claude CLI
```bash
claude mcp add emailbison -- python /root/clawd/claude-code-projects/mcp-emailbison/src/server.py
```

### 4. Verify Installation
```bash
claude mcp list
```

## Available Tools

### Campaign Management
- `emailbison_list_campaigns` - List active campaigns
- `emailbison_get_campaign_steps` - Get sequence steps
- `emailbison_get_step_content` - Get full step details
- `emailbison_get_campaign_stats` - Get per-step stats
- `emailbison_pause_campaign` - Pause campaign
- `emailbison_resume_campaign` - Resume campaign
- `emailbison_get_sender_emails` - List sender emails with health scores

### Step Modification (Dry-run by Default)
- `emailbison_update_step` - Update step copy
- `emailbison_create_step` - Create new step

## Safety Features
⚠️ **Important**: `emailbison_update_step` and `emailbison_create_step` require `confirm=true` to execute.

- Without `confirm=true`, they return a **dry-run preview** showing what WOULD change
- This prevents accidental modifications to live campaign copy
- Always review dry-run output before confirming

## Example Usage
```bash
# Safe - shows preview only
emailbison_update_step --step-id 123 --subject "New subject"

# Actually executes
emailbison_update_step --step-id 123 --subject "New subject" --confirm true
```
