from flask import request, jsonify
from db.connection import Database

def recommend_startups():
    data = request.get_json()

    if not data or "investor_id" not in data:
        return jsonify({"message": "Invalid request. 'investor_id' is required."}), 400

    investor_id = data['investor_id']
    startup_ids = ml_function_recommend_startups()

    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Example query: Fetch recommended startups for the given investor_id
        # This assumes there is a relationship between investors and startups (e.g., interests, previous investments).
        cursor.execute("""
            SELECT s.name, s.market_position, s.industry, s.yearly_sales
            FROM startups AS s
            JOIN investor_preferences AS ip ON ip.startup_id = s.startupid
            WHERE ip.investor_id = %s
            ORDER BY s.market_position ASC
            LIMIT 5
        """, (investor_id,))
        startups = cursor.fetchall()
        cursor.close()

        if not startups:
            return jsonify({"message": "No startups found for the given investor_id."}), 404

        # Format the response
        startup_list = [
            {
                "name": startup[0],
                "market_position": startup[1],
                "industry": startup[2],
                "yearly_sales": startup[3]
            }
            for startup in startups
        ]

        return jsonify({"recommended_startups": startup_list}), 200

    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500

    finally:
        if connection:
            Database.release_connection(connection)
