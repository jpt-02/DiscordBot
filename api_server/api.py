# api_server/api.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# --- Configuration ---
# You can define the port here or use environment variables
API_PORT = 5000 

app = Flask(__name__)

# Apply CORS to the application. This is crucial for local development 
# where React is likely on port 5173 and Flask is on 5000.
# The `origins='*'` allows requests from any origin (be cautious with this
# in production, you might restrict it to your specific frontend URL).
CORS(app) 

# --- API Endpoints ---

@app.route('/api/stats', methods=['GET'])
def get_bot_stats():
    """
    Endpoint to retrieve data from the Discord bot.
    In a real application, this would query a shared database.
    """
    
    # Placeholder data: Replace this with logic that reads data 
    # from your shared resource (like a database)
    stats_data = {
        "status": "online",
        "guild_count": 7,
        "total_members": 4500,
        "latency_ms": 50,
        "last_updated": "2025-12-09T15:55:00Z"
    }
    
    return jsonify(stats_data)

@app.route('/api/command', methods=['POST'])
def send_bot_command():
    """
    Endpoint to receive a command from the web UI and queue it for the bot.
    """
    
    # Ensure the request body is JSON
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    command_data = request.get_json()
    command = command_data.get('command')
    target_user = command_data.get('user_id') 

    if not command:
        return jsonify({"error": "Missing 'command' parameter"}), 400

    # --- CRITICAL INTEGRATION POINT ---
    # Here, you would write the command and its parameters into your 
    # shared database table (or queue) so the running Discord bot can pick it up.
    
    print(f"Received command: '{command}' for user: {target_user}. Writing to queue...")
    
    # Placeholder success response
    return jsonify({
        "status": "pending", 
        "message": f"Command '{command}' successfully sent to bot queue.",
        "details": command_data
    }), 202 # Use 202 Accepted, as the bot hasn't executed it yet

# --- Main Run Block ---
if __name__ == '__main__':
    print(f"Starting Flask API server on port {API_PORT}...")
    app.run(debug=True, port=API_PORT)