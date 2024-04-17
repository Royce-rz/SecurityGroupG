from flask import Flask, request
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from urllib.parse import parse_qs
import re
import csv
import ssl
import base64

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

# AES KEY and AES IV for decryption
AES_KEY = b'securitygroupg12'  # 16 bytes KEY
AES_IV = b'securitygroupg12'  # 16 bytes IV

def decrypt_aes(data): # apply AES method with essential unpadding mode
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decryption = cipher.decrypt(data)
    decrypted = unpad(decryption, AES.block_size)
    return decrypted

@app.route('/data', methods=['POST'])
def receive_data():
    # decode and decrypt process
    encoded_data = request.data
    decrypted_data = base64.b64decode(encoded_data) # decode at first
    decoded_data = decrypt_aes(decrypted_data)  # decrypt at second
    decoded_data = decoded_data.decode('utf-8')  # transfer the data as string
    
    device_id = request.form.get('device_id', 'unknown_device')
    print(device_id)

    parsed_data = parse_qs(decoded_data)
    device_id = parsed_data.get('device_id')[0]  # search for deviceid paragraph
    sensor_data = parsed_data.get('data')[0]  # search for data paragraph
    # create the local database
    csv_file_path = f"{device_id}_security_encryted_data.csv"
    # using regular expression to rename the data chain
    pattern = r'(\d+):(-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+,-?\d+\.\d+)'
    sensor_readings = re.findall(pattern, sensor_data)
    print("sensor_readings003")
    print(sensor_readings)
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        for reading in sensor_readings:
            channel = reading[0]
            values_str = reading[1]
            values = values_str.split(',')
            # record the data and time information
            writer.writerow([datetime.now(), channel] + values)
            
    return 'Data received successfully'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain('mydomain.crt', 'mydomain.key') 
    app.run(debug=True, host='0.0.0.0', port=80)
