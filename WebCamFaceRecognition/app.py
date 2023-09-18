import base64
from flask import Flask, render_template, request, jsonify, redirect, url_for
import string
import random
import requests
import io
from PIL import Image
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('master.html')

@app.route('/registersuccess')
def registersuccess():
    return render_template('registersuccess.html')
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerfail')
def registerfail():
    return render_template('registerfail.html')

@app.route('/verficationsuccess')
def verficationsuccess():
    first_name = request.args.get('firstName')
    print(first_name)
    last_name = request.args.get('lastName')
    print(last_name)
    phone_number = request.args.get('phoneNumber')
    print(phone_number)
    dob = request.args.get('dob')
    print(dob)
    face_confidence = request.args.get('faceConfidence')
    print(face_confidence)
    return render_template('verficationsuccess.html', first_name=first_name, last_name=last_name,phone_number=phone_number, dob=dob, face_confidence=face_confidence)

@app.route('/verificationfail')
def verificationfail():
    Message = request.args.get('Message')
    print(Message)
    return render_template('verificationfail.html', Message=Message)

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/process_color_image', methods=['POST'])
def process_color_image():
    color_image_data = request.form['colorImageData']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    dob = request.form['dob']
    phoneNumber = request.form['phoneNumber']
    color_image_bytes = base64.b64decode(color_image_data)
    pic_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    filename = 'webcaptures/'+pic_filename+'.png' 
    with open(filename, 'wb') as f:
        f.write(color_image_bytes)

    ## Register Face -- First task
    url = "https://e26ljwj7ah.execute-api.us-west-2.amazonaws.com/v1/register"
    image = Image.open(filename)
    stream = io.BytesIO()
    image.save(stream,format="PNG")
    image_binary = stream.getvalue()
    headers = {
            'Content-Type': 'application/png',
            'x-api-key': 'GTUn6Fepnr8WWnLxYAT1c88HfWiRK7aN48qNyf0h'
        }
    response = requests.request("POST", url, headers=headers, data=image_binary)
    print(response.text)
    responsedictionary = json.loads(response.text)
    if responsedictionary['statusCode'] == 200:
        print("Face file uploaded successfully..")
        recordurl = "https://e26ljwj7ah.execute-api.us-west-2.amazonaws.com/v1/createfaceindex"
        recordpayload = json.dumps({
        "firstName": firstName,
        "lastName": lastName,
        "dob": dob,
        "phoneNumber": phoneNumber,
        "bucket": "uploadfiles-to-s3-bucket",
        "key": responsedictionary['keyname']
        })
        recordheaders = {
        'Content-Type': 'application/json',
        'x-api-key': 'GTUn6Fepnr8WWnLxYAT1c88HfWiRK7aN48qNyf0h'
        }
        recordresponse = requests.request("POST", recordurl, headers=recordheaders, data=recordpayload)
        print(recordresponse.text)
        recordresponsedictionary = json.loads(recordresponse.text)
        if recordresponsedictionary['statusCode'] == 200:
            print("Face index created successfully..")
            return jsonify({"success": True})
        else:
            print("Face index cretion failed..")
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})
    
@app.route('/verify_process_color_image', methods=['POST'])
def verify_process_color_image():
    color_image_data = request.form['colorImageData']
    color_image_bytes = base64.b64decode(color_image_data)
    pic_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    filename = 'webcaptures/'+pic_filename+'.png'  # Save in the 'static' folder
    with open(filename, 'wb') as f:
        f.write(color_image_bytes)
    url = "https://e26ljwj7ah.execute-api.us-west-2.amazonaws.com/v1/verifyfaceid"
    image = Image.open(filename)
    stream = io.BytesIO()
    image.save(stream,format="PNG")
    image_binary = stream.getvalue()
    headers = {
    'Content-Type': 'application/png',
    'x-api-key': 'GTUn6Fepnr8WWnLxYAT1c88HfWiRK7aN48qNyf0h'
    }
    response = requests.request("POST", url, headers=headers, data=image_binary)
    print(response.text)
    try:
        responsedictionary = json.loads(response.text)
        if responsedictionary['statusCode'] == 200:
            return jsonify(responsedictionary)
        else:
            return jsonify(responsedictionary)
    except Exception as e:
        print("Error in processing face verification {}".format(e))
        return jsonify({"success": False})
if __name__ == '__main__':
    app.run(debug=True)
    
