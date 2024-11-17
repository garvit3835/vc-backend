# investor db data
from flask import request, jsonify
from db.connection import Database

def investor_details():
    data = request.get_json()
    if not data or "investor_id" not in data:
        return jsonify({"message": "Invalid request. 'investor_id' is required."}), 400

    investor_id = data['investor_id']
    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to fetch investor details for the given investor_id
        cursor.execute(
            "SELECT * FROM investors WHERE investorid = %s",
            (investor_id,)
        )
        result = cursor.fetchone()
        
        # Get column names for formatting the result
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()

        if result:
            # Format result as a dictionary
            investor_details = dict(zip(column_names, result))
            return jsonify({"message": "Investor details fetched successfully!", "investor_details": investor_details}), 200
        else:
            return jsonify({"message": "Investor not found."}), 404
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)
