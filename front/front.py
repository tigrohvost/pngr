#sudo setcap cap_net_raw+ep $(which python3.12)
from flask import Flask, jsonify, render_template, request
#from pythonping import ping
import requests

# https://stackoverflow.com/questions/71976607/how-to-run-two-flask-servers-on-different-ports-at-the-same-time-using-bash-scri

front = Flask(__name__)

""" 
def pinger(ip_address = '8.8.8.8'):
  # The IP, Timeout Seconds
  result = ping(ip_address, count=1)
  print('packets lost :', str(result.packets_lost))
  if result.success(option=3):
      #print('success')
      rounded_time = round(result.rtt_avg_ms / 10 / 100, 3) # print average time in seconds
      res_str = 'ping ' + ip_address + '... ' + str(rounded_time)
      return res_str
  else:
      return 'failed'
 """
def caller(ip_address = '8.8.8.8'):
    #import requests
    url = 'http://back:5001/pinger'
    #url = 'https://httpbin.org/post'
    # POST/form data
    payload = {
        'address': ip_address,
    }
    #r = requests.post(url, data=payload, headers = {"Content-Type": "application/json"}, timeout=1.0)
    r = requests.post(url, json=payload)
    print(r.text)
    return r.text

@front.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        ip_address = request.form['ip_address']
        output = caller(ip_address)
        if ip_address:
            return jsonify({'output':output + 'ms'})
        return jsonify({'error' : 'Missing data!'})
    return render_template('index.html')

if __name__ == '__main__':
    #front.run(debug=True)
    front.run(host='0.0.0.0')
