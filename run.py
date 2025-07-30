#!/usr/bin/env python3
"""
CrickConnect - Cricket Community Platform
Run Script

This script starts the CrickConnect Flask application.
"""

import os
import sys
from app import app, db

def create_database():
    """Create database tables if they don't exist."""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def main():
    """Main function to run the application."""
    print("🏏 Starting CrickConnect - Cricket Community Platform")
    print("=" * 50)
    
    # Create database tables
    create_database()
    
    # Get configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Server starting on http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("=" * 50)
    print("📝 First registered user will become the platform owner!")
    print("🚀 Ready to connect cricket enthusiasts worldwide!")
    print("=" * 50)
    
    try:
        # Run the Flask application
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 CrickConnect server stopped. Thank you for using our platform!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()