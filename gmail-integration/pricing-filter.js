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
  { company: 'NAI Capital', contact: 'Barry Rothstein', searchTerms: ['NAI Capital', 'Barry Rothstein', 'naicapital'] },
  { company: 'Focus GTS', contact: 'Dave Fox', searchTerms: ['Focus GTS', 'Dave Fox', 'focusgts'] },
  { company: 'Solutions Review', contact: 'Conor Carignan', searchTerms: ['Solutions Review', 'Conor Carignan', 'solutionsreview'] },
  { company: 'KingsView', contact: 'Harold Wenger Jr', searchTerms: ['KingsView', 'Harold Wenger', 'hwengerjr@kingsview.com'] },
  { company: 'Wavity', contact: 'Kent Harkins', searchTerms: ['Wavity', 'Kent Harkins'] },
  { company: 'Roles Pilot', contact: 'Dylan Whalen', searchTerms: ['Roles Pilot', 'Dylan Whalen', 'rolespilot'] },
  { company: 'DQS Africa', contact: 'Francois Labuschagne', searchTerms: ['DQS Africa', 'Francois Labuschagne', 'francois.labuschagne@dqs'] },
  { company: 'CE One Source', contact: 'Robert Bess', searchTerms: ['CE One Source', 'Robert Bess', 'rbess@dayonesolutions', 'dayonesolutions'] },
  { company: 'TXRE Properties', contact: 'Justin Smith', searchTerms: ['TXRE Properties', 'jsmith@txreproperties', 'txreproperties'] },
  { company: 'Nectus', contact: 'Dmitry Zaitsev', searchTerms: ['Nectus', 'Dmitry Zaitsev', 'dzaitsev@nectus'] },
  { company: 'AppNerve', contact: 'Kalyan A', searchTerms: ['AppNerve', 'Kalyan', 'kalyan@appnerve'] },
  { company: 'Krixi', contact: 'Sandeep Agate', searchTerms: ['Krixi', 'Sandeep Agate', 'sandeep.agate@krixi'] },
  { company: 'OnScript', contact: 'Jeff', searchTerms: ['OnScript', 'onscript.ai'] },
  { company: 'Graphy', contact: 'Vanshika', searchTerms: ['Graphy', 'Vanshika'] },
  { company: 'CourtScribes', contact: 'David Blaze', searchTerms: ['CourtScribes', 'David Blaze', 'courtscribes'] },
  { company: 'SpeedMS', contact: 'Garrett Kranz', searchTerms: ['SpeedMS', 'Garrett Kranz', 'speedms'] },
  { company: 'SecuPi', contact: 'Mosh Leder', searchTerms: ['SecuPi', 'Mosh Leder', 'secupi'] },
  { company: 'Digs', contact: 'Stephen', searchTerms: ['Digs', 'digs.co'] },
  { company: 'LinkAmerica', contact: 'Quincy', searchTerms: ['LinkAmerica', 'Quincy', 'linkamerica'] },
  { company: 'CrustData', contact: 'Aryaman', searchTerms: ['CrustData', 'Aryaman', 'crustdata'] },
  { company: 'Profit.co', contact: 'Suresh', searchTerms: ['Profit.co', 'Suresh', 'profit.co'] },
  { company: 'Soffront', contact: 'Manu Das', searchTerms: ['Soffront', 'Manu Das', 'soffront'] },
  { company: 'Byld Commerce', contact: 'Spencer', searchTerms: ['Byld Commerce', 'Spencer', 'byld'] },
  { company: 'EZO', contact: 'Matthew Fike', searchTerms: ['EZO', 'Matthew Fike', 'ezo.io'] },
  { company: 'AlignOps', contact: 'Wes Archibald', searchTerms: ['AlignOps', 'Wes Archibald', 'alignops'] },
  { company: 'UltraHaus', contact: 'Marco Bombardi', searchTerms: ['UltraHaus', 'Marco Bombardi', 'ultrahaus'] },
  { company: 'A&B Talent', contact: 'Westley Slater', searchTerms: ['A&B Talent', 'Westley Slater', 'abtalent'] },
  { company: 'BVM', contact: 'Kevin Orton', searchTerms: ['BVM', 'Kevin Orton'] },
  { company: 'Ed Funding', contact: 'Dennis Stewart', searchTerms: ['Ed Funding', 'Dennis Stewart', 'edfunding'] },
  { company: 'Verusen', contact: 'Tucker', searchTerms: ['Verusen', 'Tucker'] },
  { company: 'Industrial IA', contact: 'Doug Vail', searchTerms: ['Industrial IA', 'Doug Vail', 'industrialia'] },
  { company: 'Phala Network', contact: 'Jayson', searchTerms: ['Phala Network', 'Jayson', 'phala'] },
  { company: 'LegalSoft', contact: 'Haylie', searchTerms: ['LegalSoft', 'Haylie', 'legalsoft'] },
  { company: 'Hepner Consulting', contact: 'Nate', searchTerms: ['Hepner Consulting', 'Nate Hepner', 'hepner'] },
  { company: 'Blackstone', contact: 'Selena', searchTerms: ['Blackstone', 'Selena'] },
  { company: 'OTG Consulting', contact: 'Paul Petro', searchTerms: ['OTG Consulting', 'Paul Petro', 'otgconsulting'] },
];

// Pricing keywords to look for
const PERFORMANCE_KEYWORDS = ['pay per meeting', 'per meeting', 'cost per meeting', 'per qualified meeting', 
  'performance-based', 'performance based', 'setup fee', 'setup cost', 'one-time setup', 'onboarding fee',
  'variable', 'pay per lead', 'per lead', 'results-based', 'no retainer', '$200', '$250', '$300', '$350',
  '$1,500', '$2,000', '$2,500', '$3,000', 'per demo', 'per appointment'];

const ENTERPRISE_KEYWORDS = ['$7,500', '$7500', '7.5k', '$10,000', '$10000', '10k/month', '$12,500', '$12500',
  '$15,000', '$15000', '15k/month', 'monthly retainer', 'flat monthly', 'quarterly', '90 days', 'three month',
  '3 month', 'minimum commitment', 'enterprise', 'annual', '12 months', 'dedicated', 'full-service'];

async function searchMessages(query, maxResults = 30) {
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
    return null;
  }
}

function getHeader(msg, name) {
  const header = msg.payload.headers.find(h => h.name.toLowerCase() === name.toLowerCase());
  return header ? header.value : '';
}

function getBody(msg) {
  let body = '';
  
  function extractText(part) {
    if (part.body && part.body.data) {
      body += Buffer.from(part.body.data, 'base64').toString('utf-8') + ' ';
    }
    if (part.parts) {
      part.parts.forEach(extractText);
    }
  }
  
  extractText(msg.payload);
  return body.toLowerCase();
}

function findPricingKeywords(text) {
  const found = { performance: [], enterprise: [] };
  const textLower = text.toLowerCase();
  
  for (const kw of PERFORMANCE_KEYWORDS) {
    if (textLower.includes(kw.toLowerCase())) {
      found.performance.push(kw);
    }
  }
  
  for (const kw of ENTERPRISE_KEYWORDS) {
    if (textLower.includes(kw.toLowerCase())) {
      found.enterprise.push(kw);
    }
  }
  
  return found;
}

async function scanDeal(deal) {
  // Build search query
  const query = `(${deal.searchTerms.map(t => `"${t}"`).join(' OR ')}) newer_than:60d`;
  
  const messages = await searchMessages(query, 30);
  
  const result = {
    company: deal.company,
    contact: deal.contact,
    emails: [],
    performanceKeywords: new Set(),
    enterpriseKeywords: new Set(),
    pricingDiscussed: false,
    pricingType: null,
    relevantSnippets: []
  };
  
  for (const m of messages.slice(0, 20)) {
    const msg = await getMessage(m.id);
    if (!msg) continue;
    
    const from = getHeader(msg, 'From');
    const subject = getHeader(msg, 'Subject');
    const body = getBody(msg);
    const snippet = msg.snippet || '';
    
    // Search in subject, body, and snippet
    const combinedText = `${subject} ${body} ${snippet}`;
    const keywords = findPricingKeywords(combinedText);
    
    if (keywords.performance.length > 0 || keywords.enterprise.length > 0) {
      result.pricingDiscussed = true;
      keywords.performance.forEach(k => result.performanceKeywords.add(k));
      keywords.enterprise.forEach(k => result.enterpriseKeywords.add(k));
      
      // Extract relevant context
      result.relevantSnippets.push({
        subject,
        snippet: snippet.substring(0, 200),
        performanceTerms: keywords.performance,
        enterpriseTerms: keywords.enterprise
      });
    }
    
    result.emails.push({
      from,
      subject,
      hasPerformance: keywords.performance.length > 0,
      hasEnterprise: keywords.enterprise.length > 0
    });
  }
  
  // Determine pricing type
  result.performanceKeywords = [...result.performanceKeywords];
  result.enterpriseKeywords = [...result.enterpriseKeywords];
  
  if (result.performanceKeywords.length > result.enterpriseKeywords.length) {
    result.pricingType = 'PERFORMANCE';
  } else if (result.enterpriseKeywords.length > result.performanceKeywords.length) {
    result.pricingType = 'ENTERPRISE';
  } else if (result.pricingDiscussed) {
    result.pricingType = 'MIXED/UNCLEAR';
  }
  
  return result;
}

async function main() {
  console.log('Scanning all deals for pricing discussions...\n');
  
  const results = [];
  const enterprise = [];
  const performance = [];
  const unknown = [];
  
  for (let i = 0; i < DEALS.length; i++) {
    const deal = DEALS[i];
    process.stdout.write(`[${i+1}/${DEALS.length}] ${deal.company}... `);
    
    const result = await scanDeal(deal);
    results.push(result);
    
    if (result.pricingType === 'ENTERPRISE') {
      enterprise.push(result);
      console.log('ENTERPRISE');
    } else if (result.pricingType === 'PERFORMANCE') {
      performance.push(result);
      console.log('PERFORMANCE');
    } else if (result.pricingType === 'MIXED/UNCLEAR') {
      unknown.push(result);
      console.log('MIXED');
    } else {
      unknown.push(result);
      console.log('NO PRICING FOUND');
    }
    
    // Rate limit
    await new Promise(r => setTimeout(r, 300));
  }
  
  // Output results
  console.log('\n\n========================================');
  console.log('ENTERPRISE DEALS (Monthly Retainer $7.5k-$15k/mo)');
  console.log('========================================\n');
  
  for (const r of enterprise) {
    console.log(`• ${r.company} - ${r.contact}`);
    console.log(`  Keywords: ${r.enterpriseKeywords.join(', ')}`);
    if (r.relevantSnippets.length > 0) {
      console.log(`  Context: ${r.relevantSnippets[0].snippet}`);
    }
    console.log('');
  }
  
  console.log('\n========================================');
  console.log('PERFORMANCE DEALS (Pay per meeting/Setup + variable)');
  console.log('========================================\n');
  
  for (const r of performance) {
    console.log(`• ${r.company} - ${r.contact}`);
    console.log(`  Keywords: ${r.performanceKeywords.join(', ')}`);
    if (r.relevantSnippets.length > 0) {
      console.log(`  Context: ${r.relevantSnippets[0].snippet}`);
    }
    console.log('');
  }
  
  console.log('\n========================================');
  console.log('UNKNOWN/NO PRICING DISCUSSION FOUND');
  console.log('========================================\n');
  
  for (const r of unknown) {
    console.log(`• ${r.company} - ${r.contact} (${r.emails.length} emails scanned)`);
  }
  
  // JSON output
  console.log('\n\n=== JSON OUTPUT ===');
  console.log(JSON.stringify({ enterprise, performance, unknown }, null, 2));
}

main().catch(console.error);
