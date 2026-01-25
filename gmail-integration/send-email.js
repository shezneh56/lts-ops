#!/usr/bin/env node

const nodemailer = require('nodemailer');
const fs = require('fs').promises;
const { google } = require('googleapis');
const path = require('path');

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

async function sendEmail(to, subject, body) {
  const auth = await getAuth();
  const gmail = google.gmail({ version: 'v1', auth });
  
  // Create email in RFC 2822 format
  const message = [
    `To: ${to}`,
    `Subject: ${subject}`,
    `Content-Type: text/plain; charset=utf-8`,
    '',
    body
  ].join('\\n');
  
  const encodedMessage = Buffer.from(message)
    .toString('base64')
    .replace(/\\+/g, '-')
    .replace(/\\//g, '_')
    .replace(/=+$/, '');
  
  const result = await gmail.users.messages.send({
    userId: 'me',
    requestBody: {
      raw: encodedMessage
    }
  });
  
  return result.data;
}

async function sendDraft() {
  const draft = JSON.parse(await fs.readFile('/root/clawd/email-draft.json'));
  
  console.log('📧 Sending email...');
  console.log(`To: ${draft.to}`);
  console.log(`Subject: ${draft.subject}\\n`);
  
  const result = await sendEmail(draft.to, draft.subject, draft.body);
  
  console.log('✅ Email sent successfully!');
  console.log(`Message ID: ${result.id}`);
  
  return result;
}

if (require.main === module) {
  sendDraft().catch(console.error);
}

module.exports = { sendEmail, sendDraft };
