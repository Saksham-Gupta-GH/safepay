#!/bin/bash

# SafePay Runner Script
# This script helps you run the SafePay application with MongoDB Atlas

echo "======================================"
echo "SafePay Application Runner"
echo "======================================"
echo ""

# Check if MONGODB_URI is set
if [ -z "$MONGODB_URI" ]; then
    echo "⚠️  MONGODB_URI environment variable is not set!"
    echo ""
    echo "Please set it using:"
    echo "  export MONGODB_URI='your-connection-string-here'"
    echo ""
    echo "📖 See MONGODB_ATLAS_SETUP.md for detailed setup instructions."
    echo ""
    exit 1
fi

echo "✓ MongoDB URI is set"
echo ""
echo "Testing connection..."
python3 test_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "======================================"
    echo "❌ Connection test failed!"
    echo "======================================"
    echo ""
    echo "Please fix the connection issues above, then try again."
    echo ""
    echo "📖 For help, see: TROUBLESHOOTING.md"
    echo ""
    exit 1
fi

echo ""
echo "Initializing database..."
python3 db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Database initialized successfully!"
    echo ""
    echo "Starting SafePay application..."
    echo "Access the app at: http://127.0.0.1:5000"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo "======================================"
    echo ""
    python3 app.py
else
    echo ""
    echo "======================================"
    echo "❌ Database initialization failed!"
    echo "======================================"
    echo ""
    echo "📖 For help, see: TROUBLESHOOTING.md"
    echo "   Or run: python3 test_connection.py"
    echo ""
    exit 1
fi
