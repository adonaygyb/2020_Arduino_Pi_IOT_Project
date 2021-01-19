from flask import Flask, jsonify, request, redirect, render_template, Response
from flask_restful import Resource, Api
import sys

from db import db
from models.camera import VideoCamera, gen_frames
from resources.device import BluetoothDevice, Connect, Disconnect, DeviceList

# if sys.platform == 'win32':
     # print("Running on Windows OS. This is not supported yet.")
     # exit()

# from src.device_list import BtDevContainer
# Container = BtDevContainer()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pid_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# def gen_frames(camera):
#
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/")
def home():
    """
    Brief:
    Param(s):
    Return:
    """
    return render_template("index.html")

@app.route("/previously_paired")
def previously_paried():
    """
    Brief:
    Param(s):
    Return:
    """
    retDict = {}
    try:
        retDict["prev_devs"] = ['prev0', 'prev1', 'prev2']
    except Exception as e:
        print(f"Runtime error has occurred. {e}")

    return jsonify(retDict)

@app.route("/send_function_tests", methods=['GET', 'POST'])
def send_function_tests():
    """
    
    """
    devices = request.get_json()
    for test in devices["function_tests"]:
        print(f"Tests: {test}")

    retDict = {}
    retDict["function_tests"] = [
        {"test_name": "BT Connection", "test_value": True},
        {"test_name": "Video Feed", "test_value": False},
        {"test_name": "Sensor Detection", "test_value": True},
        {"test_name": "Servo Motors", "test_value": False},
    ]
    return jsonify(retDict)

<<<<<<< HEAD
@app.route("/scan")
def scan():
    """
    Brief:
    Param(s):
    Return:
    """
    retDict = {}
    try:
        #devices = Container.scan()
        #retDict["scan_devs"] = devices
        retDict["scan_devs"] = ['test1', 'test2', 'test3', 'test4']
    except Exception as e:
        print(f"Runtime error has occurred. {e}")

    return jsonify(retDict)

@app.route("/connect", methods=['GET', 'POST'])
def connect():
    """
    Brief:
    Param(s):
    Return:
    """
    devices = request.get_json()
    retValue = {}
    for device in devices["selectedDevices"]:
        print(f"Device: {device}")
  
    return jsonify({"test2": True, "test3": True}) 

@app.route("/disconnect", methods=['GET', 'POST'])
def disconnect():
    """
    Brief:
    Param(s):
    Return:
    """
    devices = request.get_json()
    retValue = {}
    for device in devices["selectedDevices"]:
        try:
            Container.remove_device(device)
            retValue[device] = True
        except Exception:
            retValue[device] = False
    return jsonify(retValue)
=======
@app.route('/video_feed')
def video_feed():
    print('Turn on Webcam')
    # return the response generated along with the specific  media
    # type (mime type)
    return Response(gen_frames(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')
>>>>>>> a2f290033573fa826ec651172fdfd7f0b347dcf4

@app.route("/send", methods=['GET', 'POST'])
def send():
    """
    Brief:
        send():

    POST:
        JSON => {selected_device_name : [ {method_name : {param_name : param_value} ] } ] }

    GET:
       JSON => {selected_device_name : {method_name : method_result} }

    """
    devices = request.get_json()
    retValue = {}
    for device_name in devices["selectedDevices"]:
        retValue[device_name] = {}
        for msg_name in devices[device_name]:
            print(f"Sending command: {msg_name} params: {devices[device_name][msg_name]}")
            try:
                retValue[device_name][msg_name] = Container.get_device(device_name).send_message(msg_name, **devices[device_name][msg_name])
            except Exception:
                print(f"Unexpected error occurred upon sending command: {msg_name}. Returning False.\n{Exception}")
                retValue[device_name][msg_name] = False

    return jsonify(retValue)

api.add_resource(Connect, '/connect')
api.add_resource(Disconnect, '/disconnect')
api.add_resource(BluetoothDevice, '/scan')
api.add_resource(DeviceList, '/devices')

if __name__ == '__main__':
    # setting the host to 0.0.0.0 makes the pi act as a server,
    # this allows users to get to the site by typing in the pi's
    # local ip address.
    # NOTE : When running the webapp you must use "sudo" for super user
    # rights to run as a server.
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
