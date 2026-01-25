#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';

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
        startTime: new Date(event.start_time)
      });
    } catch (err) {}
  }
  
  return detailed;
}

function fuzzyMatch(name1, name2) {
  const n1 = name1.toLowerCase().replace(/[^a-z]/g, '');
  const n2 = name2.toLowerCase().replace(/[^a-z]/g, '');
  return n1.includes(n2) || n2.includes(n1);
}

async function run() {
  const tracker = await fetchCallTracker();
  const calendly = await fetchCalendlyEvents();
  
  console.log('🔍 Checking dates for Calendly calls in tracker\n');
  console.log('='.repeat(70) + '\n');
  
  for (const cal of calendly.slice(0, 10)) {
    const match = tracker.find(t => fuzzyMatch(t.name, cal.name));
    
    if (match) {
      console.log(`${cal.name}`);
      console.log(`  Calendly date: ${cal.startTime.toLocaleDateString()}`);
      console.log(`  Tracker date:  "${match.callTime}"`);
      console.log('');
    }
  }
}

run().catch(console.error);
