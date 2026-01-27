#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { google } = require('googleapis');
const readline = require('readline');

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/gmail.send',
  'https://www.googleapis.com/auth/gmail.compose',
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/drive.readonly',
  'https://www.googleapis.com/auth/documents.readonly',
  'https://www.googleapis.com/auth/spreadsheets.readonly'
];
const TOKEN_PATH = path.join(__dirname, 'token.json');
const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');

async function authorize() {
  let credentials;
  try {
    const content = await fs.readFile(CREDENTIALS_PATH);
    credentials = JSON.parse(content);
  } catch (err) {
    console.error('Error loading credentials:', err);
    return;
  }

  const { client_secret, client_id, redirect_uris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  // Check if we have a token already
  try {
    const token = await fs.readFile(TOKEN_PATH);
    oAuth2Client.setCredentials(JSON.parse(token));
    console.log('✅ Already authorized!');
    return oAuth2Client;
  } catch (err) {
    // No token, need to get one
    return getNewToken(oAuth2Client);
  }
}

async function getNewToken(oAuth2Client) {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
  });

  console.log('\n🔐 Authorize this app by visiting this URL:\n');
  console.log(authUrl);
  console.log('\n');

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve, reject) => {
    rl.question('Enter the code from that page here: ', async (code) => {
      rl.close();
      try {
        const { tokens } = await oAuth2Client.getToken(code);
        oAuth2Client.setCredentials(tokens);
        await fs.writeFile(TOKEN_PATH, JSON.stringify(tokens));
        console.log('✅ Token stored to', TOKEN_PATH);
        resolve(oAuth2Client);
      } catch (err) {
        console.error('Error retrieving access token', err);
        reject(err);
      }
    });
  });
}

authorize().then(auth => {
  if (auth) {
    console.log('\n✅ Gmail integration ready!\n');
  }
}).catch(console.error);
