#!/usr/bin/env python3
"""
MongoDB Atlas Connection Tester
This script helps diagnose connection issues with MongoDB Atlas
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError

def test_connection():
    print("=" * 60)
    print("MongoDB Atlas Connection Tester")
    print("=" * 60)
    print()
    
    # Get connection string
    uri = os.environ.get("MONGODB_URI")
    
    if not uri:
        print("❌ ERROR: MONGODB_URI environment variable is not set!")
        print()
        print("Please set it using:")
        print('  export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority"')
        print()
        return False
    
    # Mask password for display
    if "@" in uri:
        parts = uri.split("@")
        if "://" in parts[0]:
            scheme_and_creds = parts[0].split("://")
            if ":" in scheme_and_creds[1]:
                username = scheme_and_creds[1].split(":")[0]
                masked_uri = f"{scheme_and_creds[0]}://{username}:***@{parts[1]}"
            else:
                masked_uri = uri
        else:
            masked_uri = uri
    else:
        masked_uri = uri
    
    print(f"✓ Connection string found")
    print(f"  {masked_uri}")
    print()
    
    # Check for common issues
    issues = []
    
    if "<password>" in uri or "<username>" in uri:
        issues.append("⚠️  Placeholder text detected! Replace <username> and <password> with actual values")
    
    if "mongodb+srv://" not in uri and "mongodb://" not in uri:
        issues.append("⚠️  Invalid URI format. Should start with 'mongodb+srv://' or 'mongodb://'")
    
    if "@" not in uri:
        issues.append("⚠️  Missing @ symbol. Format should be: mongodb+srv://username:password@host/database")
    
    if issues:
        print("POTENTIAL ISSUES DETECTED:")
        for issue in issues:
            print(f"  {issue}")
        print()
    
    # Test connection
    print("Testing connection to MongoDB Atlas...")
    print()
    
    try:
        # Create client with shorter timeout for testing
        client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        
        # Force connection
        print("  → Attempting to connect...")
        client.admin.command('ping')
        
        print("  ✅ Connection successful!")
        print()
        
        # Get database info
        db = client.get_default_database()
        if db is None:
            db = client["safepay"]
        
        print(f"  Database: {db.name}")
        print(f"  Collections: {db.list_collection_names()}")
        print()
        
        client.close()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("You can now run:")
        print("  python3 db.py")
        print("  python3 app.py")
        print()
        return True
        
    except OperationFailure as e:
        print(f"  ❌ Authentication Failed!")
        print()
        print("ERROR DETAILS:")
        print(f"  {str(e)}")
        print()
        print("COMMON CAUSES:")
        print("  1. Wrong username or password")
        print("  2. Password contains special characters that need URL encoding")
        print("  3. Database user not created in MongoDB Atlas")
        print()
        print("SOLUTIONS:")
        print("  1. Double-check your username and password in MongoDB Atlas")
        print("     → Go to: Database Access → View your user")
        print()
        print("  2. If password has special characters (@, :, /, ?, #, etc.), encode them:")
        print("     @ → %40")
        print("     : → %3A")
        print("     / → %2F")
        print("     ? → %3F")
        print("     # → %23")
        print()
        print("  3. Create a new database user:")
        print("     → MongoDB Atlas → Database Access → Add New Database User")
        print("     → Use a simple password (letters and numbers only)")
        print()
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"  ❌ Connection Timeout!")
        print()
        print("ERROR DETAILS:")
        print(f"  {str(e)}")
        print()
        print("COMMON CAUSES:")
        print("  1. IP address not whitelisted in MongoDB Atlas")
        print("  2. No internet connection")
        print("  3. Incorrect cluster hostname")
        print()
        print("SOLUTIONS:")
        print("  1. Whitelist your IP in MongoDB Atlas:")
        print("     → Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)")
        print()
        print("  2. Check your internet connection")
        print()
        print("  3. Verify the connection string from MongoDB Atlas:")
        print("     → Database → Connect → Connect your application → Copy connection string")
        print()
        return False
        
    except ConnectionFailure as e:
        print(f"  ❌ Connection Failed!")
        print()
        print("ERROR DETAILS:")
        print(f"  {str(e)}")
        print()
        print("Check your internet connection and MongoDB Atlas cluster status.")
        print()
        return False
        
    except Exception as e:
        print(f"  ❌ Unexpected Error!")
        print()
        print("ERROR DETAILS:")
        print(f"  {type(e).__name__}: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
