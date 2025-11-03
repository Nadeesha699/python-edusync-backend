import random
from flask import Blueprint, request, jsonify
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from dotenv import load_dotenv
import os
import datetime
from email_service import send_otp
from jwt_token import token_required_for_decode_only


teachers_bp = Blueprint('teachers_bp',__name__)

load_dotenv()

OTP_STORE = {} 

@teachers_bp.route("/register", methods=['POST'])
def register():

    con = None
    cursor = None

    try:
      
      data = request.get_json()
      name = data.get("name")
      phone_number = data.get("phone_number")
      email = data.get("email")
      password = data.get("password")

      if not all([name,phone_number,password,email]):
         return jsonify({"error": "All fields are required"}), 400

      hashed_password = generate_password_hash(password)

      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("INSERT teachers ( name, phone_number, email, password  ) VALUES ( %s, %s, %s, %s )",(name, phone_number, email, hashed_password))
      con.commit()

      return jsonify({"message":"marks added suceessfully"}),201
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 
    
@teachers_bp.route("/update-by-id/<int:id>", methods=['PUT'])
def update(id):

    con = None
    cursor = None

    try:
      data = request.get_json()

      name = data.get("name")
      phone_number = data.get("phone_number")
      email = data.get("email")
      password = data.get("password")

      if not all([name,phone_number,password,email,id]):
         return jsonify({"error": "All fields are required"}), 400
      
      hashed_password = generate_password_hash(password)

      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("UPDATE teachers SET name = %s, phone_number = %s, email = %s, password = %s WHERE id = %s",(name, phone_number, email, hashed_password, id))
      con.commit()

      return jsonify({"message":"User updated suceessfully"}),200

    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500 
     
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 

@teachers_bp.route("/get-by-id/<int:id>",methods=['GET'])
def get_teacher_by_id(id):

    con = None
    cursor = None

    try:
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("SELECT * FROM teachers WHERE id = %s",(id,))
      teacher = cursor.fetchall()

      return jsonify(teacher)
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close()              
    
    
@teachers_bp.route("/delete-by-id/<int:id>", methods=['DELETE'])
def delete(id):

    con = None
    cursor = None

    try:

      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("DELETE FROM teachers WHERE id = %s",(id,))
      con.commit()

      if cursor.rowcount == 0:
         return jsonify({"message": f"No record found with ID {id}"}), 404
      else:
         return jsonify({"message": f"Record with ID {id} deleted successfully"}),200
             
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 



@teachers_bp.route("/login", methods=['POST'])
def login():

    con = None
    cursor = None

    try:
      
      data = request.get_json()
      email = data.get("email")
      password = data.get("password")

      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("SELECT * FROM teachers WHERE email = %s",(email,))
      teacher = cursor.fetchone()

      if teacher != None :
          if check_password_hash(teacher['password'],password):

            token = jwt.encode({"user_id":teacher['id'],
                         "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                        #  "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                         os.getenv('SECRET_KEY'),
                         algorithm='HS256')
            
            return jsonify({"message":"login successfully","token": token}),200
          else:
             return jsonify({"message":"login failed, incorrect password"}),401    
      else:
         return jsonify({"message":"login failed, incorrect email"}),401

      
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 
               


@teachers_bp.route('/verify-email/<string:email>',methods=['POST'])
def email_verify(email):
   con = None
   cursor = None

   try:
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute('SELECT * FROM teachers WHERE email = %s',(email,))
      result = cursor.fetchone()

      if result != None:
         return jsonify(result),200
      else:
         return jsonify(result),404

   except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
   finally:
      if cursor:
         cursor.close()
      if con:
         con.close()        

@teachers_bp.route("/decode",methods=['GET'])
@token_required_for_decode_only
def decode_token(decoded):
  user_id =  decoded['user_id']
  return jsonify({"user_id":user_id})


@teachers_bp.route('/send-otp', methods=['POST'])
def send_otp_route():
    otp = random.randint(100000, 999999)
    
   #  Get JSON data from request
    data = request.get_json()

    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = data.get('receiver_email')
    subject = 'EduSync ICT Teacher Password Change Verification'  
    body = f"""
Dear ICT Teacher,

We received a request to change your EduSync account password.

To verify this action, please use the One-Time Password (OTP) provided below:

🔐 Your OTP Code: {otp}

This code will expire in 5 minutes.

If you did not request this change, please ignore this email or contact EduSync Support immediately.

Best regards,  
EduSync ICT Support Team

"""
    app_password = os.getenv('GMAIL_APP_PASSWORD') # App password for Gmail

   #  Call the send_email function
    otp = send_otp(sender_email, receiver_email, subject, body, app_password,otp)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    OTP_STORE[receiver_email] = {"otp":otp,"expiry":expiry} 
    print(f"[DEBUG] OTP for {receiver_email}: {otp}")

    return jsonify({"message": "OTP sent successfully"})


@teachers_bp.route('/verify-otp',methods=['POST'])
def verify_otp():
  data =  request.get_json()
  otp = int(data['otp'])
  email = data['email']

  record = OTP_STORE.get(email)

  if not record:
     return jsonify({"message":"We couldn’t find an OTP for this email. Please request a new one."}),400
  
  if datetime.datetime.utcnow() > record["expiry"]:
     return jsonify({"message": "Your OTP has expired. Please request a new code to continue."}), 400
  
  if otp != record["otp"]:
     return jsonify({"message": "The OTP you entered is incorrect. Please try again"}), 400
  
  return jsonify({"message": "OTP verified successfully"}),200
     









            


