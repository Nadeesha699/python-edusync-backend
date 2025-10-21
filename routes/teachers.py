from flask import Blueprint, request, jsonify
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

teachers_bp = Blueprint('teachers_bp',__name__)

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
             return jsonify({"message":"login successfully","user id": teacher['id']}),200
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
         return jsonify({"verify":True}),200
      else:
         return jsonify({"verify":False}),200

   except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
   finally:
      if cursor:
         cursor.close()
      if con:
         con.close() 





            


