#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs').promises;
require('dotenv').config();

const CALENDLY_API_KEY = process.env.CALENDLY_API_KEY;
const CALENDLY_API = 'https://api.calendly.com';

async function getCurrentUser() {
  const response = await axios.get(`${CALENDLY_API}/users/me`, {
    headers: {
      'Authorization': `Bearer ${CALENDLY_API_KEY}`
    }
  });
  return response.data.resource;
}

async function listScheduledEvents(maxResults = 20) {
  const user = await getCurrentUser();
  const response = await axios.get(`${CALENDLY_API}/scheduled_events`, {
    headers: {
      'Authorization': `Bearer ${CALENDLY_API_KEY}`
    },
    params: {
      user: user.uri,
      count: maxResults,
      sort: 'start_time:desc'
    }
  });
  
  return response.data.collection;
}

async function getInvitee(eventUri) {
  const response = await axios.get(`${CALENDLY_API}/scheduled_events/${eventUri.split('/').pop()}/invitees`, {
    headers: {
      'Authorization': `Bearer ${CALENDLY_API_KEY}`
    }
  });
  
  return response.data.collection[0]; // Get first invitee
}

async function getRecentBookings() {
  const events = await listScheduledEvents(10);
  const bookings = [];
  
  for (const event of events) {
    try {
      const invitee = await getInvitee(event.uri);
      
      bookings.push({
        name: invitee.name,
        email: invitee.email,
        eventName: event.name,
        startTime: event.start_time,
        status: event.status,
        createdAt: invitee.created_at,
        rescheduleUrl: invitee.reschedule_url,
        cancelUrl: invitee.cancel_url
      });
    } catch (err) {
      console.error('Error fetching invitee:', err.message);
    }
  }
  
  return bookings;
}

async function run() {
  console.log('📅 Fetching Calendly data...\n');
  
  const user = await getCurrentUser();
  console.log(`✅ Connected as: ${user.name} (${user.email})\n`);
  
  const bookings = await getRecentBookings();
  console.log(`📊 Recent bookings (${bookings.length}):\n`);
  
  bookings.forEach(booking => {
    const startTime = new Date(booking.startTime);
    const bookedAt = new Date(booking.createdAt);
    
    console.log(`📅 ${booking.name} <${booking.email}>`);
    console.log(`   Event: ${booking.eventName}`);
    console.log(`   Time: ${startTime.toLocaleString('en-US', { timeZone: 'Europe/Madrid' })} CET`);
    console.log(`   Booked: ${bookedAt.toLocaleString('en-US', { timeZone: 'Europe/Madrid' })} CET`);
    console.log(`   Status: ${booking.status}`);
    console.log('');
  });
  
  // Save for tracking
  await fs.writeFile('/root/clawd/recent-bookings.json', JSON.stringify(bookings, null, 2));
  console.log('✅ Saved to /root/clawd/recent-bookings.json');
}

run().catch(console.error);
