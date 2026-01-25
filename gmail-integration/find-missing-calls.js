#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';

function parseDate(dateStr) {
  const parts = dateStr.split('/');
  if (parts.length === 3) {
    const day = parseInt(parts[0]);
    const month = parseInt(parts[1]) - 1;
    const year = parseInt(parts[2]);
    return new Date(year, month, day);
  }
  return new Date(dateStr);
}

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
        name: cleaned[0].toLowerCase(),
        callTime: cleaned[1] || '',
      });
    }
  }
  
  return leads;
}

async function fetchCalendlyEvents() {
  const userResponse = await axios.get(`${CALENDLY_API}/users/me`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` }
  });
  
  const user = userResponse.data.resource;
  const start = new Date('2026-01-19T00:00:00');
  const end = new Date('2026-01-25T23:59:59');
  
  const eventsResponse = await axios.get(`${CALENDLY_API}/scheduled_events`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` },
    params: {
      user: user.uri,
      count: 100,
      min_start_time: start.toISOString(),
      max_start_time: end.toISOString()
    }
  });
  
  const events = eventsResponse.data.collection;
  const detailed = [];
  
  for (const event of events) {
    try {
      const inviteesResponse = await axios.get(
        `${CALENDLY_API}/scheduled_events/${event.uri.split('/').pop()}/invitees`,
        { headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` } }
      );
      
      const invitee = inviteesResponse.data.collection[0];
      
      detailed.push({
        name: invitee.name,
        email: invitee.email,
        startTime: new Date(event.start_time),
        status: event.status
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return detailed;
}

function fuzzyMatch(name1, name2) {
  const n1 = name1.toLowerCase().replace(/[^a-z]/g, '');
  const n2 = name2.toLowerCase().replace(/[^a-z]/g, '');
  
  return n1.includes(n2) || n2.includes(n1) || 
         n1.split(' ').some(part => n2.includes(part)) ||
         n2.split(' ').some(part => n1.includes(part));
}

async function run() {
  console.log('🔍 Finding Missing Calls\n');
  console.log('='.repeat(60) + '\n');
  
  const tracker = await fetchCallTracker();
  const calendly = await fetchCalendlyEvents();
  
  console.log(`📊 Call Tracker: ${tracker.length} entries`);
  console.log(`📅 Calendly: ${calendly.length} bookings\n`);
  console.log('='.repeat(60) + '\n');
  
  const missing = [];
  
  for (const cal of calendly) {
    const inTracker = tracker.some(t => fuzzyMatch(t.name, cal.name));
    
    if (!inTracker) {
      missing.push(cal);
    }
  }
  
  if (missing.length > 0) {
    console.log(`❌ ${missing.length} calls in Calendly but NOT in tracker:\n`);
    missing.forEach((call, i) => {
      console.log(`${i+1}. ${call.name}`);
      console.log(`   Email: ${call.email}`);
      console.log(`   Time: ${call.startTime.toLocaleString()}`);
      console.log(`   Status: ${call.status}\n`);
    });
  } else {
    console.log('✅ All Calendly calls are in the tracker!');
  }
  
  console.log('='.repeat(60));
}

run().catch(console.error);
