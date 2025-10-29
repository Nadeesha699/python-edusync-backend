from flask import Blueprint, request, jsonify
from db import get_db_connection

studentmarks_bp = Blueprint('studentmarks_bp',__name__)

@studentmarks_bp.route("/get-all",methods=['GET'])
def get_all_studentmarks():

    con = None
    cursor = None

    try:
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("SELECT * FROM studentmarks")
      students = cursor.fetchall()

      return jsonify(students)
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 

@studentmarks_bp.route("/get-by-id/<int:id>",methods=['GET'])
def get_studentmark_by_id(id):

    con = None
    cursor = None

    try:
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("SELECT * FROM studentmarks WHERE id = %s",(id,))
      students = cursor.fetchall()

      return jsonify(students)
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close()

@studentmarks_bp.route("/get-by-index/<string:index>",methods=['GET'])
def get_studentmark_by_index(index):

    con = None
    cursor = None

    try:
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("SELECT * FROM studentmarks WHERE student_index = %s",(index,))
      students = cursor.fetchone()

      return jsonify(students)
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close()            


@studentmarks_bp.route("/save", methods=['POST'])
def save():

    con = None
    cursor = None

    try:

      
      data = request.get_json()
      student_index = data.get("student_index")
      marks = data.get("marks")
      student_name = data.get("student_name")
      batch = data.get("batch")

      if not all([student_index,marks,student_name,batch]):
         return jsonify({"error": "All fields are required"}), 400
      
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)

      cursor.execute("SELECT * FROM studentmarks WHERE student_index = %s",(student_index,))
      student = cursor.fetchone()

      if student is None:
         cursor.execute("INSERT INTO studentmarks (student_index, marks, student_name) VALUES ( %s, %s, %s )",(student_index, marks, student_name))
         con.commit()

         return jsonify({"message":"marks added suceessfully"}),201
      else:
         
         return jsonify({"error":"duplicate index, cannot add marks"}),409
  
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
    
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close() 
    
@studentmarks_bp.route("/update-by-id/<int:id>", methods=['PUT'])
def update(id):

    con = None
    cursor = None

    try:
      data = request.get_json()

      student_index = data.get("student_index")
      marks = data.get("marks")
      student_name = data.get("student_name")
      batch = data.get("batch")

      if not all([student_index,marks,student_name,batch,id]):
         return jsonify({"error": "All fields are required"}), 400
      
      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("UPDATE studentmarks SET student_index = %s, marks = %s, student_name = %s WHERE id = %s",(student_index, marks, student_name, id))
      con.commit()

      return jsonify({"message":"marks updated suceessfully"}),200
    
    except Exception as e:
      return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500 
     
    finally:
       if cursor:
          cursor.close()
       if con:
          con.close()   
    
    
@studentmarks_bp.route("/delete-by-id/<int:id>", methods=['DELETE'])
def delete(id):

    con = None
    cursor = None
    
    try:

      con = get_db_connection()
      cursor = con.cursor(dictionary=True)
      cursor.execute("DELETE FROM studentmarks WHERE id = %s",(id,))
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
            


