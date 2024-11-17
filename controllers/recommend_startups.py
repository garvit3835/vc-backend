from flask import request, jsonify
from db.connection import Database
from recommendor import StartupInvestorRecommender

def recommend_startups():
    data = request.get_json()

    if not data or "investor_id" not in data:
        return jsonify({"message": "Invalid request. 'investor_id' is required."}), 400

    investor_id = data['investor_id']
    
    connection = None
    try:
        connection = Database.get_connection()
        cursor = connection.cursor()
        
        # Get top matches (list of startup_ids)
        matches = StartupInvestorRecommender.get_top_matches_for_investor(investor_id, top_n=5)
        
        if not matches:
            return jsonify({"message": "No recommendations found for this investor."}), 404
        
        # Fetch all data for the recommended startups
        cursor.execute(
            "SELECT * FROM startups WHERE startupid = ANY(%s)",
            (matches,)
        )
        startups = cursor.fetchall()
        cursor.close()
        
        # Format the response as a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        startups_data = [dict(zip(column_names, startup)) for startup in startups]

        return jsonify({"message": "Recommendations fetched successfully!", "startups": startups_data}), 200
    
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)

