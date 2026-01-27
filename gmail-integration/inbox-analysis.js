const {google} = require('googleapis');
const fs = require('fs');

const credentials = JSON.parse(fs.readFileSync('credentials.json'));
const token = JSON.parse(fs.readFileSync('token.json'));

const auth = new google.auth.OAuth2(
  credentials.installed.client_id,
  credentials.installed.client_secret,
  credentials.installed.redirect_uris[0]
);
auth.setCredentials(token);
const gmail = google.gmail({version: 'v1', auth});

async function searchMessages(query, maxResults = 50) {
  try {
    const res = await gmail.users.messages.list({
      userId: 'me',
      q: query,
      maxResults: maxResults
    });
    return res.data.messages || [];
  } catch (err) {
    console.error(`Error searching "${query}":`, err.message);
    return [];
  }
}

async function getMessage(id) {
  try {
    const res = await gmail.users.messages.get({
      userId: 'me',
      id: id,
      format: 'metadata',
      metadataHeaders: ['From', 'To', 'Subject', 'Date']
    });
    return res.data;
  } catch (err) {
    console.error(`Error getting message ${id}:`, err.message);
    return null;
  }
}

function getHeader(msg, name) {
  const header = msg.payload.headers.find(h => h.name.toLowerCase() === name.toLowerCase());
  return header ? header.value : '';
}

async function main() {
  const queries = [
    { name: 'unread', query: 'is:inbox is:unread' },
    { name: 'last7days', query: 'is:inbox newer_than:7d' },
    { name: 'calendly', query: 'is:inbox from:calendly newer_than:30d' },
    { name: 'replies', query: 'is:inbox subject:re: newer_than:14d' },
    { name: 'leadSignals', query: 'is:inbox (meeting OR call OR schedule OR interested OR pricing OR proposal) newer_than:14d' }
  ];

  const results = {};
  
  for (const q of queries) {
    console.log(`\n=== ${q.name.toUpperCase()} ===`);
    const messages = await searchMessages(q.query);
    console.log(`Found ${messages.length} messages`);
    
    const details = [];
    for (const m of messages.slice(0, 30)) {
      const msg = await getMessage(m.id);
      if (msg) {
        const from = getHeader(msg, 'From');
        const subject = getHeader(msg, 'Subject');
        const date = getHeader(msg, 'Date');
        const to = getHeader(msg, 'To');
        details.push({ id: m.id, from, to, subject, date, snippet: msg.snippet, labelIds: msg.labelIds });
        console.log(`[${date}] From: ${from}`);
        console.log(`  Subject: ${subject}`);
        console.log(`  Snippet: ${msg.snippet.substring(0, 100)}...`);
        console.log('');
      }
    }
    results[q.name] = details;
  }
  
  // Output JSON for further processing
  console.log('\n=== JSON OUTPUT ===');
  console.log(JSON.stringify(results, null, 2));
}

main();
