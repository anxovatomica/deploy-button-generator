# Deploy This Button Generator — One-Shot Deploy Script
# Run: chmod +x deploy.sh && ./deploy.sh
# This deploys the app itself to Render (dog food!)

set -e

echo "🔧 Deploy Button Generator — Deploy Script"
echo "=========================================="

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 not found. Please install Python 3.11+."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
venv/bin/pip install -r requirements.txt --quiet

# Start the app
echo ""
echo "🚀 Starting the Deploy Button Generator..."
echo ""
echo "   Local:    http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop."
echo ""

venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000