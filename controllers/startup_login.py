from flask import make_response, request, jsonify
from db.connection import Database

def startup_login():
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
            "SELECT * FROM startups WHERE username = %s AND pswd = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()

        if user:
            startup_id = user[0]
            response = make_response(jsonify({"message": "Login successful!", "startup_id": startup_id}), 200)
            # Set a cookie for the user with a key-value pair
            response.set_cookie("user", "startup", httponly=True)  # No 'secure' flag
            return response
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if connection:
            Database.release_connection(connection)