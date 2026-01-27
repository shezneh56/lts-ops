#!/usr/bin/env node

/**
 * Create a Gmail draft
 * Usage: node create-draft.js --to "email@example.com" --subject "Subject" --body "Body content"
 * Or pipe body: echo "content" | node create-draft.js --to "email" --subject "subject" --stdin
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const CREDENTIALS_PATH = path.join(__dirname, 'credentials.json');
const TOKEN_PATH = path.join(__dirname, 'token.json');

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { to: '', cc: '', subject: '', body: '', stdin: false };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--to' && args[i + 1]) result.to = args[++i];
    else if (args[i] === '--cc' && args[i + 1]) result.cc = args[++i];
    else if (args[i] === '--subject' && args[i + 1]) result.subject = args[++i];
    else if (args[i] === '--body' && args[i + 1]) result.body = args[++i];
    else if (args[i] === '--stdin') result.stdin = true;
  }
  
  return result;
}

async function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('readable', () => {
      let chunk;
      while ((chunk = process.stdin.read()) !== null) {
        data += chunk;
      }
    });
    process.stdin.on('end', () => resolve(data));
    
    // Timeout after 100ms if no stdin
    setTimeout(() => resolve(data), 100);
  });
}

async function createDraft(to, cc, subject, body) {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH));
  const token = JSON.parse(fs.readFileSync(TOKEN_PATH));
  
  const { client_secret, client_id, redirect_uris } = credentials.installed;
  const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
  oAuth2Client.setCredentials(token);
  
  const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
  
  // Build raw email - simple plain text
  const headers = [
    'Content-Type: text/plain; charset="UTF-8"',
    'MIME-Version: 1.0',
    `To: ${to}`,
    cc ? `Cc: ${cc}` : null,
    `Subject: ${subject}`,
    '',
    body
  ].filter(Boolean).join('\r\n');
  
  const encodedMessage = Buffer.from(headers)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
  
  const res = await gmail.users.drafts.create({
    userId: 'me',
    requestBody: {
      message: { raw: encodedMessage }
    }
  });
  
  console.log('✅ Draft created successfully');
  console.log('Draft ID:', res.data.id);
  return res.data;
}

async function main() {
  const args = parseArgs();
  
  if (!args.to || !args.subject) {
    console.error('Usage: node create-draft.js --to "email" --subject "subject" [--cc "cc"] [--body "body" | --stdin]');
    process.exit(1);
  }
  
  let body = args.body;
  if (args.stdin || !body) {
    const stdinData = await readStdin();
    if (stdinData.trim()) body = stdinData;
  }
  
  if (!body) {
    console.error('Error: No body provided. Use --body or --stdin');
    process.exit(1);
  }
  
  try {
    await createDraft(args.to, args.cc, args.subject, body);
  } catch (err) {
    console.error('Error creating draft:', err.message);
    process.exit(1);
  }
}

main();
