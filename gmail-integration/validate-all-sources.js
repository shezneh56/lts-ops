#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';

// Parse DD/M/YYYY or DD/MM/YYYY
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

function getWeekRange() {
  // Last week: 1/19/2026 - 1/25/2026
  const end = new Date('2026-01-25T23:59:59');
  const start = new Date('2026-01-19T00:00:00');
  
  return { start, end };
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
        name: cleaned[0],
        callTime: cleaned[1] || '',
        showed: cleaned[2] || '',
        closed: cleaned[3] || '',
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
  const { start, end } = getWeekRange();
  
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
        startTime: event.start_time,
        status: event.status,
        isPast: new Date(event.start_time) < new Date()
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return detailed;
}

async function run() {
  console.log('🔍 CROSS-SOURCE VALIDATION\n');
  console.log('='.repeat(60));
  
  const { start, end } = getWeekRange();
  console.log(`\n📅 Week Range: ${start.toLocaleDateString()} - ${end.toLocaleDateString()}\n`);
  
  // Source 1: Call Tracker
  console.log('📊 SOURCE 1: Call Tracker (Google Sheet)');
  const tracker = await fetchCallTracker();
  const trackerWeek = tracker.filter(lead => {
    if (!lead.callTime) return false;
    try {
      const callDate = parseDate(lead.callTime);
      return callDate >= start && callDate <= end;
    } catch {
      return false;
    }
  });
  
  const trackerShowed = trackerWeek.filter(l => 
    l.showed && l.showed.toLowerCase().includes('yes')
  ).length;
  
  console.log(`  • Booked: ${trackerWeek.length}`);
  console.log(`  • Showed: ${trackerShowed}`);
  console.log(`  • Show Rate: ${Math.round((trackerShowed/trackerWeek.length)*100)}%\n`);
  
  // Source 2: Calendly
  console.log('📅 SOURCE 2: Calendly API');
  const calendly = await fetchCalendlyEvents();
  const calendlyPast = calendly.filter(e => e.isPast);
  const calendlyActive = calendlyPast.filter(e => e.status === 'active');
  
  console.log(`  • Booked: ${calendly.length}`);
  console.log(`  • Past (due): ${calendlyPast.length}`);
  console.log(`  • Active (showed): ${calendlyActive.length}`);
  console.log(`  • Canceled: ${calendly.filter(e => e.status === 'canceled').length}`);
  console.log(`  • Show Rate: ${Math.round((calendlyActive.length/calendlyPast.length)*100)}%\n`);
  
  // Source 3: Fathom (placeholder until we fix API)
  console.log('🎥 SOURCE 3: Fathom');
  console.log(`  • Status: ⏳ API endpoint needs fixing\n`);
  
  console.log('='.repeat(60));
  console.log('\n🎯 COMPARISON:\n');
  
  console.log(`Call Tracker: ${trackerWeek.length} booked, ${trackerShowed} showed (${Math.round((trackerShowed/trackerWeek.length)*100)}%)`);
  console.log(`Calendly:     ${calendly.length} booked, ${calendlyActive.length} showed (${Math.round((calendlyActive.length/calendlyPast.length)*100)}%)`);
  
  const diff = Math.abs(trackerWeek.length - calendly.length);
  if (diff === 0) {
    console.log('\n✅ Perfect match on booking count!');
  } else {
    console.log(`\n⚠️  Discrepancy: ${diff} calls difference`);
  }
  
  const showDiff = Math.abs(trackerShowed - calendlyActive.length);
  if (showDiff === 0) {
    console.log('✅ Perfect match on show count!');
  } else {
    console.log(`⚠️  Discrepancy: ${showDiff} shows difference`);
  }
  
  console.log('\n' + '='.repeat(60) + '\n');
}

run().catch(console.error);
