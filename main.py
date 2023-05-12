import os
import json
import time
import wifi
import requests
from datetime import datetime, timedelta

DS18B20 = '28-3c51f6497131'  # Reemplazar con el ID del sensor
data_list = []

while True:
    # Leer la temperatura del sensor
    temp = float(os.popen(f"cat /sys/bus/w1/devices/{DS18B20}/w1_slave | awk 'NR==2{print $10}'").read()) / 1000

    # Obtener la hora y fecha actual
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    current_date = time.strftime("%Y-%m-%d")

    # Guardar los datos en un archivo JSON
    data = {"temperatura": temp, "hora": current_time}
    data_list.append(data)

    # Crear o abrir archivo con la fecha actual como nombre
    with open(f"temp_data_{current_date}.json", "a") as outfile:
        json.dump(data, outfile)

    # Esperar 5 minutos antes de volver a leer la temperatura
    time.sleep(10)

    # Conectarse a wifi
    wifi.connect()

    if wifi.is_connected():
        # Recorrer lista de datos y enviar cada objeto en formato JSON
        for item in data_list:
            requests.post('https://yourserver.com/post', json=item)

        #Esperar confirmacion
        response = requests.get('https://yourserver.com/confirm')
        if response.status_code == 200:
            print('Datos enviados correctamente')
            data_list = []
        else:
            print('Error al enviar los datos')
    #Administrar archivos antiguos
    now = datetime.now()
    for f in os.listdir():
        if f.endswith('.json'):
            file_date = datetime.strptime(f[11:21], '%Y-%m-%d')
            if (now - file_date) > timedelta(days=30):
                os.remove(f)
                print(f'{f} eliminado')
