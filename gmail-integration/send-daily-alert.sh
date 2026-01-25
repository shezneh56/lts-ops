#!/bin/bash

cd /root/clawd/gmail-integration

# Run the daily alert and capture output
ALERT=$(node daily-alert.js 2>&1 | tail -n +4 | head -n -1)

# Send via WhatsApp using Clawdbot message tool
# For now, we'll use a simple approach - save to file for pickup
cat > /root/clawd/daily-alert-output.txt << EOF
$ALERT
EOF

echo "Alert generated at $(date)"
