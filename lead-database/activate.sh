#!/bin/bash
# Helper script to activate virtual environment and load environment variables

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found. Create one from .env.example"
    echo "   cp .env.example .env"
    echo "   then edit .env with your Supabase credentials"
fi

echo "✓ Virtual environment activated"
echo ""
echo "Ready to use! Try:"
echo "  python test_mapping.py /root/clawd/sample_leads.csv"
echo "  python upload_leads.py /root/clawd/sample_leads.csv --test"
echo ""
echo "Exit with: deactivate"
