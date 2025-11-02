from flask import Flask
from routes.studentmarks import studentmarks_bp
from routes.teachers import teachers_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(studentmarks_bp, url_prefix='/api/studentmarks')
app.register_blueprint(teachers_bp, url_prefix='/api/teachers')


if __name__ == '__main__':
    app.run(debug=True)
