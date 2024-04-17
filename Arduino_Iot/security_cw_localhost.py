from flask import Flask, request
from datetime import datetime
import re
import csv
import ssl

app = Flask(__name__)

# maximum data packet limite
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/data', methods=['POST'])
def receive_data():
    device_id = request.form.get('device_id', 'unknown_device')  # get 'device id'
    batch_data = request.form['data']  # get 'data' and sensor readings
    # create the local database
    csv_file_path = f"{device_id}_security_testing_data.csv"
    # using regular expression to rename the data chain
    pattern = r'(\d+):(-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+)'
    sensor_readings = re.findall(pattern, batch_data)
    print("sensor_readings003")
    print(sensor_readings) # read data in terminal to check
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        for reading in sensor_readings:
            channel = reading[0]
            values_str = reading[1]
            values = values_str.split(',')
            # record the data and time information
            writer.writerow([datetime.now(), channel] + values)
    return 'Data received'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain('mydomain.crt', 'mydomain.key') 
    app.run(debug=True, host='0.0.0.0', port=443)



