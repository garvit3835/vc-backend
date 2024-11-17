from flask import request, jsonify
from db.connection import Database

def current_investors():
    data = request.get_json()
    if not data or "startup_id" not in data:
        return jsonify({"message": "Invalid request. 'startup_id' is required."}), 400

    startup_id = data['startup_id']
    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to fetch current investors for the provided startup_id
        cursor.execute("""
            SELECT i.*, inv.*
            FROM investments i
            INNER JOIN investors inv ON i.investor = inv.investorid
            WHERE i.startup = %s
        """, (startup_id,))
        
        investors = cursor.fetchall()
        cursor.close()

        if not investors:
            return jsonify({"message": "No investors found for the given startup ID."}), 404

        # Get column names for formatting the result as a list of dictionaries
        column_names = [desc[0] for desc in cursor.description]
        investors_data = [dict(zip(column_names, investor)) for investor in investors]

        return jsonify({"message": "Investors fetched successfully!", "investors": investors_data}), 200

    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)
