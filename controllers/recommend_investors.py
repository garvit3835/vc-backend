from flask import request, jsonify
from db.connection import Database
from ml.data import startups_df , investors_df
from ml.recommendor import StartupInvestorRecommender
import numpy as np

recommender = StartupInvestorRecommender(startups_df , investors_df)

def recommend_investors():
    data = request.get_json()

    if not data or "startup_id" not in data:
        return jsonify({"message": "Invalid request. 'startup_id' is required."}), 400

    startup_id = data['startup_id']
    
    connection = None
    try:
        connection = Database.get_connection()
        cursor = connection.cursor()
        
        # Get top matches (list of investor_ids)
        # matches = recommender.get_top_matches_for_startup(startup_id, top_n=5)
        matches= [1, 2, 3, 4, 5]

        matches = matches.tolist() if isinstance(matches, np.ndarray) else matches

        
        if not matches:
            return jsonify({"message": "No recommendations found for this startup."}), 404
        
        # Fetch all data for the recommended investors
        cursor.execute(
            "SELECT * FROM investors WHERE investorid = ANY(%s)",
            (matches,)
        )
        investors = cursor.fetchall()
        cursor.close()
        
        # Format the response as a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        investors_data = [dict(zip(column_names, investor)) for investor in investors]

        return jsonify({"message": "Recommendations fetched successfully!", "investors": investors_data}), 200
    
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)