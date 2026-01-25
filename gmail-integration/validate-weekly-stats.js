#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;

async function fetchCallTracker() {
  const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv`;
  const response = await axios.get(csvUrl);
  return parseCSV(response.data);
}

function parseCSV(csv) {
  const lines = csv.split('\n');
  const leads = [];
  
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue;
    
    // Handle quoted CSV fields
    const values = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || [];
    const cleaned = values.map(v => v.replace(/^"|"$/g, '').trim());
    
    if (cleaned[0]) {
      leads.push({
        name: cleaned[0],
        callTime: cleaned[1] || '',
        showed: cleaned[2] || '',
        closed: cleaned[3] || '',
        notes: cleaned[4] || '',
        actions: cleaned[5] || '',
        source: cleaned[6] || '',
        followUp: cleaned[7] || '',
      });
    }
  }
  
  return leads;
}

function parseDate(dateStr) {
  // Handle DD/MM/YYYY format (British)
  const parts = dateStr.trim().split('/');
  if (parts.length === 3) {
    const day = parseInt(parts[0]);
    const month = parseInt(parts[1]) - 1; // JS months are 0-indexed
    const year = parseInt(parts[2]);
    return new Date(year, month, day);
  }
  return new Date(dateStr);
}

function getLastWeekCalls(leads) {
  const now = new Date();
  const oneWeekAgo = new Date(now);
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
  
  return leads.filter(lead => {
    if (!lead.callTime) return false;
    
    try {
      const callDate = parseDate(lead.callTime);
      return callDate >= oneWeekAgo && callDate <= now;
    } catch {
      return false;
    }
  });
}

async function run() {
  console.log('📊 Validating Last Week Stats\n');
  console.log('=' .repeat(50));
  
  const allLeads = await fetchCallTracker();
  console.log(`\n✅ Total calls in tracker: ${allLeads.length}`);
  
  const lastWeek = getLastWeekCalls(allLeads);
  console.log(`\n📅 Last 7 days: ${lastWeek.length} calls booked`);
  
  const showed = lastWeek.filter(l => 
    l.showed && l.showed.toLowerCase().includes('yes')
  ).length;
  
  const noShow = lastWeek.filter(l => 
    l.showed && l.showed.toLowerCase().includes('no')
  ).length;
  
  const pending = lastWeek.filter(l => 
    !l.showed || l.showed.trim() === ''
  ).length;
  
  const closed = lastWeek.filter(l =>
    l.closed && l.closed.toLowerCase().includes('yes')
  ).length;
  
  const showRate = lastWeek.length > 0 
    ? Math.round((showed / lastWeek.length) * 100) 
    : 0;
  
  console.log('\n' + '='.repeat(50));
  console.log('\n📈 LAST WEEK BREAKDOWN:');
  console.log('  • Booked: ' + lastWeek.length);
  console.log('  • Showed: ' + showed);
  console.log('  • No-show: ' + noShow);
  console.log('  • Pending: ' + pending);
  console.log('  • Closed: ' + closed);
  console.log('\n  📊 Show Rate: ' + showRate + '%');
  
  console.log('\n' + '='.repeat(50));
  console.log('\n🎯 VALIDATION CHECK:');
  console.log('  Expected: ~27 booked, ~19 showed (70%)');
  console.log('  Actual: ' + lastWeek.length + ' booked, ' + showed + ' showed (' + showRate + '%)');
  
  if (lastWeek.length >= 25 && lastWeek.length <= 29) {
    console.log('  ✅ Booking volume matches!');
  } else {
    console.log('  ⚠️  Booking volume different than expected');
  }
  
  if (showRate >= 65 && showRate <= 75) {
    console.log('  ✅ Show rate in expected range!');
  } else {
    console.log('  ⚠️  Show rate different than expected');
  }
  
  console.log('\n' + '='.repeat(50) + '\n');
}

run().catch(console.error);
