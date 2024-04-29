# curl -H "Content-Type: application/json" -X POST -d '{"address": "ya.ru"}' http://localhost:5000/pinger

from flask import Flask, request, jsonify
from pythonping import ping

back = Flask(__name__)

def pinger(ip_address = '8.8.8.8'):
  # The IP, Timeout Seconds
  result = ping(ip_address, count=1)
  print('packets lost :', str(result.packets_lost))
  if result.success(option=3):
      #print('success')
      rounded_time = round(result.rtt_avg_ms / 10 / 100, 3) # print average time in seconds
      #res_str = 'ping ' + ip_address + '... ' + str(rounded_time)
      return str(rounded_time)
  else:
      return 'failed'

@back.route('/pinger', methods=['POST']) 
def foo():
    data = request.json
    #res = jsonify(data)
    #return res.get_data(as_text=True)
    ip_address = (data['address'])
    res = pinger(ip_address)
    #print(res)
    return res

if __name__ == '__main__':
    back.run(debug=True)