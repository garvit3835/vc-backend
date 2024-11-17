from flask import request, jsonify
from db.connection import Database

def invested_startups():
    data = request.get_json()
    if not data or "investor_id" not in data:
        return jsonify({"message": "Invalid request. 'investor_id' is required."}), 400

    investor_id = data['investor_id']
    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to join investments and startups to get startup details for the given investor_id
        query = """
            SELECT s.*, i.*
            FROM investments i
            INNER JOIN startups s ON i.startup = s.startupid
            WHERE i.investor = %s
        """
        cursor.execute(query, (investor_id,))
        startups = cursor.fetchall()
        
        # If no startups found
        if not startups:
            return jsonify({"message": "No startups found for the given investor."}), 404
        
        # Get column names and format the data
        column_names = [desc[0] for desc in cursor.description]
        startups_data = [dict(zip(column_names, startup)) for startup in startups]

        return jsonify({"message": "Invested startups fetched successfully!", "startups": startups_data}), 200
    
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    
    finally:
        if connection:
            Database.release_connection(connection)
