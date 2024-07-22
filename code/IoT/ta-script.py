import time
from datetime import datetime, time as dt_time
import pytz
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from DFRobot_PH import DFRobot_PH
import adafruit_shtc3
import subprocess
import RPi.GPIO as GPIO
import BlynkLib
from BlynkTimer import BlynkTimer
from PIL import Image
import os
import numpy as np
import tflite_runtime.interpreter as tflite

VREF = 5  # analog reference voltage(Volt) dari ADC
ADCRange = 65536.0 # 1024 for 10 bit; 4096 for 12bit ADC; 2^bit
wib_timezone = pytz.timezone('Asia/Jakarta') # zona waktu WIB
disease_prediction = []
output_disease_prediction = ''

# threshold ph and ppm nutrition hidroponik
lower_threshold_ph = 6.0
upper_threshold_ph = 7.0
lower_threshold_ppm = 1000.0

# inisialisasi blynk
BLYNK_AUTH_TOKEN = "fD3QZRpj7Z2oJSpCdBWrRb19wHkIoqpy"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# membuat instance blynktimer
timer = BlynkTimer()

# membuat I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# membuat ADC object menggunakan I2C bus
ads = ADS.ADS1115(i2c)

# mendefinisikan channel untuk ph dan tds
channelPH = AnalogIn(ads, ADS.P0)
channelTDS = AnalogIn(ads, ADS.P1)

# setup SHTC3
shtc3 = adafruit_shtc3.SHTC3(i2c)

# setup ph
ph = DFRobot_PH()
ph.begin()

# mengatur mode GPIO untuk definisi pin relay
GPIO.setmode(GPIO.BCM)   
# mendefinisikan channel atau pin relay
ph_relay_pin = 17 # pin 11 (GPIO 17)
nutritionA_relay_pin = 27 # pin 13 (GPIO 27)
nutritionB_relay_pin = 22 # pin 15 (GPIO 22)
rawWater_relay_pin = 23 # pin 16 (GPIO 23)
# mengatur pin sebagai output
GPIO.setup(ph_relay_pin, GPIO.OUT)
GPIO.setup(nutritionA_relay_pin, GPIO.OUT)
GPIO.setup(nutritionB_relay_pin, GPIO.OUT)
GPIO.setup(rawWater_relay_pin, GPIO.OUT)

# fungsi untuk menghidupkan relay, relay modul merupakan aktif LOW
def turn_on_relay(pin):
    GPIO.output(pin, GPIO.LOW)

# fungsi untuk mematikan relay
def turn_off_relay(pin):
    GPIO.output(pin, GPIO.HIGH)

# menonaktifkan semua relay
turn_off_relay(ph_relay_pin)
turn_off_relay(nutritionA_relay_pin)
turn_off_relay(nutritionB_relay_pin)
turn_off_relay(rawWater_relay_pin)


# mendefinisikan label kelas
class_labels = ['Karat Putih', 'Kekurangan Mangan', 'Sehat', 'Virus Keriting']

# memuat model TFLite
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# mendapatkan informasi input dan output dari model
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# menghubungkan ke blynk
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    print(".......................................................")
    time.sleep(2)

# fungsi untuk menjalankan kamera
def camera():
    command = "rpicam-still -n --width 2500 --height 2500 -o ~/Desktop/TA/output.jpg >/dev/null 2>&1" 
    result = subprocess.run(command, shell=True, check=True)    # menjalankan perintah melalui command line
    print("Foto berhasil diambil")
    time.sleep(2)

# fungsi untuk memotong gambar
def crop_image():
    # memotong gambar sesuai area hidroponik
    image = Image.open("/home/rasp/Desktop/TA/output.jpg")  # membuka gambar
    crop_area = (290, 470, 1970, 2075)  # mendefinisikan area yang dipotong berdasarkan koordinat (left, upper, right, lower)
    cropped_image = image.crop(crop_area)   # memotong gambar
    cropped_image.save("/home/rasp/Desktop/TA/output-result.jpg")  # menyimpan hasil gambar yang telah dipotong
    
    # Load the image
    image_path = "/home/rasp/Desktop/TA/output-result.jpg" 
    img = Image.open(image_path)
    img_width, img_height = img.size    # mendapatkan dimensi gambar
    # menghitung ukuran setiap tile
    tile_width = img_width // 6
    tile_height = img_height // 5
    # membuat direktori untuk menyimpan semua tile
    output_dir = "tiles"
    os.makedirs(output_dir, exist_ok=True)
    # memotong gambar menjadi 5x6 dan menyimpannya
    tile_number = 0
    tiles = []
    for i in range(5):
        for j in range(6):
            left = j * tile_width
            upper = i * tile_height
            right = (j + 1) * tile_width
            lower = (i + 1) * tile_height
            tile = img.crop((left, upper, right, lower))
            tile_path = os.path.join(output_dir, f"tile_{tile_number}.jpg")
            tile.save(tile_path)
            tiles.append(tile_path)
            tile_number += 1
    
    return tiles

# fungsi untuk memprediksi penyakit bayam
def predict_image_class(img_path):
    # memuat dan memproses gambar menggunakan PIL
    img = Image.open(img_path)
    img = img.resize((320, 320))
    x = np.array(img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # Skala gambar

    # menyiapkan input data untuk interpreter TFLite
    interpreter.set_tensor(input_details[0]['index'], x)

    # melakukan inferensi
    interpreter.invoke()

    # mendapatkan hasil prediksi
    predictions = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(predictions, axis=1)
    predicted_label = class_labels[predicted_class[0]]

    # menampilkan hasil prediksi
    print(f'Predicted Label: {predicted_label}')
    print(f'Prediction Confidence: {predictions[0][predicted_class[0]]:.2f}')
    print(f'All Predictions: {predictions}') 

    return predicted_label


# fungsi utama
def myData():
    global disease_prediction, output_disease_prediction
    
    try:
        # mendapatkan nilai suhu dan kelembaban dari sensor
        temperature, relative_humidity = shtc3.measurements

        # mendapatkan nilai ph dari sensor
        phResultWithVoltage = ph.read_PH(int(channelPH.voltage*1000), temperature)
        
        # mendapatkan nilai ppm dari sensor
        averageVoltage = channelTDS.value * VREF / ADCRange # mendapatkan rata2 voltage
        compensationCoefficient = 1.0 + 0.02 * (19 - 25.0)  # rumus untuk mendapatkan koefisien kompensasi
        compensationVolatge = averageVoltage / compensationCoefficient  # voltage kompensasi
        tdsValue = (133.42 * compensationVolatge**3 - 255.86 * compensationVolatge**2 + 857.39 * compensationVolatge) * 0.5  # ubah nilai ke dalam nilai nutrisi atau tds
        tdsValue = tdsValue*2
        
        # mendapatkan waktu sekarang
        current_time = datetime.now(wib_timezone) # mendapatkan waktu saat ini dalam wib
        current_time_str = current_time.strftime('%H:%M:%S') # mendapatkan jam, menit, dan detik sekarang
        print(f'Jam sekarang: {current_time_str}')
        
        current_time_obj = datetime.strptime(current_time_str, '%H:%M:%S').time()   # mendapatkan objek time dari string waktu
        
        # rentang waktu yang menjalankan kamera dan prediksi penyakit
        start_time_morning = dt_time(8, 0, 0)  # jam 09:00:00
        end_time_morning = dt_time(8, 0, 5)    # jam 09:00:05
        start_time_evening = dt_time(17, 0, 0) # jam 17:00:00
        end_time_evening = dt_time(17, 0, 5)   # jam 17:00:05
        
        # menjalankan kamera dan mendeteksi penyakit setiap jam 08:00:00-08:00:05 pagi dan 17:00:00-17:00:05 sore
        if start_time_morning <= current_time_obj <= end_time_morning or start_time_evening <= current_time_obj <= end_time_evening:
            disease_prediction = [] # reset isi list setiap akan memprediksi penyakit
            camera()    # memotret bayam
            tiles = crop_image() # crop gambar dan menjadi 30 gambar (sesuai jumlah lubang)
            # memprediksi bayam keseluruhan
            #disease_prediction = predict_image_class('/home/rasp/Desktop/TA/output-result.jpg')
            # loop masing-masing tile dan memprediksi penyakit bayam
            for tile_path in tiles:
                 print(f'Processing file: {tile_path}')
                 pred = predict_image_class(tile_path)
                 disease_prediction.append(pred)
                 
            # Membuat kamus untuk mengelompokkan indeks berdasarkan penyakit
            grouped_indices = {
                'KP': [],
                'KM': [],
                'S': [],
                'VK': []
            }

            # Mendefinisikan mapping penyakit ke kelompok
            disease_to_group = {
                'Karat Putih': 'KP',
                'Kekurangan Mangan': 'KM',
                'Sehat': 'S',
                'Virus Keriting': 'VK'
            }

            # Mengelompokkan indeks berdasarkan penyakit
            for index, disease in enumerate(disease_prediction):
                group = disease_to_group[disease]
                grouped_indices[group].append(index+1)

            # Membuat output string
            output_disease_prediction = ' | '.join([f"{group}: {','.join(map(str, indices))}" for group, indices in grouped_indices.items()])

            print(output_disease_prediction)

        # daftar nilai
        current_temperature = temperature
        current_humidity = relative_humidity
        current_ph = phResultWithVoltage
        current_ppm = tdsValue
        disease = "Sehat" if not output_disease_prediction else output_disease_prediction
        
        #current_ph = float(input("masukkan nilai ph: "))
        #current_ppm = float(input("masukkan nilai nutrisi: "))

        
        # mencetak nilai di console
        print(f"temperature: {current_temperature:.2f}, humidity: {current_humidity:.2f}, ph: {current_ph:.2f}, ppm: {current_ppm:.2f}, disease: {disease}")
        #print(f"disease prediction: {disease_prediction}")
        # mengirim nilai ke blynk
        blynk.virtual_write(0, current_humidity,)
        blynk.virtual_write(1, current_temperature)
        blynk.virtual_write(2, current_ph)
        blynk.virtual_write(3, current_ppm)
        blynk.virtual_write(4, disease)
        print("Values sent to New Blynk Server!")
        

        # pengaturan nutrisi dan ph
        # jika ph kurang dari threshold, maka menghidupkan pompa air selama 3 detika
        if current_ph < lower_threshold_ph:
            print('relay air aktif untuk menghidupkan pompa air')
            turn_on_relay(rawWater_relay_pin)
            time.sleep(3) # hidup selama 3 detik
            turn_off_relay(rawWater_relay_pin)
            time.sleep(25)

        # jika ph lebih dari threshold, maka menghidupkan pompa ph down selama 3 detik
        if current_ph > upper_threshold_ph:
            print('relay ph aktif untuk menghidupkan pompa ph')
            turn_on_relay(ph_relay_pin)
            time.sleep(1) # hidup selama 1 detik
            turn_off_relay(ph_relay_pin)
            time.sleep(25)
        
        # jika ppm kurang dari threshold, maka menghidupkan pompa nutrisi a dan b selama 3 detik
        if current_ppm < lower_threshold_ppm:
            print('relay nutrisi a dan b aktif untuk menghidupkan pompa a dan b')
            turn_on_relay(nutritionA_relay_pin)
            turn_on_relay(nutritionB_relay_pin)
            time.sleep(2) # hidup selama 2 detik
            turn_off_relay(nutritionA_relay_pin)
            turn_off_relay(nutritionB_relay_pin)
            time.sleep(25)

        print("======================================")
        
    except RuntimeError as error:
        time.sleep(2.0)
        #continue
    except Exception as error:
        raise error
    except KeyboardInterrupt:
        GPIO.cleanup()  # membersihkan konfigurasi GPIO saat program dihentikan
    
    time.sleep(5)   # jeda selama 5 detiks
    
timer.set_interval(2, myData)

while True:
    blynk.run()
    timer.run()