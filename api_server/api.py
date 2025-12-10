from flask import Flask, jsonify
from flask_cors import CORS
from database.database import testfunc # Import utility functions and model

API_PORT = 5000 
app = Flask(__name__)
CORS(app)

# --- API Endpoints ---

@app.route('/api/stats', methods=['GET'])
def get_bot_stats():
    """
    Endpoint to retrieve data from the BotStats table.
    """
    # Use the SQLAlchemy session provided by the get_db generator
    # We only need the first (and only) row of the stats table
    db_session_generator = get_db()
    db = next(db_session_generator) # Get the session object

    # Query the first row of the BotStats table
    stats_record = db.query(BotStats).first()
    
    # Check if we found data
    if stats_record is None:
        return jsonify({"error": "No bot stats found in database"}), 404

    # Prepare data for JSON response
    stats_data = {
        # Convert SQLAlchemy object attributes to a standard Python dictionary
        "id": stats_record.id,
        "status": stats_record.status_message,
        "guild_count": stats_record.guild_count,
        "total_members": stats_record.total_members,
        "last_updated": stats_record.last_updated.isoformat() # Format datetime for JSON
    }
    
    # Clean up the session (the finally block in get_db() will close it)
    try:
        db_session_generator.close()
    except:
        pass

    # Return data with default 200 OK status
    return jsonify(stats_data) 

# --- Main Run Block ---
def run_api(): 
    print(f"Starting Flask API server on port {API_PORT}...")
    app.run(debug=True, port=API_PORT)