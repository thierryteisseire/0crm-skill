import requests
import sys

BASE_URL = "https://vbrsrhfxfv6qk2jbrraym2a2du0qlazt.lambda-url.us-east-1.on.aws"

def test_connection(api_key):
    headers = {"x-api-key": api_key}
    
    # Test Health
    try:
        health = requests.get(f"{BASE_URL}/api/health")
        print(f"Health Check: {health.status_code} - {health.json()}")
        
        # Test Auth with Profile
        profile = requests.get(f"{BASE_URL}/api/user/profile", headers=headers)
        if profile.status_code == 200:
            print(f"Auth Success! Logged in as: {profile.json().get('id')}")
            return True
        else:
            print(f"Auth Failed: {profile.status_code} - {profile.text}")
            return False
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_api.py <API_KEY>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    test_connection(api_key)
