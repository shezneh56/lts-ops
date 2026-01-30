#!/usr/bin/env node
const {google} = require('googleapis');
const fs = require('fs');

const credentials = JSON.parse(fs.readFileSync(__dirname + '/credentials.json'));
const token = JSON.parse(fs.readFileSync(__dirname + '/token.json'));

const auth = new google.auth.OAuth2(
  credentials.installed.client_id,
  credentials.installed.client_secret,
  credentials.installed.redirect_uris[0]
);
auth.setCredentials(token);
const gmail = google.gmail({version: 'v1', auth});

const DEALS = [
  { company: 'KingsView', contact: 'Harold Wenger Jr', email: 'hwengerjr@kingsview.com' },
  { company: 'Krixi', contact: 'Sandeep Agate', email: 'sandeep.agate@krixi.com' },
  { company: 'Nectus', contact: 'Dmitry Zaitsev', email: 'dzaitsev@nectus5.com' },
  { company: 'DQS Africa', contact: 'Francois Labuschagne', email: 'francois.labuschagne@dqs.de' },
  { company: 'ECOSubSea', contact: 'Theodor Larsen', email: 'theodor.larsen@ecosubsea.com' },
  { company: 'TXRE Properties', contact: 'Justin Smith', email: 'jsmith@txreproperties.com' },
  { company: 'Logistics One', contact: 'John Madden', email: 'jmadden@logisticsone.com' },
  { company: 'CE One Source', contact: 'R Bess', email: 'rbess@dayonesolutions.io' },
  { company: 'AppNerve', contact: 'Kalyan A', email: 'kalyan@appnerve.com' },
  { company: 'Hesper Consulting', contact: 'Nate Hepner', email: null },
  { company: 'Asuene', contact: 'Chan Lee', email: 'chan.lee@asuene.com' },
  { company: 'Byld Commerce', contact: 'Spencer', email: null },
];

async function searchMessages(query, maxResults = 20) {
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
      format: 'full',
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

async function searchDeal(deal) {
  let query;
  if (deal.email) {
    query = `(from:${deal.email} OR to:${deal.email}) newer_than:45d`;
  } else {
    // Search by name and company
    const searchTerms = deal.contact.split(' ').filter(w => w.length > 2).join(' OR ');
    query = `(${searchTerms} OR ${deal.company}) newer_than:45d`;
  }
  
  console.log(`\n=== ${deal.company.toUpperCase()} (${deal.contact}) ===`);
  console.log(`Query: ${query}`);
  
  const messages = await searchMessages(query, 15);
  console.log(`Found ${messages.length} messages`);
  
  const emails = [];
  for (const m of messages.slice(0, 10)) {
    const msg = await getMessage(m.id);
    if (msg) {
      const from = getHeader(msg, 'From');
      const to = getHeader(msg, 'To');
      const subject = getHeader(msg, 'Subject');
      const date = getHeader(msg, 'Date');
      
      // Determine if from them or us
      const fromThem = deal.email ? from.toLowerCase().includes(deal.email.toLowerCase()) : 
        from.toLowerCase().includes(deal.contact.split(' ')[0].toLowerCase());
      
      emails.push({
        id: m.id,
        from,
        to,
        subject,
        date,
        snippet: msg.snippet,
        fromThem,
        internalDate: parseInt(msg.internalDate)
      });
      
      console.log(`[${date}] ${fromThem ? '← THEM' : '→ US'}`);
      console.log(`  From: ${from}`);
      console.log(`  Subject: ${subject}`);
      console.log(`  Snippet: ${msg.snippet.substring(0, 120)}...`);
      console.log('');
    }
  }
  
  return {
    deal,
    emails,
    lastEmail: emails[0] || null,
    count: messages.length
  };
}

async function main() {
  const results = [];
  
  for (const deal of DEALS) {
    const result = await searchDeal(deal);
    results.push(result);
    // Small delay to avoid rate limits
    await new Promise(r => setTimeout(r, 200));
  }
  
  console.log('\n\n=== SUMMARY JSON ===');
  console.log(JSON.stringify(results, null, 2));
}

main().catch(console.error);
