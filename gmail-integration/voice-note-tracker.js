#!/usr/bin/env node

/**
 * Voice Note Reminder System
 * 
 * Tracks Calendly bookings and reminds Liam to send voice notes.
 * 
 * Reminder cadence:
 * 1. Immediate: When booking detected
 * 2. 11 PM CET: If not marked done
 * 3. 9 AM prospect's timezone: If still not done
 * 
 * Usage:
 *   node voice-note-tracker.js check     - Check for new bookings, send immediate reminders
 *   node voice-note-tracker.js evening   - Send 11 PM CET reminders
 *   node voice-note-tracker.js morning   - Send 9 AM prospect timezone reminders
 *   node voice-note-tracker.js done <id> - Mark voice note as sent
 *   node voice-note-tracker.js status    - Show pending voice notes
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const TRACKER_FILE = path.join(__dirname, 'voice-note-status.json');

// Load or initialize tracker
function loadTracker() {
  try {
    return JSON.parse(fs.readFileSync(TRACKER_FILE, 'utf8'));
  } catch {
    return { bookings: {}, lastCheck: null };
  }
}

function saveTracker(data) {
  fs.writeFileSync(TRACKER_FILE, JSON.stringify(data, null, 2));
}

// Get recent Calendly bookings
async function getRecentBookings() {
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  
  try {
    // First get user URI
    const userRes = await axios.get('https://api.calendly.com/users/me', {
      headers: { Authorization: `Bearer ${CALENDLY_API_KEY}` }
    });
    const userUri = userRes.data.resource.uri;
    
    // Get scheduled events
    const eventsRes = await axios.get('https://api.calendly.com/scheduled_events', {
      headers: { Authorization: `Bearer ${CALENDLY_API_KEY}` },
      params: {
        user: userUri,
        min_start_time: weekAgo.toISOString(),
        max_start_time: new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000).toISOString(),
        status: 'active',
        count: 50
      }
    });
    
    const bookings = [];
    for (const event of eventsRes.data.collection) {
      // Get invitee details
      const inviteesRes = await axios.get(`${event.uri}/invitees`, {
        headers: { Authorization: `Bearer ${CALENDLY_API_KEY}` }
      });
      
      const invitee = inviteesRes.data.collection[0];
      if (invitee) {
        bookings.push({
          id: event.uri.split('/').pop(),
          name: invitee.name,
          email: invitee.email,
          startTime: event.start_time,
          timezone: invitee.timezone || 'America/New_York',
          createdAt: event.created_at
        });
      }
    }
    
    return bookings;
  } catch (err) {
    console.error('Error fetching Calendly:', err.response?.data || err.message);
    return [];
  }
}

// Format booking for display
function formatBooking(b) {
  const date = new Date(b.startTime);
  return `${b.name} - ${date.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' })} at ${date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Madrid' })} CET`;
}

// Check for new bookings and send immediate reminders
async function checkNewBookings() {
  const tracker = loadTracker();
  const bookings = await getRecentBookings();
  
  const newBookings = [];
  for (const booking of bookings) {
    if (!tracker.bookings[booking.id]) {
      tracker.bookings[booking.id] = {
        ...booking,
        voiceNoteSent: false,
        remindersSent: { immediate: false, evening: false, morning: false },
        addedAt: new Date().toISOString()
      };
      newBookings.push(booking);
    }
  }
  
  tracker.lastCheck = new Date().toISOString();
  saveTracker(tracker);
  
  if (newBookings.length > 0) {
    console.log(`\n🆕 ${newBookings.length} new booking(s) found:\n`);
    for (const b of newBookings) {
      console.log(`📞 ${formatBooking(b)}`);
      console.log(`   → Send voice note to ${b.name}\n`);
      tracker.bookings[b.id].remindersSent.immediate = true;
    }
    saveTracker(tracker);
    return { action: 'remind', bookings: newBookings };
  } else {
    console.log('No new bookings found.');
    return { action: 'none' };
  }
}

// Send evening reminders (11 PM CET)
async function sendEveningReminders() {
  const tracker = loadTracker();
  const pending = [];
  
  for (const [id, booking] of Object.entries(tracker.bookings)) {
    if (!booking.voiceNoteSent && !booking.remindersSent.evening) {
      const callDate = new Date(booking.startTime);
      const now = new Date();
      
      // Only remind for calls in the future or today
      if (callDate > now || callDate.toDateString() === now.toDateString()) {
        pending.push(booking);
        tracker.bookings[id].remindersSent.evening = true;
      }
    }
  }
  
  saveTracker(tracker);
  
  if (pending.length > 0) {
    console.log(`\n⏰ Evening reminder - ${pending.length} voice note(s) pending:\n`);
    for (const b of pending) {
      console.log(`📞 ${formatBooking(b)}`);
      console.log(`   → Still need to send voice note to ${b.name}\n`);
    }
    return { action: 'remind', bookings: pending };
  } else {
    console.log('No pending voice notes for evening reminder.');
    return { action: 'none' };
  }
}

// Send morning reminders (9 AM prospect timezone)
async function sendMorningReminders() {
  const tracker = loadTracker();
  const pending = [];
  const now = new Date();
  
  for (const [id, booking] of Object.entries(tracker.bookings)) {
    if (!booking.voiceNoteSent && !booking.remindersSent.morning) {
      const callDate = new Date(booking.startTime);
      
      // Check if it's around 9 AM in prospect's timezone
      // For simplicity, just check if call is today or tomorrow
      const hoursUntilCall = (callDate - now) / (1000 * 60 * 60);
      if (hoursUntilCall > 0 && hoursUntilCall < 48) {
        pending.push(booking);
        tracker.bookings[id].remindersSent.morning = true;
      }
    }
  }
  
  saveTracker(tracker);
  
  if (pending.length > 0) {
    console.log(`\n🌅 Morning reminder - ${pending.length} voice note(s) URGENT:\n`);
    for (const b of pending) {
      console.log(`🚨 ${formatBooking(b)}`);
      console.log(`   → URGENT: Send voice note to ${b.name} NOW\n`);
    }
    return { action: 'remind', bookings: pending };
  } else {
    console.log('No urgent voice notes for morning reminder.');
    return { action: 'none' };
  }
}

// Mark voice note as sent
function markDone(id) {
  const tracker = loadTracker();
  
  // Find by partial ID match
  const matchingId = Object.keys(tracker.bookings).find(k => k.includes(id) || tracker.bookings[k].name.toLowerCase().includes(id.toLowerCase()));
  
  if (matchingId) {
    tracker.bookings[matchingId].voiceNoteSent = true;
    tracker.bookings[matchingId].voiceNoteSentAt = new Date().toISOString();
    saveTracker(tracker);
    console.log(`✅ Marked voice note sent for: ${tracker.bookings[matchingId].name}`);
  } else {
    console.log(`❌ No booking found matching: ${id}`);
    console.log('Use "status" to see pending bookings.');
  }
}

// Show status
function showStatus() {
  const tracker = loadTracker();
  const pending = [];
  const done = [];
  
  for (const booking of Object.values(tracker.bookings)) {
    if (booking.voiceNoteSent) {
      done.push(booking);
    } else {
      pending.push(booking);
    }
  }
  
  console.log('\n📋 Voice Note Status\n');
  
  if (pending.length > 0) {
    console.log('⏳ PENDING:');
    for (const b of pending) {
      console.log(`   • ${formatBooking(b)} (ID: ${b.id.slice(-8)})`);
    }
  } else {
    console.log('✅ No pending voice notes!');
  }
  
  if (done.length > 0) {
    console.log('\n✅ COMPLETED (last 7 days):');
    for (const b of done.slice(-5)) {
      console.log(`   • ${formatBooking(b)}`);
    }
  }
  
  console.log(`\nLast check: ${tracker.lastCheck || 'never'}`);
}

// Main
async function main() {
  const command = process.argv[2] || 'status';
  const arg = process.argv[3];
  
  switch (command) {
    case 'check':
      await checkNewBookings();
      break;
    case 'evening':
      await sendEveningReminders();
      break;
    case 'morning':
      await sendMorningReminders();
      break;
    case 'done':
      if (!arg) {
        console.log('Usage: node voice-note-tracker.js done <name or id>');
      } else {
        markDone(arg);
      }
      break;
    case 'status':
    default:
      showStatus();
  }
}

main().catch(console.error);
