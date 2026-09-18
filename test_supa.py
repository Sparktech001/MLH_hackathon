import sys
import os

# Ensure the backend module is in the path
sys.path.append(os.path.dirname(__file__))

from backend.services.supabase_client import supabase

def test_connection():
    try:
        print("Testing connection to Supabase via REST API...")
        
        # Test 1: Users table
        response = supabase.table("users").select("*").limit(1).execute()
        print("SUCCESS: Connected to 'users' table!")
        
        # Test 2: Document Chunks table (verifies pgvector setup)
        res2 = supabase.table("document_chunks").select("id").limit(1).execute()
        print("SUCCESS: Connected to 'document_chunks' table!")
        
        print("ALL GOOD: Supabase is fully configured and accessible from Python!")
        
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
