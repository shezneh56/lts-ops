#!/usr/bin/env node

const { google } = require('googleapis');
const fs = require('fs').promises;
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

async function sendEmail() {
  const auth = await getAuth();
  const gmail = google.gmail({ version: 'v1', auth });
  
  const emailContent = await fs.readFile('/root/clawd/email-to-send.txt', 'utf8');
  
  // Convert to HTML with proper formatting
  const htmlBody = emailContent
    .split('\n\n')
    .map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`)
    .join('\n');
  
  const message = [
    'To: liamsheridanlfc@gmail.com',
    'From: Liam Sheridan <liam@leadsthat.show>',
    'Subject: Great speaking with you - Fareed Aziz',
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=utf-8',
    '',
    `<html><body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 650px;">`,
    htmlBody,
    `</body></html>`
  ].join('\n');
  
  const encodedMessage = Buffer.from(message)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
  
  const result = await gmail.users.messages.send({
    userId: 'me',
    requestBody: { raw: encodedMessage }
  });
  
  console.log('✅ Email sent successfully!');
  console.log('To: liamsheridanlfc@gmail.com');
  console.log('From: Liam Sheridan <liam@leadsthat.show>');
  console.log('Subject: Great speaking with you - Fareed Aziz');
  console.log('Message ID:', result.data.id);
  
  return result.data;
}

sendEmail().catch(console.error);
