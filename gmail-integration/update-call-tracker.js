#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '526d65d994ef4d78ce05616264fdd7c68dbb0b818c3f7269';

// Mock Fathom data for now - will replace with real API once endpoint is confirmed
async function getRecentRecordings() {
  // This will be replaced with real Fathom API calls
  // For now, return empty array
  return [];
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
        notes: values[4],
        actions: values[5],
        source: values[6],
        followUp: values[7],
      });
    }
  }
  
  return leads;
}

async function generateCallSummary(transcript) {
  // Use Claude to generate summary from transcript
  // For now, placeholder
  return {
    keyPoints: [],
    nextSteps: [],
    sentiment: 'positive',
    closeStatus: 'potential'
  };
}

async function updateFromCalendly() {
  // Check Calendly for calls that happened (past start time)
  // Update "Showed?" based on whether they happened
  const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
  const CALENDLY_API = 'https://api.calendly.com';
  
  try {
    const userResponse = await axios.get(`${CALENDLY_API}/users/me`, {
      headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` }
    });
    
    const user = userResponse.data.resource;
    
    // Get events from past 7 days
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    
    const eventsResponse = await axios.get(`${CALENDLY_API}/scheduled_events`, {
      headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` },
      params: {
        user: user.uri,
        count: 50,
        min_start_time: sevenDaysAgo.toISOString(),
        max_start_time: new Date().toISOString() // Past events only
      }
    });
    
    const pastEvents = eventsResponse.data.collection;
    const updates = [];
    
    for (const event of pastEvents) {
      try {
        const inviteesResponse = await axios.get(
          `${CALENDLY_API}/scheduled_events/${event.uri.split('/').pop()}/invitees`,
          { headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` } }
        );
        
        const invitee = inviteesResponse.data.collection[0];
        
        updates.push({
          name: invitee.name,
          email: invitee.email,
          callTime: event.start_time,
          status: event.status, // active, canceled
          showed: event.status === 'active' ? 'Yes' : 'No'
        });
      } catch (err) {
        console.error('Error fetching invitee:', err.message);
      }
    }
    
    return updates;
  } catch (err) {
    console.error('Calendly error:', err.message);
    return [];
  }
}

async function run() {
  console.log('📊 Fetching call tracker...\n');
  const tracker = await fetchCallTracker();
  console.log(`Found ${tracker.length} calls in tracker\n`);
  
  console.log('📅 Checking Calendly for past calls...\n');
  const calendlyUpdates = await updateFromCalendly();
  console.log(`Found ${calendlyUpdates.length} past calls from Calendly\n`);
  
  const needsUpdate = [];
  
  // Match Calendly data to tracker entries
  for (const update of calendlyUpdates) {
    const trackerEntry = tracker.find(t => 
      t.name.toLowerCase().includes(update.name.toLowerCase()) ||
      update.name.toLowerCase().includes(t.name.toLowerCase())
    );
    
    if (trackerEntry && !trackerEntry.showed) {
      console.log(`✅ Update found: ${update.name} - ${update.showed}`);
      needsUpdate.push({
        name: update.name,
        showed: update.showed,
        callTime: new Date(update.callTime).toLocaleDateString()
      });
    }
  }
  
  if (needsUpdate.length > 0) {
    console.log(`\n🚨 ${needsUpdate.length} calls need "Showed?" updated:\n`);
    needsUpdate.forEach(u => {
      console.log(`  • ${u.name} (${u.callTime}): Showed = ${u.showed}`);
    });
    
    // Save update recommendations
    await fs.writeFile(
      '/root/clawd/tracker-updates.json',
      JSON.stringify(needsUpdate, null, 2)
    );
    console.log('\n✅ Saved updates to /root/clawd/tracker-updates.json');
    console.log('\n💡 Manual action: Update the Google Sheet with these values');
  } else {
    console.log('\n✅ All recent calls already marked in tracker');
  }
}

run().catch(console.error);
