import requests
import time
import os

API_SERVER = "http://127.0.0.1:5000"  # Change if running on another machine
NODE_ID = os.getenv("NODE_ID")  # Get assigned node ID from Docker

if not NODE_ID:
    print(" NODE_ID environment variable not set! Exiting...")
    exit(1)

print(f" Node {NODE_ID} started. Sending heartbeats...")

while True:
    try:
        response = requests.post(f"{API_SERVER}/heartbeat", json={"node_id": NODE_ID})
        print(f" Heartbeat sent: {response.json()}")
    except Exception as e:
        print(f"Failed to send heartbeat: {e}")
    
    time.sleep(5)  # Send heartbeat every 5 seconds
