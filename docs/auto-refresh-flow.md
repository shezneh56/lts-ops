# Auto-Refresh Flow for Email Campaigns

## When to Trigger
A variant is flagged for fingerprinting when:
- Reply drop >50%
- Minimum 50 sends (enough data)
- Not already refreshed in last 7 days

## Step 1: Fetch the Flagged Copy
```bash
python -m campaign_engine.deliverability.daily_digest --command "REFRESH {STEP_ID}"
```

Returns: current subject, body, campaign_id, and workspace.

## Step 2: Rewrite the Copy
Use this prompt on the flagged copy:

```
Rewrite this cold email. It has been flagged for fingerprinting.

RULES:
- SAME offer, angle, meaning, and CTA - do not change what it says
- DIFFERENT wording - new sentence structure, vocabulary, phrasing
- Keep ultra-short (2-4 lines max)
- Add spintax: {{option1|option2|option3}} with 3 options per variable element
- Subject line: 8 spintax options
- Avoid spam words (guarantee, free, act now, limited time)
- No "performance-based" or "pay-per-meeting" language
- Keep P.S. concept but reword it

ORIGINAL:
Subject: {SUBJECT}
Body: {BODY}

OUTPUT:
One rewritten version with subject and body in HTML format.
```

## Step 3: Deploy the Rewrite

### Get sequence_id:
```bash
curl -X GET "https://send.leadsthat.show/api/campaigns/v1.1/{CAMPAIGN_ID}/sequence-steps" \
  -H "Authorization: Bearer {API_KEY}"
```

### Deploy via PUT:
```bash
curl -X PUT "https://send.leadsthat.show/api/campaigns/v1.1/sequence-steps/{SEQUENCE_ID}" \
  -H "Authorization: Bearer {API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{CAMPAIGN_NAME}",
    "sequence_steps": [{
      "id": {STEP_ID},
      "email_subject": "{NEW_SUBJECT}",
      "email_body": "{NEW_BODY}",
      "order": 1,
      "variant": true,
      "variant_from_step_id": {PARENT_STEP_ID},
      "wait_in_days": 1,
      "thread_reply": false
    }]
  }'
```

## Step 4: Confirm to User
Send WhatsApp message:
```
✅ Auto-refresh completed

Step {STEP_ID} in {CAMPAIGN_NAME} was flagged (dropped {DROP}%).

Rewritten and deployed:
• New subject: {FIRST 40 CHARS}...
• Same angle, different wording
• Spintax added

Will monitor performance over next 48hrs.
```

## API Keys
Location: `config/workspace_keys.json`

See `/root/clawd/docs/emailbison-workspaces.md` for the complete list of all 11 configured workspaces.

## When NOT to Auto-Refresh
- Step has <50 sends (insufficient data)
- Drop is <50% (normal variance)
- Already refreshed in last 7 days (check git history)
