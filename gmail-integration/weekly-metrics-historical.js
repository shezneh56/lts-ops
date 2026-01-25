#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();
const { getMeetings } = require('./fathom-api.js');

const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';

function getWeekBounds(weeksAgo = 0) {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  
  const thisMonday = new Date(now);
  thisMonday.setDate(now.getDate() + diffToMonday);
  thisMonday.setHours(0, 0, 0, 0);
  
  const monday = new Date(thisMonday);
  monday.setDate(thisMonday.getDate() - (weeksAgo * 7));
  
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);
  
  return { monday, sunday };
}

async function getCurrentUser() {
  const response = await axios.get(`${CALENDLY_API}/users/me`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` }
  });
  return response.data.resource;
}

async function getWeeklyBookings(weeksAgo = 0) {
  const user = await getCurrentUser();
  const { monday, sunday } = getWeekBounds(weeksAgo);
  
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
    const isDiscoveryCall = event.name.toLowerCase().includes('discovery') || 
                           event.name.toLowerCase().includes('leads that show');
    const isClientCall = event.name.toLowerCase().includes('client call');
    
    if (!isDiscoveryCall || isClientCall) {
      continue;
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
        status: event.status
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return { bookings, weekStart: monday, weekEnd: sunday };
}

function isSalesCall(title) {
  const lower = title.toLowerCase();
  if (lower.includes('client call')) return false;
  return lower.includes('discovery call') || lower.includes('leads that show - discovery');
}

async function getWeeklySalesCalls(weeksAgo = 0) {
  const { monday, sunday } = getWeekBounds(weeksAgo);
  const salesCalls = [];
  
  let cursor = null;
  let hasMore = true;
  
  while (hasMore) {
    const data = await getMeetings(100, cursor);
    
    for (const meeting of data.items) {
      const recordingTime = new Date(meeting.recording_start_time);
      
      if (recordingTime >= monday && recordingTime <= sunday) {
        if (isSalesCall(meeting.title)) {
          const name = meeting.title.split(':')[0].trim();
          salesCalls.push({
            name,
            title: meeting.title,
            recordingTime: meeting.recording_start_time
          });
        }
      } else if (recordingTime < monday) {
        hasMore = false;
        break;
      }
    }
    
    if (data.next_cursor && hasMore) {
      cursor = data.next_cursor;
    } else {
      hasMore = false;
    }
  }
  
  return salesCalls;
}

async function run() {
  const weeksAgo = parseInt(process.argv[2]) || 1; // Default to last week
  
  console.log(`\n📊 Calculating metrics for ${weeksAgo} week(s) ago...\n`);
  
  const { bookings, weekStart, weekEnd } = await getWeeklyBookings(weeksAgo);
  const fathomCalls = await getWeeklySalesCalls(weeksAgo);
  
  const now = new Date();
  const pastCalls = bookings.filter(b => new Date(b.startTime) < now);
  const showRate = pastCalls.length > 0 ? Math.round((fathomCalls.length / pastCalls.length) * 100) : 0;
  
  console.log(`📅 Week: ${weekStart.toLocaleDateString()} - ${weekEnd.toLocaleDateString()}\n`);
  console.log(`📞 Calls Booked: ${bookings.length}`);
  console.log(`✅ Calls Showed: ${fathomCalls.length}/${pastCalls.length}`);
  console.log(`📈 Show Rate: ${showRate}%\n`);
  
  if (fathomCalls.length > 0) {
    console.log('Who showed up:\n');
    fathomCalls.forEach(call => {
      console.log(`  • ${call.name}`);
    });
  }
  
  return {
    week: `${weekStart.toLocaleDateString()} - ${weekEnd.toLocaleDateString()}`,
    booked: bookings.length,
    showed: fathomCalls.length,
    due: pastCalls.length,
    showRate,
    names: fathomCalls.map(c => c.name)
  };
}

run().catch(console.error);
