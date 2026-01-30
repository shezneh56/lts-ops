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

// Search queries to find ALL prospects
const SEARCH_QUERIES = [
  // Discovery calls
  'subject:discovery after:2024/12/01 before:2025/01/31',
  'subject:"discovery call" after:2024/12/01 before:2025/01/31',
  
  // Proposals
  'subject:proposal after:2024/12/01 before:2025/01/31',
  '"proposal" has:attachment after:2024/12/01 before:2025/01/31',
  
  // Leads That Show
  'subject:"Leads That Show" after:2024/12/01 before:2025/01/31',
  '"Leads That Show" after:2024/12/01 before:2025/01/31',
  
  // Pricing discussions
  'subject:pricing after:2024/12/01 before:2025/01/31',
  '"pricing" "package" after:2024/12/01 before:2025/01/31',
  
  // Follow-ups and meetings
  'subject:"follow up" after:2024/12/01 before:2025/01/31',
  'subject:"following up" after:2024/12/01 before:2025/01/31',
  
  // Calendly/meetings
  '"calendly" after:2024/12/01 before:2025/01/31',
  'subject:meeting after:2024/12/01 before:2025/01/31',
  
  // Contract/agreement
  'subject:contract after:2024/12/01 before:2025/01/31',
  'subject:agreement after:2024/12/01 before:2025/01/31',
  
  // Demo
  'subject:demo after:2024/12/01 before:2025/01/31',
  
  // Quick intro / outreach
  'subject:"quick intro" after:2024/12/01 before:2025/01/31',
  'subject:intro after:2024/12/01 before:2025/01/31',
  
  // SDR outreach patterns
  '("interested in" OR "love to chat") after:2024/12/01 before:2025/01/31',
];

// Exclusion patterns (internal, newsletters, etc.)
const EXCLUDE_DOMAINS = [
  'leadsthatshow.com',
  'google.com',
  'calendly.com',
  'fathom.video',
  'hubspot.com',
  'apollo.io',
  'linkedin.com',
  'stripe.com',
  'slack.com',
  'notion.so',
  'gmail.com', // Often internal
  'emailbison.com',
];

const EXCLUDE_PATTERNS = [
  'noreply',
  'no-reply',
  'notifications',
  'support@',
  'team@',
  'hello@',
  'info@',
  'marketing@',
  'news@',
  'updates@',
];

async function searchMessages(query, maxResults = 100) {
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
      format: 'full'
    });
    return res.data;
  } catch (err) {
    console.error(`Error getting message ${id}:`, err.message);
    return null;
  }
}

function getHeader(msg, name) {
  const header = msg.payload?.headers?.find(h => h.name.toLowerCase() === name.toLowerCase());
  return header ? header.value : '';
}

function extractEmail(fromString) {
  const match = fromString.match(/<([^>]+)>/) || fromString.match(/([^\s<>]+@[^\s<>]+)/);
  return match ? match[1].toLowerCase() : fromString.toLowerCase();
}

function extractName(fromString) {
  const match = fromString.match(/^"?([^"<]+)"?\s*</);
  if (match) return match[1].trim();
  const emailMatch = fromString.match(/([^\s@]+)@/);
  return emailMatch ? emailMatch[1] : fromString;
}

function extractCompany(email, subject) {
  // Try to get company from email domain
  const domain = email.split('@')[1];
  if (domain) {
    const company = domain.split('.')[0];
    // Capitalize first letter
    return company.charAt(0).toUpperCase() + company.slice(1);
  }
  return 'Unknown';
}

function shouldExclude(email) {
  const lowerEmail = email.toLowerCase();
  
  for (const domain of EXCLUDE_DOMAINS) {
    if (lowerEmail.includes(domain)) return true;
  }
  
  for (const pattern of EXCLUDE_PATTERNS) {
    if (lowerEmail.includes(pattern)) return true;
  }
  
  return false;
}

function isFromUs(email) {
  const lowerEmail = email.toLowerCase();
  return lowerEmail.includes('leadsthatshow.com') || 
         lowerEmail.includes('liam@') ||
         lowerEmail.includes('liamhague');
}

async function main() {
  console.log('🔍 Starting comprehensive deal scan...\n');
  
  const allMessageIds = new Set();
  const prospects = new Map(); // email -> prospect data
  
  // Run all searches
  for (const query of SEARCH_QUERIES) {
    console.log(`Searching: ${query.substring(0, 60)}...`);
    const messages = await searchMessages(query, 100);
    console.log(`  Found ${messages.length} messages`);
    
    for (const m of messages) {
      allMessageIds.add(m.id);
    }
    
    // Small delay
    await new Promise(r => setTimeout(r, 100));
  }
  
  console.log(`\n📧 Total unique messages to process: ${allMessageIds.size}\n`);
  
  // Process all messages
  let processed = 0;
  for (const msgId of allMessageIds) {
    processed++;
    if (processed % 50 === 0) {
      console.log(`Processing ${processed}/${allMessageIds.size}...`);
    }
    
    const msg = await getMessage(msgId);
    if (!msg) continue;
    
    const from = getHeader(msg, 'From');
    const to = getHeader(msg, 'To');
    const cc = getHeader(msg, 'Cc');
    const subject = getHeader(msg, 'Subject');
    const date = getHeader(msg, 'Date');
    const internalDate = parseInt(msg.internalDate);
    
    // Extract the prospect email (whoever isn't us)
    const fromEmail = extractEmail(from);
    const fromName = extractName(from);
    
    // Determine if this is inbound or outbound
    const fromUs = isFromUs(fromEmail);
    
    // Get prospect email
    let prospectEmail, prospectName;
    
    if (fromUs) {
      // Outbound - get recipient
      const toEmail = extractEmail(to);
      if (shouldExclude(toEmail)) continue;
      prospectEmail = toEmail;
      prospectName = extractName(to);
    } else {
      // Inbound - from is prospect
      if (shouldExclude(fromEmail)) continue;
      prospectEmail = fromEmail;
      prospectName = fromName;
    }
    
    if (!prospectEmail || prospectEmail.length < 5) continue;
    
    // Add or update prospect
    if (!prospects.has(prospectEmail)) {
      prospects.set(prospectEmail, {
        email: prospectEmail,
        name: prospectName,
        company: extractCompany(prospectEmail, subject),
        threads: [],
        lastDate: internalDate,
        lastSubject: subject,
        lastFromUs: fromUs,
        hasProposal: false,
        hasDiscovery: false,
        hasPricing: false,
        hasContract: false,
        responseCount: 0, // Emails from them
        outboundCount: 0, // Emails from us
      });
    }
    
    const prospect = prospects.get(prospectEmail);
    
    // Update last email if newer
    if (internalDate > prospect.lastDate) {
      prospect.lastDate = internalDate;
      prospect.lastSubject = subject;
      prospect.lastFromUs = fromUs;
    }
    
    // Track email direction
    if (fromUs) {
      prospect.outboundCount++;
    } else {
      prospect.responseCount++;
    }
    
    // Update name if we have a better one
    if (prospectName && prospectName.length > prospect.name.length && !prospectName.includes('@')) {
      prospect.name = prospectName;
    }
    
    // Check for deal signals
    const lowerSubject = subject.toLowerCase();
    const snippet = (msg.snippet || '').toLowerCase();
    
    if (lowerSubject.includes('proposal') || snippet.includes('proposal')) {
      prospect.hasProposal = true;
    }
    if (lowerSubject.includes('discovery') || snippet.includes('discovery call')) {
      prospect.hasDiscovery = true;
    }
    if (lowerSubject.includes('pricing') || snippet.includes('pricing') || snippet.includes('package')) {
      prospect.hasPricing = true;
    }
    if (lowerSubject.includes('contract') || lowerSubject.includes('agreement') || snippet.includes('sign')) {
      prospect.hasContract = true;
    }
    
    // Add thread reference
    if (!prospect.threads.includes(msg.threadId)) {
      prospect.threads.push(msg.threadId);
    }
    
    // Small delay
    await new Promise(r => setTimeout(r, 50));
  }
  
  console.log(`\n✅ Found ${prospects.size} unique prospects\n`);
  
  // Categorize prospects
  const categorized = {
    WON: [],
    NEGOTIATION: [],
    PROPOSAL_SENT: [],
    DISCOVERY_DONE: [],
    DISCOVERY_BOOKED: [],
    COLD: [],
    LOST: [],
    ON_HOLD: [],
    UNKNOWN: []
  };
  
  const now = Date.now();
  const sevenDaysAgo = now - (7 * 24 * 60 * 60 * 1000);
  
  for (const [email, p] of prospects) {
    // Determine status based on signals
    let status = 'UNKNOWN';
    
    const daysSinceContact = Math.floor((now - p.lastDate) / (24 * 60 * 60 * 1000));
    const hasBackAndForth = p.responseCount > 0 && p.outboundCount > 0;
    const noResponse = p.responseCount === 0;
    
    if (p.hasContract) {
      status = hasBackAndForth ? 'WON' : 'NEGOTIATION';
    } else if (p.hasProposal && hasBackAndForth && daysSinceContact < 7) {
      status = 'NEGOTIATION';
    } else if (p.hasProposal && !hasBackAndForth) {
      status = 'PROPOSAL_SENT';
    } else if (p.hasProposal && daysSinceContact >= 7) {
      status = p.lastFromUs ? 'COLD' : 'NEGOTIATION';
    } else if (p.hasDiscovery && p.hasPricing) {
      status = daysSinceContact < 7 ? 'NEGOTIATION' : 'PROPOSAL_SENT';
    } else if (p.hasDiscovery) {
      status = daysSinceContact < 7 ? 'DISCOVERY_DONE' : 'COLD';
    } else if (hasBackAndForth) {
      status = daysSinceContact < 7 ? 'DISCOVERY_BOOKED' : 'COLD';
    } else if (noResponse && daysSinceContact >= 7) {
      status = 'COLD';
    } else {
      status = 'UNKNOWN';
    }
    
    p.status = status;
    p.daysSinceContact = daysSinceContact;
    
    categorized[status].push(p);
  }
  
  // Sort each category by last contact date
  for (const status of Object.keys(categorized)) {
    categorized[status].sort((a, b) => b.lastDate - a.lastDate);
  }
  
  // Output results
  const output = {
    scanDate: new Date().toISOString(),
    totalProspects: prospects.size,
    totalMessages: allMessageIds.size,
    categorized,
    allProspects: Array.from(prospects.values())
  };
  
  // Write JSON
  fs.writeFileSync('/root/clawd/all-deals-scan-raw.json', JSON.stringify(output, null, 2));
  console.log('📁 Raw data saved to /root/clawd/all-deals-scan-raw.json');
  
  // Print summary
  console.log('\n=== SUMMARY ===\n');
  for (const [status, list] of Object.entries(categorized)) {
    if (list.length > 0) {
      console.log(`${status}: ${list.length} prospects`);
    }
  }
  
  console.log('\n=== ALL PROSPECTS BY STATUS ===\n');
  
  for (const [status, list] of Object.entries(categorized)) {
    if (list.length === 0) continue;
    
    console.log(`\n### ${status} (${list.length}) ###\n`);
    
    for (const p of list) {
      const dateStr = new Date(p.lastDate).toLocaleDateString();
      const direction = p.lastFromUs ? '→ We sent' : '← They replied';
      console.log(`${p.name} (${p.company})`);
      console.log(`  Email: ${p.email}`);
      console.log(`  Last: ${dateStr} - ${direction}`);
      console.log(`  Subject: ${p.lastSubject.substring(0, 60)}`);
      console.log(`  Signals: ${[
        p.hasDiscovery ? '📞 Discovery' : '',
        p.hasProposal ? '📄 Proposal' : '',
        p.hasPricing ? '💰 Pricing' : '',
        p.hasContract ? '✍️ Contract' : ''
      ].filter(Boolean).join(', ') || 'None'}`);
      console.log(`  Activity: ${p.outboundCount} sent, ${p.responseCount} received`);
      console.log(`  Days since contact: ${p.daysSinceContact}`);
      console.log('');
    }
  }
}

main().catch(console.error);
