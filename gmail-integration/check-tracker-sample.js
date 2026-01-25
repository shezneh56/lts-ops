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
    
    const values = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g) || [];
    const cleaned = values.map(v => v.replace(/^"|"$/g, '').trim());
    
    if (cleaned[0]) {
      leads.push({
        name: cleaned[0],
        callTime: cleaned[1] || '',
        showed: cleaned[2] || '',
        closed: cleaned[3] || '',
        notes: cleaned[4] || '',
      });
    }
  }
  
  return leads;
}

async function run() {
  const leads = await fetchCallTracker();
  
  console.log('📋 Sample of recent entries:\n');
  console.log('Total entries:', leads.length);
  console.log('\nLast 10 entries:');
  console.log('='.repeat(80));
  
  const recent = leads.slice(-10);
  recent.forEach((lead, i) => {
    console.log(`\n${i + 1}. ${lead.name}`);
    console.log(`   Call Time: "${lead.callTime}"`);
    console.log(`   Showed: "${lead.showed}"`);
    console.log(`   Closed: "${lead.closed}"`);
  });
}

run().catch(console.error);
