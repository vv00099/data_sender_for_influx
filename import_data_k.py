import time
import json
import re

current_file = "./txt/station0"+ time.strftime('_%d_%m') + ".txt"
reading = False
last_port = ''
ports = {'0/0' : [],
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


file1 = open(current_file, "r")

# считываем все строки
lines = file1.readlines()

# итерация по строкам
for line in lines:
    if 'display ont' in line:
        last_port = re.findall(r"\d+", line)
        print(last_port[2])
    if (line[3:5]).isnumeric:
        reading = True
    if reading and '( Press' in line:
        try:
            #print(float(line[92:97]))
            ports["0/" + str(last_port[2])].append(float(line[92:97]))
        except ValueError:
            pass
        continue
    if reading and '  ----------------------------------------------' in line:
        reading = False
    if reading and '.' in line:
        try:
            #print(float(line[8:13]))
            ports["0/" + str(last_port[2])].append(float(line[8:13]))
            pass
        except ValueError:
            pass

file1.close

for key,value in ports.items():
    print(key, value)

with open('./json/export_data' + time.strftime('_%d_%m') + '.json', 'w') as f:
	json.dump(ports, f, indent=4)