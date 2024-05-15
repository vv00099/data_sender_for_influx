import telnetlib
import time
import json

#Данные для подключения
station_data = {}

#Загружаем логин пароль и ip станции
with open("connect_data.json",encoding='utf-8') as file1:
    station_data = json.load(file1)
		
telnet = telnetlib.Telnet(station_data.get('ip'))

result = ""
#Попытка авторизоваться пока не получим приглашение
#После 3х неудачных попыток станция сама разорвет соединение
while "Huawei Integrated Access Software" not in str(result):
    result = telnet.read_very_eager().decode('ascii')
    time.sleep(2)
    if "User name:" in str(result):
        telnet.write(station_data.get('login').encode('ascii'))
        telnet.write(b"\n")
        time.sleep(3)
        telnet.write(station_data.get('password').encode('ascii'))
        telnet.write(b"\n")
        time.sleep(3)

telnet.write("enable".encode('ascii') + b"\n")
time.sleep(2)
telnet.write("config".encode('ascii') + b"\n")
time.sleep(2)
telnet.write("interface gpon 0/0".encode('ascii') + b"\n")
time.sleep(2)
#16 потому что 16 портов на плате станции
for i in range(16):
    print("display ont optical-info " + str(i))
    telnet.write(f"display ont optical-info {i} all".encode('ascii') + b"\n")
    #Ждать 25с нужно потому что сигналы опрашиваются с задержкой
    time.sleep(25)
    #Если onu'шек больше чем 30 то нужно будет подтвердить дальнейший опрос
    telnet.write(" ".encode('ascii') + b"\n")
    time.sleep(25)
    telnet.write(" ".encode('ascii') + b"\n")
    time.sleep(25)
    telnet.write(" ".encode('ascii') + b"\n")
    time.sleep(25)
    telnet.write(" ".encode('ascii') + b"\n")
    time.sleep(25)
all_result = telnet.read_very_eager().decode('ascii')

with open("./txt/station0"+ time.strftime('_%d_%m') + ".txt", "a+") as f_result:
    f_result.write(all_result)
print('done!')
telnet.close()