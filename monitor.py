#!/usr/bin/env python3

import hashlib
import os
import requests
import sys
import time
from datetime import datetime

def calculate_file_hash(content):
    """Calculate SHA256 hash of file content"""
    return hashlib.sha256(content).hexdigest()

def get_stored_hash():
    """Get the previously stored hash from file"""
    hash_file = 'last_hash.txt'
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            return f.read().strip()
    return None

def store_hash(hash_value):
    """Store the new hash to file"""
    with open('last_hash.txt', 'w') as f:
        f.write(hash_value)

def check_file_headers(url):
    """Check file headers to get metadata without downloading"""
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none'
    }
    
    try:
        # Try HEAD request first (just headers, no download)
        print("Checking file headers...")
        response = session.head(url, headers=headers, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        # Get file metadata
        last_modified = response.headers.get('Last-Modified', '')
        etag = response.headers.get('ETag', '')
        content_length = response.headers.get('Content-Length', '')
        
        print(f"Last-Modified: {last_modified}")
        print(f"ETag: {etag}")
        print(f"Content-Length: {content_length}")
        
        # Create a signature from headers
        signature = f"{last_modified}|{etag}|{content_length}"
        return signature
        
    except requests.RequestException as e:
        print(f"HEAD request failed: {e}")
        print("Trying with GET request...")
        
        # Fallback: try minimal GET request
        try:
            response = session.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Read just first 1KB to get file signature
            chunk = response.raw.read(1024)
            response.close()
            
            # Create hash from first chunk
            import hashlib
            return hashlib.md5(chunk).hexdigest()
            
        except requests.RequestException as e2:
            print(f"Error checking file: {e2}")
            sys.exit(1)

def main():
    # Get file URL from environment
    file_url = os.environ.get('FILE_URL')
    if not file_url:
        print("ERROR: FILE_URL environment variable not set")
        sys.exit(1)
    
    print(f"Monitoring file: {file_url}")
    
    # Check file signature (headers or partial content)
    file_signature = check_file_headers(file_url)
    print(f"Current file signature: {file_signature}")
    
    # Get stored signature
    old_signature = get_stored_hash()
    print(f"Previous signature: {old_signature}")
    
    # Check if signature changed
    signature_changed = old_signature != file_signature
    
    # Set GitHub Actions outputs
    timestamp = datetime.now().isoformat()
    
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            f.write(f"hash_changed={str(signature_changed).lower()}\n")
            f.write(f"new_hash={file_signature}\n")
            f.write(f"old_hash={old_signature or 'none'}\n")
            f.write(f"timestamp={timestamp}\n")
    
    if signature_changed:
        print("🚨 File signature changed! Notification will be sent.")
        store_hash(file_signature)
    else:
        print("✅ No changes detected.")

if __name__ == "__main__":
    main()