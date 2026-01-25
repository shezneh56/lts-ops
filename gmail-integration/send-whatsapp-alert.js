#!/usr/bin/env node

const { execSync } = require('child_process');
const axios = require('axios');
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;
const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '526d65d994ef4d78ce05616264fdd7c68dbb0b818c3f7269';

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

function analyzeLeads(leads) {
  const urgent = [];
  const hot = [];
  const needsPostCall = [];
  const followUpsDue = [];
  
  leads.forEach(lead => {
    if (lead.notes && lead.notes.toLowerCase().includes('havent followed up')) {
      urgent.push({
        name: lead.name,
        reason: 'Agreement sent - NO FOLLOW-UP'
      });
    }
    
    if (lead.actions && lead.actions.trim() && !lead.actions.toLowerCase().includes('closed')) {
      needsPostCall.push({
        name: lead.name,
        action: lead.actions
      });
    }
    
    if (lead.closed && (lead.closed === 'HOT' || lead.closed === 'HOT HOT' || lead.closed.includes('HOT'))) {
      hot.push({
        name: lead.name,
        status: lead.closed,
        notes: lead.notes || '',
        followUp: lead.followUp || ''
      });
    }
    
    if (lead.followUp && lead.followUp.includes('Jan') && lead.followUp.includes('20')) {
      followUpsDue.push({
        name: lead.name,
        followUpDate: lead.followUp,
        notes: lead.notes || ''
      });
    }
  });
  
  return { urgent, hot, needsPostCall, followUpsDue };
}

function formatAlert(analysis) {
  let message = '🌅 *Good morning Liam!*\n\n';
  
  if (analysis.urgent.length > 0) {
    message += '🚨 *URGENT - ACTION REQUIRED:*\n';
    analysis.urgent.forEach(item => {
      message += `• *${item.name}* - ${item.reason}\n`;
    });
    message += '\n';
  }
  
  if (analysis.followUpsDue.length > 0) {
    message += `📅 *FOLLOW-UPS DUE SOON (${analysis.followUpsDue.length}):*\n`;
    analysis.followUpsDue.slice(0, 6).forEach(item => {
      message += `• *${item.name}*`;
      if (item.notes) message += ` - ${item.notes}`;
      message += '\n';
    });
    if (analysis.followUpsDue.length > 6) {
      message += `   ...and ${analysis.followUpsDue.length - 6} more\n`;
    }
    message += '\n';
  }
  
  if (analysis.needsPostCall.length > 0) {
    message += `📧 *POST-CALL ACTIONS (${analysis.needsPostCall.length}):*\n`;
    analysis.needsPostCall.slice(0, 5).forEach(item => {
      message += `• *${item.name}* - ${item.action}\n`;
    });
    if (analysis.needsPostCall.length > 5) {
      message += `   ...and ${analysis.needsPostCall.length - 5} more\n`;
    }
    message += '\n';
  }
  
  if (analysis.hot.length > 0) {
    message += `🔥 *HOT LEADS:* ${analysis.hot.length} total\n`;
    message += 'Top 5:\n';
    analysis.hot.slice(0, 5).forEach(item => {
      message += `• *${item.name}*`;
      if (item.notes) message += ` - ${item.notes}`;
      message += '\n';
    });
    message += '\n';
  }
  
  if (analysis.urgent.length === 0 && analysis.followUpsDue.length === 0 && 
      analysis.needsPostCall.length === 0 && analysis.hot.length === 0) {
    message += '✅ *All clear!* No urgent actions today.\n\n';
  }
  
  message += '💪 *Get after it!*';
  
  return message;
}

async function sendWhatsApp(message) {
  try {
    const response = await axios.post(
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
    
    console.log('✅ Alert sent via WhatsApp');
    return response.data;
  } catch (err) {
    console.error('❌ Error sending WhatsApp:', err.message);
    throw err;
  }
}

async function run() {
  console.log('📊 Fetching call tracker...');
  const leads = await fetchCallTracker();
  console.log(`✅ Found ${leads.length} leads`);
  
  console.log('🔍 Analyzing...');
  const analysis = analyzeLeads(leads);
  
  const alert = formatAlert(analysis);
  console.log('\n' + alert + '\n');
  
  console.log('📱 Sending WhatsApp alert...');
  await sendWhatsApp(alert);
}

run().catch(console.error);
