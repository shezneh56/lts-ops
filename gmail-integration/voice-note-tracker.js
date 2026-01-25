#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';
const TRACKER_FILE = '/root/clawd/voice-note-tracker.json';
const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '526d65d994ef4d78ce05616264fdd7c68dbb0b818c3f7269';

async function loadTracker() {
  try {
    const data = await fs.readFile(TRACKER_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    return { bookings: [] };
  }
}

async function saveTracker(data) {
  await fs.writeFile(TRACKER_FILE, JSON.stringify(data, null, 2));
}

async function getCurrentUser() {
  const response = await axios.get(`${CALENDLY_API}/users/me`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` }
  });
  return response.data.resource;
}

async function getRecentBookings() {
  const user = await getCurrentUser();
  const response = await axios.get(`${CALENDLY_API}/scheduled_events`, {
    headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` },
    params: {
      user: user.uri,
      count: 20,
      sort: 'start_time:desc',
      min_start_time: new Date().toISOString() // Only future events
    }
  });
  
  const events = response.data.collection;
  const bookings = [];
  
  for (const event of events) {
    try {
      const inviteesResponse = await axios.get(
        `${CALENDLY_API}/scheduled_events/${event.uri.split('/').pop()}/invitees`,
        { headers: { 'Authorization': `Bearer ${CALENDLY_API_KEY}` } }
      );
      
      const invitee = inviteesResponse.data.collection[0];
      
      bookings.push({
        eventUri: event.uri,
        name: invitee.name,
        email: invitee.email,
        startTime: event.start_time,
        timezone: invitee.timezone || 'America/New_York',
        bookedAt: invitee.created_at,
        status: event.status
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return bookings;
}

async function sendWhatsApp(message) {
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
  } catch (err) {
    console.error('WhatsApp error:', err.message);
  }
}

function getProspectLocalTime(timezone) {
  return new Date().toLocaleString('en-US', { 
    timeZone: timezone,
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

async function checkReminders() {
  const tracker = await loadTracker();
  const bookings = await getRecentBookings();
  const now = new Date();
  const nowCET = new Date().toLocaleString('en-US', { timeZone: 'Europe/Madrid' });
  const hourCET = parseInt(nowCET.split(',')[1].trim().split(':')[0]);
  
  let updated = false;
  
  // Check for new bookings
  for (const booking of bookings) {
    const existing = tracker.bookings.find(b => b.eventUri === booking.eventUri);
    
    if (!existing) {
      // New booking detected!
      tracker.bookings.push({
        ...booking,
        voiceNoteSent: false,
        reminders: []
      });
      
      await sendWhatsApp(
        `📞 *New call booked!*\n\n` +
        `👤 ${booking.name}\n` +
        `📧 ${booking.email}\n` +
        `🕐 ${new Date(booking.startTime).toLocaleString('en-US', { timeZone: 'Europe/Madrid' })} CET\n\n` +
        `🎤 *Send voice note to ${booking.name.split(' ')[0]}*`
      );
      
      tracker.bookings.find(b => b.eventUri === booking.eventUri).reminders.push({
        time: now.toISOString(),
        type: 'initial'
      });
      
      updated = true;
    }
  }
  
  // Check for 11 PM CET reminders (not sent yet)
  if (hourCET === 23) {
    for (const booking of tracker.bookings) {
      if (!booking.voiceNoteSent) {
        const last11pmReminder = booking.reminders.find(r => r.type === '11pm');
        const bookingDate = new Date(booking.bookedAt).toDateString();
        const todayDate = now.toDateString();
        
        if (!last11pmReminder && bookingDate === todayDate) {
          await sendWhatsApp(
            `⏰ *11 PM Reminder*\n\n` +
            `🎤 Send voice note to *${booking.name}*\n` +
            `📧 ${booking.email}`
          );
          
          booking.reminders.push({
            time: now.toISOString(),
            type: '11pm'
          });
          updated = true;
        }
      }
    }
  }
  
  // Check for 9 AM prospect timezone reminders (still not sent)
  for (const booking of tracker.bookings) {
    if (!booking.voiceNoteSent) {
      const prospectTime = getProspectLocalTime(booking.timezone);
      const prospectHour = parseInt(prospectTime.split(':')[0]);
      
      const last9amReminder = booking.reminders.find(r => r.type === '9am-prospect');
      
      if (prospectHour === 9 && !last9amReminder) {
        const bookingDate = new Date(booking.bookedAt);
        const daysSinceBooking = Math.floor((now - bookingDate) / (1000 * 60 * 60 * 24));
        
        if (daysSinceBooking >= 1) {
          await sendWhatsApp(
            `🌅 *9 AM Reminder (Prospect's Time)*\n\n` +
            `🎤 *STILL NEED:* Voice note to *${booking.name}*\n` +
            `📧 ${booking.email}\n` +
            `🕐 Their call: ${new Date(booking.startTime).toLocaleString('en-US', { timeZone: booking.timezone })}`
          );
          
          booking.reminders.push({
            time: now.toISOString(),
            type: '9am-prospect'
          });
          updated = true;
        }
      }
    }
  }
  
  if (updated) {
    await saveTracker(tracker);
  }
  
  return tracker;
}

// Allow manual marking as sent
async function markSent(name) {
  const tracker = await loadTracker();
  const booking = tracker.bookings.find(b => 
    b.name.toLowerCase().includes(name.toLowerCase())
  );
  
  if (booking) {
    booking.voiceNoteSent = true;
    booking.sentAt = new Date().toISOString();
    await saveTracker(tracker);
    console.log(`✅ Marked voice note sent for ${booking.name}`);
  } else {
    console.log(`❌ Not found: ${name}`);
  }
}

// CLI
const command = process.argv[2];
const arg = process.argv[3];

if (command === 'check') {
  checkReminders().then(() => console.log('✅ Reminders checked'));
} else if (command === 'mark' && arg) {
  markSent(arg);
} else if (command === 'list') {
  loadTracker().then(tracker => {
    console.log('\n📋 Voice Note Tracker:\n');
    tracker.bookings.forEach(b => {
      console.log(`${b.voiceNoteSent ? '✅' : '❌'} ${b.name} (${b.email})`);
      console.log(`   Call: ${new Date(b.startTime).toLocaleString()}`);
      console.log(`   Reminders sent: ${b.reminders.length}`);
      console.log('');
    });
  });
} else {
  console.log('Usage:');
  console.log('  node voice-note-tracker.js check       - Check for new bookings & send reminders');
  console.log('  node voice-note-tracker.js list        - List all tracked bookings');
  console.log('  node voice-note-tracker.js mark <name> - Mark voice note as sent');
}
