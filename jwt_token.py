from flask import request, jsonify
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token missing"}), 403
        try:
           decoded= jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 403
        except Exception as e:
            return jsonify({"message": "Invalid token"}), 403
        return func(decoded, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper