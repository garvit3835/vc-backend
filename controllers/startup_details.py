# equity structure
from flask import request, jsonify
from db.connection import Database

def equity_structure():
    data = request.get_json()
    if not data or "startup_id" not in data:
        return jsonify({"message": "Invalid request. 'startup_id' is required."}), 400

    startup_id = data['startup_id']
    connection = None

    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to fetch the equity structure for the given startup_id
        cursor.execute(
            "SELECT equity_structure FROM startups WHERE startupid = %s",
            (startup_id,)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            equity_structure = result[0]  # Assuming equity_structure is stored as JSONB
            return jsonify({"startup_id": startup_id, "equity_structure": equity_structure}), 200
        else:
            return jsonify({"message": "Startup not found or no equity structure available."}), 404
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)

# predicted valuation // VAR

# startup db details

# current investor

# founder details

