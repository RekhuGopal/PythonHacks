from flask import Flask, render_template, request
import random
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/', methods=['GET', 'POST'])
def index():
    color = "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    
    if request.method == 'POST':
        redis.incr('clicks')
        
    clicks = redis.get('clicks')
    
    if clicks is None:
        clicks = 0
    else:
        clicks = int(clicks.decode())
       
    return render_template('index.html', color=color, clicks=clicks)
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
