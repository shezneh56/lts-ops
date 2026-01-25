#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;

async function fetchCallTracker() {
  const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv`;
  const response = await axios.get(csvUrl);
  
  const lines = response.data.split('\n');
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
    const month = parseInt(parts[1]) - 1;
    const year = parseInt(parts[2]);
    return new Date(year, month, day);
  }
  return new Date(dateStr);
}

async function run() {
  const tracker = await fetchCallTracker();
  
  const start = new Date('2026-01-19T00:00:00');
  const end = new Date('2026-01-25T23:59:59');
  
  const inRange = tracker.filter(lead => {
    if (!lead.callTime) return false;
    try {
      const callDate = parseDate(lead.callTime);
      return callDate >= start && callDate <= end;
    } catch {
      return false;
    }
  });
  
  console.log(`📋 Calls in tracker for Jan 19-25, 2026:\n`);
  console.log('Total:', inRange.length);
  console.log('');
  
  inRange.forEach(lead => {
    console.log(`${lead.name} - ${lead.callTime}`);
  });
}

run().catch(console.error);
