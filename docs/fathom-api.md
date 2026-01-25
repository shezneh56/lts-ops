# Fathom API Integration

## API Configuration

**Base URL:** `https://api.fathom.ai/external/v1`

**Authentication:**
- Header: `X-Api-Key`
- Value: Stored in `/root/clawd/gmail-integration/.env` as `FATHOM_API_KEY`

**Webhook Secret:** Stored as `FATHOM_WEBHOOK_SECRET` (for future webhook integration)

## Endpoints

### GET /meetings
Fetch meeting recordings with pagination.

**Parameters:**
- `limit` (number): Max results per page (default: 50, max: 100)
- `cursor` (string, optional): Pagination cursor for next page

**Response:**
```json
{
  "items": [
    {
      "title": "Discovery Call: John Doe",
      "recording_start_time": "2026-01-20T10:00:00Z",
      "recording_end_time": "2026-01-20T10:30:00Z",
      "url": "https://app.fathom.video/...",
      // ... other fields
    }
  ],
  "next_cursor": "abc123..."
}
```

## Example Usage

```javascript
const axios = require('axios');

const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const FATHOM_API = 'https://api.fathom.ai/external/v1';

async function getMeetings(limit = 50, cursor = null) {
  const params = { limit };
  if (cursor) params.cursor = cursor;
  
  const response = await axios.get(`${FATHOM_API}/meetings`, {
    headers: { 'X-Api-Key': FATHOM_API_KEY },
    params
  });
  
  return response.data;
}
```

## Helper Scripts

### fathom-api.js
Core API wrapper with helper functions:
- `getMeetings(limit, cursor)` - Fetch meetings with pagination
- `getWeeklySalesCalls()` - Get sales calls from current week
- `isSalesCall(title)` - Filter logic for sales vs client calls

**Usage:**
```bash
cd /root/clawd/gmail-integration
node fathom-api.js
```

### Weekly Sales Calls
Automatically filters for:
- ✅ "Discovery Call" in title
- ✅ "Leads That Show - Discovery" event type
- ❌ Excludes "Client Call"

Returns array with: name, title, recordingTime, duration, url

## Integration Status

- ✅ API working and tested
- ✅ Used in weekly metrics automation
- ⏳ Post-call automation (transcripts, summaries) - pending
- ⏳ Auto-update call tracker from recordings - pending

## Notes

- Fathom orders meetings by `recording_start_time` (newest first)
- Sales call detection: filters by title keywords
- Pagination: use `next_cursor` to fetch more pages
- Weekly boundaries: Monday 00:00 - Sunday 23:59
