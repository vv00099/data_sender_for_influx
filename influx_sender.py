import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import json

bucket = "station0"

org = "company"
token = "22yecbwm............"

url="http://192.168.1.100:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

ports = {}

export_data = {'0/0' : [],
              '0/1' : [],
              '0/2' : [],
              '0/3' : [],
              '0/4' : [],
              '0/5' : [],
              '0/6' : [],
              '0/7' : [],
              '0/8' : [],
              '0/9' : [],
              '0/10' : [],
              '0/11' : [],
              '0/12' : [],
              '0/13' : [],
              '0/14' : [],
              '0/15' : []}

with open('./json/export_data' + time.strftime('_%d_%m') + '.json', 'r') as f:
	ports = json.load(f)

def send(list1):
    for key,value in list1.items():
        if value[0] >= 1:
            p0 = influxdb_client.Point("Опрос станции0 21.00").tag("PORT " + key, "ONLINE").field("Кол-во", value[0])
            write_api.write(bucket=bucket, org=org, record=p0)
            time.sleep(5)

            p1 = influxdb_client.Point("Опрос станции0 21.00").tag("PORT " + key, "Слабый сигнал < -27,2").field("Кол-во", value[1])
            write_api.write(bucket=bucket, org=org, record=p1)
            time.sleep(5)

            p2 = influxdb_client.Point("Опрос станции0 21.00").tag("PORT " + key, "Очень cлабый сигнал < -30").field("Кол-во", value[2])
            write_api.write(bucket=bucket, org=org, record=p2)
            time.sleep(5)

            p3 = influxdb_client.Point("Опрос станции0 в 21.00").tag("PORT " + key, "Средний сигнал").field("- db", value[3])
            write_api.write(bucket=bucket, org=org, record=p3)
            time.sleep(5)

            print(key)
        else:
            continue
    
def data_processing():
    for key,value in ports.items():
        export_data[key].append(int(len(value)))
        weak_signal = 0
        very_weak_signal = 0
        total = 0
        for i in value:
            total += i
            if i >= 30:
                very_weak_signal += 1
                continue
            if i >= 27.2:
                weak_signal += 1
            
        
        export_data[key].append(weak_signal)
        export_data[key].append(very_weak_signal)
        try:
            export_data[key].append(round(total / len(value), 2))
        except ZeroDivisionError:
            export_data[key].append(0)
data_processing()
send(export_data)
#print(export_data)
