from flask import Flask
import random
import time

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    timestamp = str(int(time.time()))
    response = {
        "time":  timestamp,
        "message": "success",
        "httpsresponse": "200",
        "testedTIME": "yes"
    }
    return response

## Add a new route here
@app.route('/random')
def get_random_numbers():
    numbers = [random.randint(0, 5) for _ in range(10)]
    response = {
        "random_number": numbers,
        "message": "success",
        "httpsresponse": "200",
        "testedTIME": "yes"
    }
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)