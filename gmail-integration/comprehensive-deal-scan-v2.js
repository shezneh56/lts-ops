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

// Search queries using newer_than syntax
const SEARCH_QUERIES = [
  // All recent emails first
  'newer_than:60d',
  
  // Discovery calls
  'subject:discovery newer_than:90d',
  'subject:"discovery call" newer_than:90d',
  
  // Proposals
  'subject:proposal newer_than:90d',
  'proposal has:attachment newer_than:90d',
  
  // Leads That Show
  'subject:"Leads That Show" newer_than:90d',
  '"Leads That Show" newer_than:90d',
  
  // Pricing
  'subject:pricing newer_than:90d',
  'pricing package newer_than:90d',
  
  // Follow-ups
  'subject:"follow up" newer_than:90d',
  'subject:"following up" newer_than:90d',
  
  // Calendly/meetings
  'from:calendly newer_than:90d',
  'subject:meeting newer_than:90d',
  
  // Contract
  'subject:contract newer_than:90d',
  'subject:agreement newer_than:90d',
  
  // Demo
  'subject:demo newer_than:90d',
  
  // Intro
  'subject:intro newer_than:90d',
];

// Exclusion patterns
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
  'emailbison.com',
  'zendesk.com',
  'intercom.io',
  'mailchimp.com',
  'sendgrid.net',
];

const EXCLUDE_PATTERNS = [
  'noreply',
  'no-reply',
  'notifications@',
  'support@',
  'team@',
  'hello@',
  'info@',
  'marketing@',
  'news@',
  'updates@',
  'billing@',
  'mailer-daemon',
];

async function searchMessages(query, maxResults = 200) {
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
  return match ? match[1].toLowerCase().trim() : fromString.toLowerCase().trim();
}

function extractName(fromString) {
  const match = fromString.match(/^"?([^"<]+)"?\s*</);
  if (match) return match[1].trim();
  const emailMatch = fromString.match(/([^\s@]+)@/);
  return emailMatch ? emailMatch[1] : fromString;
}

function extractCompany(email, subject) {
  const domain = email.split('@')[1];
  if (domain) {
    const company = domain.split('.')[0];
    return company.charAt(0).toUpperCase() + company.slice(1);
  }
  return 'Unknown';
}

function shouldExclude(email) {
  if (!email) return true;
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
  if (!email) return false;
  const lowerEmail = email.toLowerCase();
  return lowerEmail.includes('leadsthatshow.com') || 
         lowerEmail.includes('liam') ||
         lowerEmail.includes('lts');
}

// Parse Calendly subject to extract prospect info
function parseCalendlySubject(subject) {
  // Pattern: "Name - Time - Leads That Show - Discovery"
  const match = subject.match(/^(?:Updated: |Canceled: )?([^-]+)\s*-\s*[\d:apm\s]+\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)/i);
  if (match) {
    return match[1].trim();
  }
  return null;
}

async function main() {
  console.log('🔍 Starting comprehensive deal scan v2...\n');
  
  const allMessageIds = new Set();
  const prospects = new Map(); // email -> prospect data
  
  // Run all searches
  for (const query of SEARCH_QUERIES) {
    console.log(`Searching: ${query.substring(0, 60)}...`);
    const messages = await searchMessages(query, 200);
    console.log(`  Found ${messages.length} messages`);
    
    for (const m of messages) {
      allMessageIds.add(m.id);
    }
    
    await new Promise(r => setTimeout(r, 100));
  }
  
  console.log(`\n📧 Total unique messages to process: ${allMessageIds.size}\n`);
  
  // Process all messages
  let processed = 0;
  for (const msgId of allMessageIds) {
    processed++;
    if (processed % 20 === 0) {
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
    
    const fromEmail = extractEmail(from);
    const fromName = extractName(from);
    
    // Handle Calendly notifications specially
    if (fromEmail.includes('calendly')) {
      const prospectName = parseCalendlySubject(subject);
      if (prospectName) {
        // Look for the prospect in To/CC or create placeholder
        console.log(`  Calendly event: ${prospectName}`);
      }
      continue; // Skip adding Calendly as prospect
    }
    
    const fromUs = isFromUs(fromEmail);
    
    let prospectEmail, prospectName;
    
    if (fromUs) {
      // Outbound
      const toEmail = extractEmail(to);
      if (shouldExclude(toEmail)) continue;
      prospectEmail = toEmail;
      prospectName = extractName(to);
    } else {
      // Inbound
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
        emails: [],
        lastDate: internalDate,
        lastSubject: subject,
        lastFromUs: fromUs,
        hasProposal: false,
        hasDiscovery: false,
        hasPricing: false,
        hasContract: false,
        hasCalendly: false,
        responseCount: 0,
        outboundCount: 0,
      });
    }
    
    const prospect = prospects.get(prospectEmail);
    
    // Update last email if newer
    if (internalDate > prospect.lastDate) {
      prospect.lastDate = internalDate;
      prospect.lastSubject = subject;
      prospect.lastFromUs = fromUs;
    }
    
    // Track direction
    if (fromUs) {
      prospect.outboundCount++;
    } else {
      prospect.responseCount++;
    }
    
    // Update name
    if (prospectName && prospectName.length > prospect.name.length && !prospectName.includes('@')) {
      prospect.name = prospectName;
    }
    
    // Check signals
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
    if (lowerSubject.includes('contract') || lowerSubject.includes('agreement')) {
      prospect.hasContract = true;
    }
    if (lowerSubject.includes('calendly') || snippet.includes('calendly')) {
      prospect.hasCalendly = true;
    }
    
    // Store email summary
    prospect.emails.push({
      date: new Date(internalDate).toISOString(),
      subject: subject,
      fromUs: fromUs,
      snippet: msg.snippet?.substring(0, 200)
    });
    
    if (!prospect.threads.includes(msg.threadId)) {
      prospect.threads.push(msg.threadId);
    }
    
    await new Promise(r => setTimeout(r, 30));
  }
  
  console.log(`\n✅ Found ${prospects.size} unique prospects\n`);
  
  // Categorize
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
  
  for (const [email, p] of prospects) {
    const daysSinceContact = Math.floor((now - p.lastDate) / (24 * 60 * 60 * 1000));
    const hasBackAndForth = p.responseCount > 0 && p.outboundCount > 0;
    
    let status = 'UNKNOWN';
    
    if (p.hasContract) {
      status = hasBackAndForth ? 'WON' : 'NEGOTIATION';
    } else if (p.hasProposal && hasBackAndForth && daysSinceContact < 7) {
      status = 'NEGOTIATION';
    } else if (p.hasProposal && daysSinceContact >= 7 && p.lastFromUs) {
      status = 'COLD';
    } else if (p.hasProposal) {
      status = 'PROPOSAL_SENT';
    } else if (p.hasDiscovery && p.hasPricing) {
      status = daysSinceContact < 7 ? 'NEGOTIATION' : 'PROPOSAL_SENT';
    } else if (p.hasDiscovery) {
      status = daysSinceContact < 7 ? 'DISCOVERY_DONE' : 'COLD';
    } else if (p.hasCalendly || (hasBackAndForth && daysSinceContact < 14)) {
      status = 'DISCOVERY_BOOKED';
    } else if (daysSinceContact >= 7 && p.lastFromUs) {
      status = 'COLD';
    } else if (hasBackAndForth) {
      status = 'NEGOTIATION';
    } else {
      status = 'UNKNOWN';
    }
    
    p.status = status;
    p.daysSinceContact = daysSinceContact;
    
    categorized[status].push(p);
  }
  
  // Sort by recency
  for (const status of Object.keys(categorized)) {
    categorized[status].sort((a, b) => b.lastDate - a.lastDate);
  }
  
  // Output
  const output = {
    scanDate: new Date().toISOString(),
    totalProspects: prospects.size,
    totalMessages: allMessageIds.size,
    categorized,
    allProspects: Array.from(prospects.values())
  };
  
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
      console.log(`  Subject: ${p.lastSubject.substring(0, 70)}`);
      console.log(`  Signals: ${[
        p.hasDiscovery ? '📞 Discovery' : '',
        p.hasProposal ? '📄 Proposal' : '',
        p.hasPricing ? '💰 Pricing' : '',
        p.hasContract ? '✍️ Contract' : '',
        p.hasCalendly ? '📅 Calendly' : ''
      ].filter(Boolean).join(', ') || 'None'}`);
      console.log(`  Activity: ${p.outboundCount} sent, ${p.responseCount} received`);
      console.log(`  Days since: ${p.daysSinceContact}`);
      console.log('');
    }
  }
}

main().catch(console.error);
