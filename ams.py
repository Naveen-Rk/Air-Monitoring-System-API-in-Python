from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime, uuid
from flask_restful import Api, Resource
from itsdangerous import URLSafeSerializer
from functools import wraps
from validate_email import validate_email
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_mqtt import Mqtt
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/ams'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = "52.36.175.99"
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
controllerregisteration = "air/controller/interns/register"
controllervalue = "air/controller/interns/status"

db = SQLAlchemy(app)
mqtt = Mqtt(app)

@app.route('/')
def index():
    return 'index'

class dbcon(db.Model):
    __tablename__ = 'user'
    user_no = db.Column('USER_NO', db.INTEGER, primary_key=True, nullable=False)
    email = db.Column('USER_EMAIL_ID', db.String(50), nullable=False)
    password = db.Column('USER_PASSWORD', db.String(80), nullable=False)
    mobile = db.Column('USER_MOBILE', db.INTEGER, nullable=False)
    username = db.Column('USER_NAME', db.String(30), nullable=False)
    user_company_name = db.Column('USER_COMPANY_NAME', db.String(30), nullable=False)
    user_company_address = db.Column('USER_COMPANY_ADDRESS', db.String(50), nullable=False)
    user_active = db.Column('USER_ACTIVE', db.Boolean)
    user_create_ts = db.Column('USER_CREATE_TS', db.DATETIME, nullable=False, onupdate=datetime.datetime.now,
                               default=datetime.datetime.now)
    user_update_ts = db.Column('USER_UPDATE_TS', db.DATETIME, default=datetime.datetime.now, nullable=False)

    def __init__(self, user_no, email, password, mobile, username, user_company_name, user_company_address, user_active,
                 user_create_ts, user_update_ts):
        self.user_no = user_no
        self.email = email
        self.password = password
        self.mobile = mobile
        self.username = username
        self.user_company_name = user_company_name
        self.user_company_address = user_company_address
        self.user_active = user_active
        self.user_create_ts = user_create_ts
        self.user_update_ts = user_update_ts


class controller(db.Model):
    controller_id = db.Column('CONTROLLER_ID', db.INTEGER, primary_key=True, nullable=False, autoincrement= True)
    controller_user = db.Column('CONTROLLER_USER_ID', db.INTEGER, db.ForeignKey('user.USER_NO'),
                                nullable=False)
    controller_number = db.Column('CONTROLLER_NUMBER', db.INTEGER, primary_key=True, nullable=False)
    cName = db.Column('CONTROLLER_NAME', db.String(35), nullable=False)
    controller_create_ts = db.Column('CONTROLLER_CREATE_TS', db.DATETIME, nullable=False,
                                     onupdate=datetime.datetime.now,
                                     default=datetime.datetime.now)
    controller_update_ts = db.Column('CONTROLLER_UPDATE_TS', db.DATETIME, default=datetime.datetime.now, nullable=False)

    def __init__(self, controller_id, controller_user, controller_number, cName,
                 controller_create_ts, controller_update_ts):
        self.controller_id = controller_id
        self.controller_user = controller_user
        self.controller_number = controller_number
        self.cName = cName
        self.controller_create_ts = controller_create_ts
        self.controller_update_ts = controller_update_ts


# Method to throw invalid JSON key value
def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 404
    return response


# Method to throw abort error


@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description})
    return response


# Method to throw invalid JSON Parameter Type


def bad_request403(message):
    response = jsonify({'message': message})
    response.status_code = 403
    return response


def success_response(code, message, data):
    response = jsonify({'message': message, 'data': data})
    response.status_code = code
    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'})

        try:
            s = URLSafeSerializer(app.config['SECRET'], salt='activate-salt')
            data = s.loads(token)
            current_user = dbcon.query.filter_by(email=data['email']).first()

        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user)

    return decorated


def return_profile(no, mail, password, mobile, user_name, comp_name, comp_address):
    response = jsonify({'userno': no, 'email_id': mail, 'password': password, 'mobile': mobile, 'user_name': user_name,
                        'comp_name': comp_name, 'comp_address': comp_address})
    response.status_code = 200
    return response


def add_controller(uID, mA, cName):
    with app.app_context():
        new_controller = controller(controller_id=1, controller_user=uID, controller_number=mA,
                                    cName=cName,
                                    controller_create_ts=datetime.datetime.now(),
                                    controller_update_ts=datetime.datetime.now())
        db.session.add(new_controller)
        db.session.commit()
        return jsonify({'message': 'New Controller Created'})


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Mqtt connected")
    mqtt.subscribe(controllerregisteration)
    mqtt.subscribe(controllervalue)


@mqtt.on_subscribe()
def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed to Topic: " + controllerregisteration)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(client, userdata, message.payload.decode(), message.topic)
    data = message.payload.decode()
    value = json.loads(data)

    if message.topic == controllerregisteration:
        add_controller(**value)

    elif message.topic == controllervalue:
        mqtt.publish('controller/value', message.payload.decode())

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
    # print(level, buf)

class login(Resource):

    def post(self):

        data = request.get_json(force=True)
        data = json.loads(data)

        if not request.json:
            abort(400, 'Invalid JSON Type')

        if not 'username' in request.json or not 'password' in request.json:
            return bad_request('Invalid JSON Key')
        active = dbcon.query.filter_by(email=data['username']).first()
        # checking for active state of the user
        if active:
            if not data or not data['username'] or not data['password']:
                return bad_request403('Login required')

            # checking for username availability
            if active.user_active:
                return bad_request403('User already logged in')

            # verifying password
            if check_password_hash(active.password, data['password']):
                s = URLSafeSerializer(app.config['SECRET'], salt='activate-salt')  # Token creation
                active.user_active = 1
                db.session.commit()
                respdata = {
                    'userID': active.user_no,
                    'token': s.dumps({'email': active.email})
                }
                return success_response(200, 'Login Success', respdata)
            return bad_request403('Authentication failed! wrong password')
        else:
            return bad_request403('User not exists')

    def get(self):
        return bad_request("method not supported")

    @token_required
    def delete(current_user):
        id = current_user.email

        user = dbcon.query.filter_by(email=id).first()

        user.user_active = 0
        db.session.commit()
        return jsonify({'message': 'User successfully logged out'})

    def put(self):
        return bad_request('method type not supported')


class register(Resource):

    @token_required
    def get(current_user):

        id = current_user.email

        user = dbcon.query.filter_by(email=id).first()

        if user:
            return return_profile(user.user_no, user.email, user.password, user.mobile, user.username, user.user_company_name,
                                  user.user_company_address)

    @token_required
    def delete(current_user):

        id = current_user.email

        user = dbcon.query.filter_by(email=id).delete()

        if user:
            return jsonify({'message': 'User Successfully deleted'})
        else:
            return jsonify({'message': 'User cannot be deleted'})


    @token_required
    def put(current_user):

        data = request.get_json()

        if not request.json:
            abort(400, 'Invalid JSON Type')

        if not 'username' in request.json or not 'password' in request.json \
                or not 'deviceid' in request.json or not 'email' in request.json \
                or not 'user_company_name' in request.json or not 'user_company_address' in request.json \
                or not 'mobile' in request.json:
            return bad_request('Invalid JSON Key')

        if type(request.json['username']) is not str and len(data['username']) < 3 or len(data['username']) > 30:
            return bad_request403('username must be string')

        if type(request.json['email']) is not str or not validate_email(data['email']):
            return bad_request403('Enter valid email address')

        if len(data['password']) < 6 or len(data['password']) > 10 and not data['password'].isalnum():
            return bad_request403('Password should contain minimum of 6 and maximum of 10 alphanumeric characters')

        if len(data['user_company_name']) < 3 or len(data['user_company_name']) > 30:
            return bad_request403('Company name should contain minimum of 3 and maximum of 30 alphabets')

        if len(data['user_company_address']) > 50:
            return bad_request403('Company address shall be maximum of 50 characters')

        if len(data['mobile']) > 10 or len(data['mobile']) < 10 and not data['mobile'].isdigit():
            return bad_request403('Please enter valid mobile number')

        hashed_password = generate_password_hash(data['password'], method='sha256')

        userid = current_user.email
        user = dbcon.query.filter_by(email=userid).first()

        user.password = hashed_password
        user.user_company_name = data['user_company_name']
        user.user_company_address = data['user_company_address']
        user.mobile = data['mobile']

        db.session.commit()

    def post(self):
        data = request.get_json()

        if not request.json:
            abort(400, 'Invalid JSON Type')

        if not 'username' in request.json or not 'password' in request.json \
                or not 'email' in request.json \
                or not 'company_name' in request.json or not 'user_company_address' in request.json \
                or not 'mobile' in request.json:
            return bad_request('Invalid JSON Key')

        if type(request.json['username']) is not str and len(data['username']) < 3 or len(data['username']) > 30:
            return bad_request403('username must be string')

        if type(request.json['email']) is not str or not validate_email(data['email']):
            return bad_request403('Enter valid email address')

        if len(data['password']) < 6 or len(data['password']) > 10 and not data['password'].isalnum():
            return bad_request403('Password should contain minimum of 6 and maximum of 10 alphanumeric characters')

        if len(data['user_company_name']) < 3 or len(data['user_company_name']) > 30:
            return bad_request403('Company name should contain minimum of 3 and maximum of 30 alphabets')

        if len(data['user_company_address']) > 50:
            return bad_request403('Company address shall be maximum of 50 characters')

        if len(data['mobile']) > 10 or len(data['mobile']) < 10 and not data['mobile'].isdigit():
            return bad_request403('Please enter valid mobile number')

        hashed_password = generate_password_hash(data['password'], method='sha256')

        mob = dbcon.query.filter_by(mobile=data['mobile'], email=data['email']).first()
        if not mob:
            new_user = dbcon(user_no=str(uuid.uuid4()), email=data['email'], password=hashed_password,
                             mobile=data['mobile'], username=data['username'],
                             user_company_name=data['user_company_name'],
                             user_company_address=data['user_company_address'], user_active=False,
                             user_create_ts=datetime.datetime.now(), user_update_tsxamp=datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'New User Created'})

        else:
            return jsonify({'message': 'User already exists'})



api.add_resource(login, '/login')
api.add_resource(register, '/register')
if __name__ == '__main__':
    app.run(debug=True, host='192.168.43.217', port=5050)
    # app.run(debug=True, host='192.168.2.79', port=5050)
    # app.run(debug=True, host='127.0.0.1', port=5050)
    # socketio.run(app, host='127.0.0.1', port=5050, use_reloader=True, debug=True)