#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
require('dotenv').config();

const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const FATHOM_API = 'https://api.fathom.video/v1';

async function listCalls(limit = 20) {
  const response = await axios.get(`${FATHOM_API}/calls`, {
    headers: {
      'Authorization': `Bearer ${FATHOM_API_KEY}`,
      'Content-Type': 'application/json'
    },
    params: {
      limit: limit
    }
  });
  
  return response.data.calls || response.data;
}

async function getCallDetails(callId) {
  const response = await axios.get(`${FATHOM_API}/calls/${callId}`, {
    headers: {
      'Authorization': `Bearer ${FATHOM_API_KEY}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.data;
}

async function getTranscript(callId) {
  try {
    const response = await axios.get(`${FATHOM_API}/calls/${callId}/transcript`, {
      headers: {
        'Authorization': `Bearer ${FATHOM_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    return response.data;
  } catch (err) {
    console.error(`Transcript not available for ${callId}:`, err.message);
    return null;
  }
}

async function getSummary(callId) {
  try {
    const response = await axios.get(`${FATHOM_API}/calls/${callId}/summary`, {
      headers: {
        'Authorization': `Bearer ${FATHOM_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    
    return response.data;
  } catch (err) {
    console.error(`Summary not available for ${callId}:`, err.message);
    return null;
  }
}

async function run() {
  console.log('🎥 Fetching Fathom calls...\n');
  
  const calls = await listCalls(10);
  console.log(`Found ${calls.length} recent calls\n`);
  
  for (const call of calls.slice(0, 5)) {
    console.log(`📞 ${call.title || 'Untitled Call'}`);
    console.log(`   ID: ${call.id}`);
    console.log(`   Date: ${new Date(call.start_time).toLocaleString()}`);
    console.log(`   Duration: ${Math.round(call.duration / 60)} min`);
    
    // Try to get transcript
    const transcript = await getTranscript(call.id);
    if (transcript) {
      console.log(`   ✅ Transcript available (${transcript.length} chars)`);
    }
    
    // Try to get summary
    const summary = await getSummary(call.id);
    if (summary) {
      console.log(`   ✅ Summary available`);
    }
    
    console.log('');
  }
  
  // Save first call details for reference
  if (calls.length > 0) {
    const firstCall = calls[0];
    const details = await getCallDetails(firstCall.id);
    const transcript = await getTranscript(firstCall.id);
    const summary = await getSummary(firstCall.id);
    
    await fs.writeFile(
      '/root/clawd/fathom-sample.json',
      JSON.stringify({ details, transcript, summary }, null, 2)
    );
    console.log('✅ Saved sample call to /root/clawd/fathom-sample.json');
  }
}

run().catch(console.error);
