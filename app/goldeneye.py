from flask import Flask
from flask import render_template
from werkzeug.contrib.cache import SimpleCache

from app import get_final_list

app = Flask(__name__)

cache = SimpleCache(threshold=1000000)

lb_metadata = {
  'AMS1': {'name': 'AMS1', 'city': 'Amsterdam', 'ip': '10.10.1.11', 'type': 'A10'},
  'FRA1': {'name': 'FRA1', 'city': 'Frankfurt', 'ip': '10.20.1.11', 'type': 'A10'},
  'HKG1': {'name': 'HKG1', 'city': 'Hong Kong', 'ip': '10.30.1.11', 'type': 'A10'},
  'IAD1': {'name': 'IAD1', 'city': 'Ashburn', 'ip': '10.40.1.11', 'type': 'NetScaler'},
  'LAS1': {'name': 'LAS1', 'city': 'Las Vegas', 'ip': '10.50.1.11', 'type': 'NetScaler'},
  'LAX1': {'name': 'LAX1', 'city': 'Los Angeles', 'ip': '10.70.1.11', 'type': 'NetScaler'},
  'NRT1': {'name': 'NRT1', 'city': 'Tokyo', 'ip': '10.80.1.11', 'type': 'NetScaler'},
  'SJC1': {'name': 'SJC1', 'city': 'San Jose', 'ip': '10.90.1.11', 'type': 'A10'}
}


@app.route("/")
def hello():
  return render_template('index.html',
                         lb_metadata = lb_metadata)

@app.route('/datacenter/<dc>')
def datacenter(dc):
  lb_ipaddress = lb_metadata[dc.upper()]['ip']
  type = lb_metadata[dc.upper()]['type']
  #try:
  #  lb_info = cache.get(str(dc))
  #  if lb_info == None:
  #    lb_info = get_final_list(dc)
  #    cache.set(str(dc), lb_info, timeout = 5 * 60)
  #
  #except:
  #  lb_info = {}

  lb_info = get_final_list(dc)

  return render_template('datacenter.html',
                         dc = dc,
                         lb_info = lb_info,
                         lb_ipaddress = lb_ipaddress,
                         lb_metadata = lb_metadata)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
