import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db ,User,Certificate

#UPLOAD_FOLDER ='static'


app=Flask(__name__)
app.url_map.strict_slashes= False
app.config['DEBUG']=True
app.config['ENV']='development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['JWT_SECRET_KEY']='secret-key'
#app.config['UPLOAD_FOLDER']= UPLOAD FOLDER

db.init_app(app)
Migrate(app,db)
CORS(app)
jwt=JWTManager(app)
bcrypt=Bcrypt(app)



app.route('/')
def main():
    return render_template('index.htm')


@app.route('/register',methods=['POST'])
def register():
    email=request.json.get("email",None)
    password=request.json.get("password",None)
    
    if not email:
        return jsonify({"msg":"Email requerido"}),200
    if not password:
        return jsonify({"msg":"Password requerdo"}),200
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        return jsonify({"msg":"Emaol ya existe"}),400
       
       
    user =User()
    user.name=request.json.get("name","")
    user.email= email
    user.password=bcrypt.generate_password_hash(password)
    
    user.save()
    
    return jsonify({"succes":"Registro Exitoso, porfavor inicia sesion"}),200




@app.route('/login' ,methods=['POST'])
def login():
    email=request.json.get("email",None)
    password=request.json.get("password",None)
    
    if not email:
        return jsonify({"msg":"Email requerido"}),200
    if not password:
        return jsonify({"msg":"Password requerdo"}),200
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"msg":"Datos de inicio de sesion incorrectos favor verfique"}),400
       
       
    if not bcrypt.check_password_hash(user.password,password):
        return jsonify({"msg":"email/password incorrectos"}),400
    
    expires= datetime.timedelta(days=3)
    
    data= {
     "access_token": create_access_token( identity=user.email, expires_delta=expires),
     "user": user.serialize()
    }

    return jsonify({"success":"Registro exitoso", "data":data}),200



if __name__== "__main__":
    app.run()
    
