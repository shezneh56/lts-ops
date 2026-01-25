# EmailBison Workspaces

## All Configured Workspaces

The following 11 workspaces are configured in `config/workspace_keys.json`:

| ID | Short Name | Full Name |
|----|------------|-----------|
| 16 | C2 | C2 Experience |
| 4 | CGS | CGS Team |
| 8 | Gestell | Gestell |
| 15 | Hygraph | Hygraph |
| 6 | Jampot | Jam Pot |
| 3 | Lawtech | LawTech |
| 2 | LTS | Leads That Show |
| 7 | Legalsoft | LegalSoft |
| 17 | Medvirtual | Med Virtual |
| 12 | Paralect | Paralect |
| 5 | Wow24-7 | Wow 24-7 |

## Usage

When using the daily digest or EmailBison tools, reference workspaces by their **short name** (case-insensitive).

### Examples:

```bash
# Daily digest for specific workspace
python3 -m campaign_engine.deliverability.daily_digest --workspace LTS --format json

# Get campaigns for a workspace
python3 -m campaign_engine.deliverability.emailbison_client --workspace Gestell list-campaigns

# Refresh flagged step
python3 -m campaign_engine.deliverability.daily_digest --command "REFRESH {STEP_ID}"
```

## API Configuration

All workspaces use the same base URL:
- **Base URL:** `https://send.leadsthat.show/api`

Each workspace has its own API key stored securely in `config/workspace_keys.json`.
