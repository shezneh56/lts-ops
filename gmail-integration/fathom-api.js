#!/usr/bin/env node

const axios = require('axios');
require('dotenv').config();

const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const FATHOM_API = 'https://api.fathom.ai/external/v1';

async function getMeetings(limit = 50, cursor = null) {
  const params = { limit };
  if (cursor) params.cursor = cursor;
  
  const response = await axios.get(`${FATHOM_API}/meetings`, {
    headers: { 'X-Api-Key': FATHOM_API_KEY },
    params
  });
  
  return response.data;
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

function isSalesCall(title) {
  const lower = title.toLowerCase();
  
  // Exclude client calls
  if (lower.includes('client call')) return false;
  
  // Include discovery calls
  return lower.includes('discovery call') || 
         lower.includes('leads that show - discovery');
}

async function getWeeklySalesCalls() {
  const { monday, sunday } = getWeekBounds();
  const salesCalls = [];
  
  let cursor = null;
  let hasMore = true;
  
  while (hasMore) {
    const data = await getMeetings(100, cursor);
    
    for (const meeting of data.items) {
      const recordingTime = new Date(meeting.recording_start_time);
      
      // Check if in this week
      if (recordingTime >= monday && recordingTime <= sunday) {
        // Check if it's a sales call
        if (isSalesCall(meeting.title)) {
          const name = meeting.title.split(':')[0].trim();
          
          salesCalls.push({
            name,
            title: meeting.title,
            recordingTime: meeting.recording_start_time,
            duration: Math.round((new Date(meeting.recording_end_time) - new Date(meeting.recording_start_time)) / 1000 / 60),
            url: meeting.url
          });
        }
      } else if (recordingTime < monday) {
        // Past the week, stop pagination
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
  console.log('🎥 Fetching Fathom sales calls this week...\n');
  
  const { monday, sunday } = getWeekBounds();
  console.log(`Week: ${monday.toLocaleDateString()} - ${sunday.toLocaleDateString()}\n`);
  
  const salesCalls = await getWeeklySalesCalls();
  
  console.log(`✅ Found ${salesCalls.length} sales calls that showed up:\n`);
  
  salesCalls.forEach(call => {
    console.log(`📞 ${call.name}`);
    console.log(`   ${new Date(call.recordingTime).toLocaleString()}`);
    console.log(`   Duration: ${call.duration} min`);
    console.log('');
  });
  
  return salesCalls;
}

if (require.main === module) {
  run().catch(console.error);
}

module.exports = { getMeetings, getWeeklySalesCalls, isSalesCall };
