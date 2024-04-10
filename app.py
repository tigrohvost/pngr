# pip install pythonping
# fix operation not permitted error: icmp wants root)):
# sudo setcap cap_net_raw+ep $(readlink -f $(which python))
import re
from datetime import datetime
from flask import Flask
from flask import render_template, request
from pythonping import ping

app = Flask(__name__)

@app.route("/")
def index():
  return '=^_^='

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

#################################################################################################
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        
        data = form_data.to_dict()
        ip_address = data['Ip']
        print(ip_address)
        print('-----------------------')
        result = pinger(ip_address)
        print(result)

        return render_template('data.html',result = result)

#################################################################################################
@app.route("/ping/")
@app.route("/ping/<ip_address>")
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

if __name__ == '__main__':
  app.run()