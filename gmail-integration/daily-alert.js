#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
require('dotenv').config();

const SHEET_ID = process.env.CALL_TRACKER_SHEET_ID;

async function fetchCallTracker() {
  const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv`;
  const response = await axios.get(csvUrl);
  return parseCSV(response.data);
}

function parseCSV(csv) {
  const lines = csv.split('\n');
  const headers = lines[0].split(',');
  
  const leads = [];
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',');
    if (values[0]) { // Has a name
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
  const today = new Date();
  const urgent = [];
  const hot = [];
  const needsPostCall = [];
  const followUpsDue = [];
  
  leads.forEach(lead => {
    // Check for urgent actions in notes
    if (lead.notes && lead.notes.toLowerCase().includes('havent followed up')) {
      urgent.push({
        name: lead.name,
        reason: 'Agreement sent - NO FOLLOW-UP',
        priority: 'CRITICAL'
      });
    }
    
    // Check for action items
    if (lead.actions && lead.actions.trim()) {
      needsPostCall.push({
        name: lead.name,
        action: lead.actions,
        callDate: lead.callTime
      });
    }
    
    // Check for HOT leads
    if (lead.closed && (lead.closed === 'HOT' || lead.closed === 'HOT HOT' || lead.closed.includes('HOT'))) {
      hot.push({
        name: lead.name,
        status: lead.closed,
        notes: lead.notes || '',
        followUp: lead.followUp || ''
      });
    }
    
    // Check for follow-up dates
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
    message += '📅 *FOLLOW-UPS DUE SOON (by Jan 20):*\n';
    analysis.followUpsDue.forEach(item => {
      message += `• *${item.name}*`;
      if (item.notes) message += ` - ${item.notes}`;
      message += '\n';
    });
    message += '\n';
  }
  
  if (analysis.needsPostCall.length > 0) {
    message += '📧 *POST-CALL ACTIONS NEEDED:*\n';
    analysis.needsPostCall.forEach(item => {
      message += `• *${item.name}* - ${item.action}\n`;
    });
    message += '\n';
  }
  
  if (analysis.hot.length > 0) {
    message += `🔥 *HOT LEADS (${analysis.hot.length}):*\n`;
    analysis.hot.slice(0, 5).forEach(item => {
      message += `• *${item.name}*`;
      if (item.notes) message += ` - ${item.notes}`;
      if (item.followUp) message += ` (Follow up: ${item.followUp})`;
      message += '\n';
    });
    if (analysis.hot.length > 5) {
      message += `   ...and ${analysis.hot.length - 5} more\n`;
    }
    message += '\n';
  }
  
  if (analysis.urgent.length === 0 && analysis.followUpsDue.length === 0 && 
      analysis.needsPostCall.length === 0 && analysis.hot.length === 0) {
    message += '✅ *All clear!* No urgent actions today.\n\n';
  }
  
  message += '💪 *Get after it!*';
  
  return message;
}

async function sendAlert(message) {
  // For now, just print to console
  // Will integrate with WhatsApp once tested
  console.log(message);
  
  // Save to file for WhatsApp pickup
  await fs.writeFile('/root/clawd/daily-alert.txt', message);
  console.log('\n✅ Alert saved to /root/clawd/daily-alert.txt');
}

async function run() {
  console.log('📊 Fetching call tracker...');
  const leads = await fetchCallTracker();
  console.log(`✅ Found ${leads.length} leads`);
  
  console.log('🔍 Analyzing...');
  const analysis = analyzeLeads(leads);
  
  const alert = formatAlert(analysis);
  await sendAlert(alert);
}

run().catch(console.error);
