#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');

const TOKEN_PATH = path.join(__dirname, 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

async function getAuth() {
  const credentials = JSON.parse(await fs.readFile(CREDENTIALS_PATH));
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  
  const token = JSON.parse(await fs.readFile(TOKEN_PATH));
  oAuth2Client.setCredentials(token);
  
  return oAuth2Client;
}

async function listLabels() {
  const auth = await getAuth();
  const gmail = google.gmail({ version: 'v1', auth });
  
  const res = await gmail.users.labels.list({
    userId: 'me',
  });
  
  const labels = res.data.labels;
  console.log('\n📋 Your Gmail Labels:\n');
  if (labels && labels.length) {
    labels.forEach((label) => {
      console.log(`- ${label.name} (${label.id})`);
    });
  }
  
  return labels;
}

async function getRecentThreads(maxResults = 50, excludeLabel = null) {
  const auth = await getAuth();
  const gmail = google.gmail({ version: 'v1', auth });
  
  // Exclude warmup emails containing the warmup code
  let query = 'is:sent OR from:me -p0zfhi2t';
  if (excludeLabel) {
    query += ` -label:${excludeLabel}`;
  }
  
  const res = await gmail.users.threads.list({
    userId: 'me',
    maxResults: maxResults,
    q: query,
  });
  
  return res.data.threads || [];
}

async function getThreadDetails(threadId) {
  const auth = await getAuth();
  const gmail = google.gmail({ version: 'v1', auth });
  
  const res = await gmail.users.threads.get({
    userId: 'me',
    id: threadId,
  });
  
  return res.data;
}

async function analyzeThread(thread) {
  const messages = thread.messages || [];
  const firstMessage = messages[0];
  const lastMessage = messages[messages.length - 1];
  
  // Get subject
  const subjectHeader = firstMessage.payload.headers.find(h => h.name === 'Subject');
  const subject = subjectHeader ? subjectHeader.value : '(no subject)';
  
  // Get recipient/sender
  const toHeader = firstMessage.payload.headers.find(h => h.name === 'To');
  const fromHeader = lastMessage.payload.headers.find(h => h.name === 'From');
  const recipient = toHeader ? toHeader.value : '';
  const lastFrom = fromHeader ? fromHeader.value : '';
  
  // Check if last message is from you or them
  const lastIsFromYou = lastFrom.includes('liam@leadsthat.show');
  
  // Get dates
  const firstDate = new Date(parseInt(firstMessage.internalDate));
  const lastDate = new Date(parseInt(lastMessage.internalDate));
  const daysSinceLastReply = Math.floor((Date.now() - lastDate) / (1000 * 60 * 60 * 24));
  
  return {
    threadId: thread.id,
    subject,
    recipient,
    messageCount: messages.length,
    firstDate,
    lastDate,
    daysSinceLastReply,
    lastIsFromYou,
    needsFollowUp: lastIsFromYou && daysSinceLastReply >= 3,
  };
}

async function scanInbox(options = {}) {
  const {
    maxThreads = 100,
    excludeLabel = 'warmup',
    minDaysForFollowUp = 3
  } = options;
  
  console.log('\n🔍 Scanning inbox...\n');
  
  const threads = await getRecentThreads(maxThreads, excludeLabel);
  console.log(`Found ${threads.length} threads to analyze`);
  
  const needsFollowUp = [];
  const active = [];
  const waiting = [];
  
  for (const thread of threads.slice(0, 50)) { // Analyze first 50 to start
    try {
      const details = await getThreadDetails(thread.id);
      const analysis = await analyzeThread(details);
      
      if (analysis.needsFollowUp) {
        needsFollowUp.push(analysis);
      } else if (analysis.lastIsFromYou) {
        waiting.push(analysis);
      } else {
        active.push(analysis);
      }
    } catch (err) {
      console.error(`Error analyzing thread ${thread.id}:`, err.message);
    }
  }
  
  console.log('\n📊 Analysis Complete:\n');
  console.log(`✅ Active conversations (they replied): ${active.length}`);
  console.log(`⏳ Waiting for reply (you sent last): ${waiting.length}`);
  console.log(`🚨 NEEDS FOLLOW-UP (${minDaysForFollowUp}+ days): ${needsFollowUp.length}\n`);
  
  if (needsFollowUp.length > 0) {
    console.log('🚨 FOLLOW-UP REQUIRED:\n');
    needsFollowUp
      .sort((a, b) => b.daysSinceLastReply - a.daysSinceLastReply)
      .forEach(conv => {
        console.log(`📧 ${conv.recipient}`);
        console.log(`   Subject: ${conv.subject}`);
        console.log(`   Last contact: ${conv.daysSinceLastReply} days ago`);
        console.log(`   Messages: ${conv.messageCount}`);
        console.log('');
      });
  }
  
  return { needsFollowUp, active, waiting };
}

// Run based on command
const command = process.argv[2];

if (command === 'labels') {
  listLabels().catch(console.error);
} else if (command === 'scan') {
  scanInbox().catch(console.error);
} else {
  console.log('Usage:');
  console.log('  node gmail-monitor.js labels  - List all labels');
  console.log('  node gmail-monitor.js scan    - Scan inbox for follow-ups');
}
