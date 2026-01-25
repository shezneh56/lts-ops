#!/usr/bin/env node

const axios = require('axios');

// Google Sheets ID from the URL
const SHEET_ID = '1nXeNTdObxbH723Pdlo2Op48d_CJqjCoci6oaGJV1c9o';

async function fetchSheet() {
  try {
    // Try to export as CSV (works if sheet is public)
    const csvUrl = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv`;
    const response = await axios.get(csvUrl);
    
    console.log('✅ Successfully fetched sheet:\n');
    console.log(response.data);
    
    return response.data;
  } catch (err) {
    console.error('❌ Error fetching sheet:', err.message);
    console.log('\nMake sure the sheet is shared with "Anyone with the link can view"');
  }
}

fetchSheet();
