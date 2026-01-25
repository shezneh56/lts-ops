#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
require('dotenv').config();
const { getWeeklySalesCalls } = require('./fathom-api.js');

const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';
const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '526d65d994ef4d78ce05616264fdd7c68dbb0b818c3f7269';

async function getCurrentUser() {
  const response = await axios.get(`${CALENDLY_API}/users/me`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` }
  });
  return response.data.resource;
}

async function getWeeklyBookings() {
  const user = await getCurrentUser();
  
  // Get this week's date range (Monday to Sunday)
  const now = new Date();
  const dayOfWeek = now.getDay();
  const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Sunday = 0
  
  const monday = new Date(now);
  monday.setDate(now.getDate() + diffToMonday);
  monday.setHours(0, 0, 0, 0);
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);
  
  console.log(`Week: ${monday.toLocaleDateString()} - ${sunday.toLocaleDateString()}`);
  
  const response = await axios.get(`${CALENDLY_API}/scheduled_events`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` },
    params: {
      user: user.uri,
      count: 100,
      min_start_time: monday.toISOString(),
      max_start_time: sunday.toISOString()
    }
  });
  
  const events = response.data.collection;
  const bookings = [];
  
  for (const event of events) {
    // Only count sales calls (Discovery Calls), not client/team calls
    const isDiscoveryCall = event.name.toLowerCase().includes('discovery') || 
                           event.name.toLowerCase().includes('leads that show');
    const isClientCall = event.name.toLowerCase().includes('client call');
    
    if (!isDiscoveryCall || isClientCall) {
      continue; // Skip non-sales calls
    }
    
    try {
      const inviteesResponse = await axios.get(
        `${CALENDLY_API}/scheduled_events/${event.uri.split('/').pop()}/invitees`,
        { headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` } }
      );
      
      const invitee = inviteesResponse.data.collection[0];
      
      bookings.push({
        name: invitee.name,
        email: invitee.email,
        startTime: event.start_time,
        status: event.status, // active, canceled
        eventType: event.name
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return { bookings, weekStart: monday, weekEnd: sunday };
}

async function fetchCallTracker() {
  const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv`;
  const response = await axios.get(csvUrl);
  return parseCSV(response.data);
}

function parseCSV(csv) {
  const lines = csv.split('\n');
  const leads = [];
  
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',');
    if (values[0]) {
      leads.push({
        name: values[0],
        callTime: values[1],
        showed: values[2],
        closed: values[3],
        notes: values[4]
      });
    }
  }
  
  return leads;
}

function getWeekBounds() {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  
  const monday = new Date(now);
  monday.setDate(now.getDate() + diffToMonday);
  monday.setHours(0, 0, 0, 0);
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);
  
  return { monday, sunday };
}

function isThisWeek(dateStr) {
  const { monday, sunday } = getWeekBounds();
  
  // Parse DD/MM/YYYY format
  const parts = dateStr.split('/');
  if (parts.length !== 3) return false;
  
  const callDate = new Date(parts[2], parts[1] - 1, parts[0]);
  
  return callDate >= monday && callDate <= sunday;
}

async function calculateMetrics() {
  console.log('\n📊 Calculating weekly metrics...\n');
  
  const { bookings, weekStart, weekEnd } = await getWeeklyBookings();
  const tracker = await fetchCallTracker();
  
  // Calls booked this week (from Calendly)
  const callsBooked = bookings.length;
  
  // Calls that should have happened (past start time)
  const now = new Date();
  const pastCalls = bookings.filter(b => new Date(b.startTime) < now);
  
  // Get who actually showed up from Fathom
  console.log('📹 Fetching Fathom recordings...\n');
  const fathomCalls = await getWeeklySalesCalls();
  const showedCount = fathomCalls.length;
  
  // Calculate show rate
  const showRate = pastCalls.length > 0 
    ? Math.round((showedCount / pastCalls.length) * 100) 
    : 0;
  
  // Count closes from tracker this week
  const closes = tracker.filter(t => 
    isThisWeek(t.callTime) && 
    (t.closed === 'Yes' || t.closed === 'Closed')
  );
  
  return {
    week: `${weekStart.toLocaleDateString()} - ${weekEnd.toLocaleDateString()}`,
    callsBooked,
    callsDue: pastCalls.length,
    callsShowed: showedCount,
    callsNoShow: pastCalls.length - showedCount,
    showRate,
    closes: closes.length,
    details: {
      showed: fathomCalls.map(c => c.name),
      closedDeals: closes.map(c => c.name)
    }
  };
}

async function sendWeeklySummary(metrics) {
  const message = 
    `📊 *WEEKLY SALES METRICS*\n\n` +
    `📅 Week: ${metrics.week}\n\n` +
    `📞 *Calls Booked:* ${metrics.callsBooked}\n` +
    `✅ *Calls Showed:* ${metrics.callsShowed}/${metrics.callsDue}\n` +
    `📈 *Show Rate:* ${metrics.showRate}%\n` +
    `🎯 *Target:* 30 calls/week (${metrics.callsBooked >= 30 ? '✅' : '❌'})\n\n` +
    `💰 *Closed This Week:* ${metrics.closes}\n\n` +
    (metrics.showRate < 70 ? `⚠️ Show rate below 70% - consider follow-up cadence improvements\n\n` : '') +
    (metrics.callsBooked < 30 ? `⚠️ Below weekly target - need ${30 - metrics.callsBooked} more bookings\n\n` : '') +
    `Keep crushing it! 💪`;
  
  try {
    await axios.post(
      `${GATEWAY_URL}/rpc`,
      {
        tool: 'message',
        params: {
          action: 'send',
          channel: 'whatsapp',
          target: '+447716953711',
          message: message
        }
      },
      {
        headers: {
          'Authorization': `Bearer ${GATEWAY_TOKEN}`,
          'Content-Type': 'application/json'
        }
      }
    );
    console.log('✅ Weekly summary sent via WhatsApp');
  } catch (err) {
    console.error('WhatsApp error:', err.message);
  }
}

async function run() {
  const metrics = await calculateMetrics();
  
  console.log('\n📊 Weekly Metrics:\n');
  console.log(`Week: ${metrics.week}`);
  console.log(`Calls Booked: ${metrics.callsBooked}`);
  console.log(`Calls Due: ${metrics.callsDue}`);
  console.log(`Showed Up: ${metrics.callsShowed}`);
  console.log(`No Shows: ${metrics.callsNoShow}`);
  console.log(`Show Rate: ${metrics.showRate}%`);
  console.log(`Closes: ${metrics.closes}`);
  console.log('');
  
  // Save metrics
  await fs.writeFile(
    '/root/clawd/weekly-metrics.json',
    JSON.stringify(metrics, null, 2)
  );
  console.log('✅ Saved to /root/clawd/weekly-metrics.json\n');
  
  // Send summary
  await sendWeeklySummary(metrics);
}

run().catch(console.error);
