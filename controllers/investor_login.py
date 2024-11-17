from flask import make_response, request, jsonify
from db.connection import Database

def investor_login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Invalid request"}), 400

    username = data['username']
    password = data['password']

    connection = None
    try:
        connection = Database.get_connection()
        cursor = connection.cursor()

        # Query to verify user credentials
        cursor.execute(
            "SELECT * FROM investors WHERE username = %s AND pswd = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()

        if user:
            investor_id = user[0]  # Extract investor_id from the query result
            response = make_response(jsonify({"message": "Login successful!", "investor_id": investor_id}), 200)
            return response
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)
