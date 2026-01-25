#!/usr/bin/env node

const fs = require('fs').promises;

async function generateEmail() {
  const callData = JSON.parse(await fs.readFile('/root/clawd/fathom-fareed-call.json'));
  
  // Extract key info
  const prospectName = callData.title.split(':')[0].trim();
  const transcript = callData.transcript;
  
  // Build a summary from transcript
  const conversationPoints = transcript
    .map(t => `${t.speaker.display_name}: ${t.text}`)
    .join('\n');
  
  // Create email draft
  const email = {
    to: 'liamsheridanlfc@gmail.com', // TEST EMAIL
    realProspect: prospectName, // Would be extracted from calendar_invitees
    subject: `Great speaking with you - ${prospectName}`,
    body: `Hi ${prospectName.split(' ')[0]},\n\nGreat connecting today! Thanks for taking the time to walk through your current outbound setup and goals.\n\n**Quick Recap:**\n• Discussed your current lead generation challenges\n• Reviewed our multi-channel approach (Email → LinkedIn → Calling)\n• Covered our TAM coverage model (reaching every decision-maker every 45-60 days)\n\n**Next Steps:**\n• I'll send over a proposal outlining how we'd approach your specific market\n• We can schedule a follow-up call once you've had a chance to review\n\n**Recording:**\nHere's the link to our conversation for your reference: ${callData.url}\n\nLooking forward to working together!\n\nBest,\nLiam\n\n---\nLiam Sheridan\nLeads That Show\nleadsthat.show`,
    callUrl: callData.url,
    duration: Math.round((new Date(callData.recording_end_time) - new Date(callData.recording_start_time)) / 1000 / 60),
    transcript: conversationPoints.substring(0, 5000) // First 5000 chars for reference
  };
  
  return email;
}

generateEmail().then(email => {
  console.log('📧 DRAFT EMAIL\\n');
  console.log(`To: ${email.to} (TEST - would normally go to ${email.realProspect})`);
  console.log(`Subject: ${email.subject}\\n`);
  console.log(`Body:\\n${email.body}\\n`);
  console.log(`Call Duration: ${email.duration} minutes`);
  console.log(`Call URL: ${email.callUrl}`);
  
  // Save draft
  fs.writeFile('/root/clawd/email-draft.json', JSON.stringify(email, null, 2));
  console.log('\\n✅ Draft saved to /root/clawd/email-draft.json');
});
