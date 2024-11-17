from flask import request, jsonify
from db.connection import Database

def startup_details():
    data = request.get_json()
    if not data or "startup_id" not in data:
        return jsonify({"message": "Invalid request. 'startup_id' is required."}), 400

    startup_id = data["startup_id"]
    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to fetch the startup details
        cursor.execute(
            "SELECT * FROM startups WHERE startupid = %s",
            (startup_id,)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            # Extract column names to return a proper JSON response
            column_names = [desc[0] for desc in cursor.description]
            startup_details = dict(zip(column_names, result))
            return jsonify({"startup_id": startup_id, "startup_details": startup_details}), 200
        else:
            return jsonify({"message": "Startup not found."}), 404
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)


# predicted valuation // VAR

# startup db details

# current investor

# founder details

