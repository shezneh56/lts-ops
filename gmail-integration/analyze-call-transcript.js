#!/usr/bin/env node

const fs = require('fs').promises;

async function analyzeTranscript() {
  const callData = JSON.parse(await fs.readFile('/root/clawd/fathom-fareed-call.json'));
  
  const prospectName = callData.title.split(':')[0].trim();
  const firstName = prospectName.split(' ')[0];
  const transcript = callData.transcript;
  
  // Build full conversation for AI analysis
  const conversation = transcript
    .map(t => `${t.speaker.display_name}: ${t.text}`)
    .join('\n');
  
  // For now, create a structured summary prompt for Claude to analyze
  const analysisPrompt = `Analyze this sales call transcript and extract key information:

TRANSCRIPT:
${conversation}

Please extract and summarize:

1. PROSPECT'S CURRENT SITUATION:
- Business description (industry, product/service)
- ICP (ideal customer profile - company size, roles targeted)
- Average ACV (if mentioned)
- Current marketing/sales efforts and channels
- Current results/metrics (calls per week, conversion rates, etc.)
- Goals for scaling
- Pain points or challenges mentioned

2. WHAT THEY'RE LOOKING FOR:
- Specific goals (e.g., "2 more calls per week")
- Budget constraints or concerns (if mentioned)
- Timeline

3. KEY OBJECTIONS OR CONCERNS:
- Previous experiences with similar companies
- Hesitations

4. RECOMMENDED TIER:
Based on their situation, which tier (1, 2, or 3) makes most sense and why?

5. CUSTOMIZED ROI CALCULATION:
Based on their ACV and goals, calculate the ROI for the recommended tier.

Format your response as JSON with these exact keys:
{
  "currentSituation": "...",
  "goals": "...",
  "recommendedTier": 1-3,
  "recommendationReason": "...",
  "roiCalculation": "..."
}`;
  
  console.log('📊 TRANSCRIPT ANALYSIS NEEDED\\n');
  console.log('Prospect:', prospectName);
  console.log('Call Duration:', Math.round((new Date(callData.recording_end_time) - new Date(callData.recording_start_time)) / 1000 / 60), 'min');
  console.log('\\n--- FULL TRANSCRIPT ---');
  console.log(conversation.substring(0, 2000), '...\\n');
  
  console.log('\\n💡 To generate full email, I need to analyze this transcript with Claude.');
  console.log('The transcript is too long to analyze in this script alone.\\n');
  
  return {
    prospectName,
    firstName,
    conversation,
    callUrl: callData.url,
    duration: Math.round((new Date(callData.recording_end_time) - new Date(callData.recording_start_time)) / 1000 / 60),
    analysisPrompt
  };
}

analyzeTranscript().then(async data => {
  await fs.writeFile('/root/clawd/transcript-for-analysis.txt', data.conversation);
  await fs.writeFile('/root/clawd/analysis-prompt.txt', data.analysisPrompt);
  
  console.log('✅ Saved transcript to /root/clawd/transcript-for-analysis.txt');
  console.log('✅ Saved analysis prompt to /root/clawd/analysis-prompt.txt');
  console.log('\\n⏳ Ready for Claude to analyze and generate full email');
});
