#!/bin/bash

# Log in and extract token from JSON response
LOGIN_URL="http://localhost:8000/token"
RESPONSE=$(curl -s -X POST $LOGIN_URL \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=secret")

# Extract token from JSON
TOKEN=$(echo $RESPONSE | jq -r '.access_token')

# Save to a file for later use
echo $TOKEN > token.txt
