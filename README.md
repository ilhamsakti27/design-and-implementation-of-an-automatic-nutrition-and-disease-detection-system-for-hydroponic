# Automation of Nutrition and Disease Detection in Hydroponic Spinach

## Introduction

### I. Project Name
DESIGN AND IMPLEMENTATION OF AN AUTOMATIC NUTRITION AND DISEASE DETECTION SYSTEM FOR HYDROPONIC SPINACH PLANTS USING RASPBERRY PI

### II. Description
In addressing the challenge of meeting food requirements triggered by the increasing human population and decreasing agricultural land, hydroponic farming emerges as a solution for cultivating in limited spaces. Spinach, a plant with high economic value and widely favored by the community, can be grown using hydroponics, though it is susceptible to diseases. Proper management of the nutrient solution according to the plants' needs is a crucial factor in the success of hydroponic farming. With the application of IoT, managing nutrients and detecting diseases in hydroponic spinach becomes more efficient than doing so manually, which requires time, effort, and specialized skills. This research aims to develop an automation system for managing nutrients and detecting diseases in hydroponic spinach using the Nutrient Film Technique (NFT), utilizing a Raspberry Pi as the control center. The system monitors pH, nutrient content, temperature, humidity, and detects plant diseases using a Convolutional Neural Network (CNN) with a transfer learning architecture based on the MobileNetV2 model integrated with the Blynk dashboard. According to test results, the temperature and humidity sensors, pH sensors, and nutrient sensors have an accuracy above 97%, and the MobileNetV2 model used has an accuracy of 57% in detecting diseases in hydroponic spinach through images captured by a camera.  
**Keywords: *CNN, hydroponic, IoT, smart farming, spinach***

### III. Project Objectives
1. Designing a nutrient delivery automation system in hydroponic spinach farming NFT method by optimizing nutrient and water delivery to ensure plants get their needs quickly and precisely.  
2. Developing a disease detection mechanism for hydroponic spinach plants using deep learning methods, enabling early prevention and treatment.  
3. Integrating the automation system of nutrient delivery and disease detection of hydroponic spinach plants to improve the effectiveness and efficiency of hydroponic plant management.  

### IV. Project Team
Ilham Muhammad Sakti

### V. Project Start & End Dates
March 2024 - July 2024


## Methodology

### I. Tools & Materials

#### Hardware
| Item | Description |
| ---- | ----- |
| Raspberry Pi 4B | As a microcomputer. Used to manage automatic nutrient delivery and deployed plant disease detection model. |
| 32GB MicroSD | As a medium for storing the Raspberry Pi operating system. |
| ADC Module 1115 | To convert analog signals to digital signals.
| TDS DFRobot Sensor (SEN0244 Gravity Analog TDS Meter) | Sensor to read nutrient concentration (ppm) in hydroponic nutrient solution. | 
| PH DFRobot Sensor (SEN0161 Gravity Analog pH Sensor Meter Kit V2) | Sensor to read the pH content of the hydroponic nutrient solution. |
| Temperature and Humidity Sensor (SHTC3) | Sensor to read the temperatur and humidity of the hydroponic area installation. |
| Pi Camera Module 3 12MP | Used to take pictures of hydroponic plants with the the purpose of detecting diseases in these plants. |
| Micro Water Pump R385 | Serves to flow nutrient solutions to plants and mix the nutrient solution by flowing pH down, nutrients a, nutrient b, and water to the nutrient solution reservoir. |
| Relay Module 12V | Used to control the pumps (water, pH down, nutrient a, and nutrient b) as needed. |
| Power Supply 12V | Used to supply the electric power of the pump (water, pH down, nutrient a, and nutrient b). | 

#### Software
| Item | Description | 
| ---- | ----------- | 
| Raspberry Pi Imager (app) | Application for installing the Raspberry Pi operating system |
| TensorFlow Lite (TFLite) | An open-source framework that enables running machine learning (ML) models trained with Tensorflow on mobile and embedded devices. |
| Blynk (web dashboard) | To display predictions of plant disease classification, temperature & humidity values, and pH & ppm content of nutrient solutions. |
| BlynkLib (library) | To send data from Raspberry Pi to Blynk. |
| adafruit-circuitpython-ads1x15 (packages) [version 2.2.25] | Driver for Adafruit's ADS1x15 ADC (Analog-to-Digital Converters) used with CircuitPython. |
| adafruit-circuitpython-shtc3 (packages) [version 1.1.14] | Driver for the SHTC3 temperature and humidity sensor from Adafruit used with CircuitPython. |
| RPi.GPIO (packages) [version 0.7.1] | Library to control GPIO (General Purpose Input/Output) pins on Raspberry Pi. |
| tflite-runtime (packages) [version 2.14.0] | A runtime for running TensorFlow Lite models on devices with limited resources, such as microprocessors or edge devices. |
| image (packages) [version 1.5.33] | Library for manipulating and processing images. |
| pillow (packages) [version 10.3.0] | An image processing library that is the successor to PIL (Python Imaging Library).
| numpy (packages) [version 1.26.4] | Library for scientific computing in Python, providing support for multidimensional arrays and various high-level math functions. |
| pytz (packages) [version 2024.1] | A library for handling time zones in Python, making it easy to convert between different time zones. |

### II. System Architecture
![System Architecture](./images/System%20Architecture.png)  
The design of the system that will be developed in this research aims to be able to monitor and provide nutrients and pH automatically to conduct early detection of diseases in hydroponic spinach plants. The main idea of the system is to interface several sensors with Raspberry Pi and forward the data (pH, PPM, and temperature) obtained from the sensors to Blynk. The data obtained is displayed on the Blyk dashboard through the website and Blynk application. While in detecting the disease using MobileNetV2. The dataset used in this research is obtained from the internet on the website https://universe.roboflow.com/.

This research uses the Nutrient Film Technique (NFT) technique in growing spinach hydroponically which is very suitable for vegetable cultivation. The advantage of this method lies in the ability to supply oxygen that is more quickly absorbed by the roots, thanks to the continuous and rapid water circulation process. This allows the plant to absorb nutrients more and more easily resulting in better plant growth. There are two types of pumps used, the mini pump and the main pump. The main pump is used to drain the nutrient solution from the reservoir to the hydroponic spinach plants and the micro pump is used to add liquids, such as A/B mix nutrients, pure water and pH down to the reservoir according to the nutritional needs of the plants. 

### III. Schematics Diagram
![Schematics Diagram](./images/Schematics%20Diagram.png)  

### IV. Flowchart System
![System Flowchart](./images/System%20Flowchart.png)  
For the automatic nutrient delivery system, it starts with the Raspberry Pi reading the pH value, nutrient content (PPM), temperature and humidity through the pH sensor, TDS sensor, and TDS sensor. 15 SHTC3 SENSOR. Then the pH content is checked. The ideal pH value for hydroponic spinach plants is 6.0 to 7.0. The ideal pH value for hydroponic spinach plants is 6.0 to 7.0. If the pH is less than 6, the water pump water pump is turned on for 3 seconds to raise the pH of the nutrient solution. However, if the pH is more than 7, If the pH is more than 7, then the pH pump is turned on for 1 second to lower the pH. Next, the nutrient content is checked. checking the nutrient content. The ideal PPM value for hydroponic spinach plants is at least 900, but in this research I used a PPM value of 1000. If PPM is less than 1000, the Raspberry Pi will turn on the nutrient pumps A and B for 2 seconds to increase the nutrient content. increase the nutrient content.

### V. Flowchart Build Model
![Build Disease Classification Model Flowchart](./images/Build%20Disease%20Classification%20Model%20Flowchart.png)  
In the model building process, the first step is to load the dataset, then divide the dataset into three parts, namely train data, validation data, and test data. Augmentation is performed on train data by rotating, shifting images horizontally and vertically, and enlarging or reducing images. After that, data preprocessing is done by changing the size to 320x320 pixels. Build a CNN model using the sequential API from TensorFlow. The model consists of several layers of convolution, ReLU activation, pooling, flattening, dense, and dropout. After that, the model evaluation is carried out to calculate the accuracy, recall, precisiom, and F1-score values. Then save the model in tflite format and deploy the model to Raspberry Pi. For details of the model building process can be seen in the figure above. 

### VI. Usage
#### A. Connect the Raspberry Pi with the computer
**With Cable**  
1. Use a microHDMI to HDMI & Video Capture cable to connect the Raspberry Pi with a computer as shown below.   
    <img alt="connect raspberryPi to laptop" src="./images/connect%20raspberryPi%20to%20laptop.jpg" width="500" />  
2. Open the OBS Studio app.
3. Select the source and double-click "Video Capture Device".
4. Select the "USB Video" device and click "Activate" and click "OK".  
    <img alt="pop up property" src="./images/popUp OBS.png" width="500" />  
5. Use a mouse and keyboard to operate the Raspberry Pi.

**Remote**
1. To access the Raspberry Pi remotely, you can use XRDP.  
2. Update system packages & install XRDP.
    ```bash
    sudo apt update
    sudo apt upgrade
    sudo apt install xrdp
    ```
3. Check the IP address of Raspbery Pi.  
    ```bash
    hostname -I
    or
    ip -br a
    ```  
4. Open the Remote Desktop Connection application and enter the Raspberry Pi IP then click “Connect” and “Yes” on the pop up afterwards.  
    <img alt="Remote Desktop Connection" src="./images/conectRaspRemote.png" width="500" />  
5. Login Raspberry Pi.  
    <img alt="login raspberrypi" src="./images/loginRaspberrypi.png" width="500" />  
6. Raspberry Pi can be directly operated through a computer.  

#### B. Calibration PH sensor and TDS sensor
**PH Sensor**  
->**Raspberry Pi**
1. Connect the Raspberry Pi with the pH sensor through the ADC module according to the [Schematics Diagram](#iii-schematics-diagram).
2. Clean the sensor probe and insert it into the buffer solution (pH 4.0 or 7.0).
3. Run the following [program code](./code/IoT/ph_calibrate.py), then the sensor will automatically calibrate.
> Make sure the adafruit-circuitpython-ads1x15 and DFRobot_PH libraries are installed.  

->**Arduino Uno**
1. Connect the Arduino with the pH sensor and upload [the following code](./code/IoT/ph_calibrate.ino) to the board, after that put it into the buffer solution (pH 4.0 or 7.0).  
    <img alt="ph connection arduino" src="./images/SEN0161-V2_Connection.png" width="500" /> 
2. Run the code.
3. When the pH value is stable, enter the command `enterph` in the serial monitor to enter calibration mode.
4. Enter `calph` command in the serial monitor to start calibration. The program will automatically identify the buffer solution used. 
5. After calibration, enter the `exitph` command in the serial monitor to exit the calibration mode and save the calibration results.
6. Perform the previous steps on a different buffer solution from the previous step.
> Make sure the DFRobot_PH library is installed.

**TDS Sensor**  
->**Arduino Uno**
1. Connect the Arduino with the TDS sensor and upload [the following code](./code/IoT/tds_calibrate.ino).    
    <img alt="tds connection arduino" src="./images/SEN0244_Connection.png" width="500"/>
2. Clean the TDS probe then put it into the solution buffer and run the code.
3. After the ppm value is stable, enter the `enter` command in the serial monitor to enter the calibration mode.
4. Enter the command `cal:tds` to start calibration. The “tds” value is the ppm content read by the sensor in numeric form.
5. Enter the `exit` command to save the calibration results and exit the calibration mode. 
> Make sure the DFRobot Gravity TDS sensor library is installed. 

#### C. Connect the Camera with the Raspberry Pi
1. Connect the Raspberry Pi with the Pi Camera Module (ensure Raspberry Pi is turned off).  
    <img alt="connect camera to rasp" src="./images/connect-camera.gif" width="500"/>
2. Reboot Raspberry Pi.
3. Update system packages & update firmware and kernel.
    ```bash
    sudo apt update
    sudo apt upgrade
    sudo rpi-update
    ```
4. Make configuration changes to the `/boot/config.txt` or `/boot/firmware/config.txt` file by adding the following code, then reboot.
    ```bash
    # ubah start_x=1 menjadi
    camera_auto_detect=1
    
    # ubah gpu_mem=128 menjadi
    gpu_mem=256
    ```
5. Reboot Raspberry Pi.
6. Test the camera with the following command.
    ```bash
    libcamera-hello
    or
    rpicam-hello
    ```

#### D. Training Model
In this research, researcher used the [dataset bayam daun tunggal](./code/Dataset/dataset_bayam%20(daun%20tunggal).zip) to create a spinach disease classification model through the image captured by the camera. The training process was conducted at [Google Collaboratory](https://colab.research.google.com/).The following are the steps in training the model in this study.
1. Upload [the following code](./code/AI/Training%20Model.ipynb) and dataset in [Google Collaboratory](https://colab.research.google.com/).
2. Connect to a runtime.
3. Run all the code.
4. Once done, download the model in tflite format.

#### Blynk Dashboard
1. Login [Blynk](https://blynk.cloud/).  
2. Select menu "Developer Zone" -> "My Templates" -> click "New Template" to add a new template.
    <img alt="new template" src="./images/blynk_new template.png" width="500"/>
3. Fill pop up "Create New Template".  
    <img alt="create new template" src="./images/blynk_create new template.png" width="400"/>
4. Create data stream for each data obtained from the sensor.  
    <img alt="create datastream" src="./images/blynk_create datastream.png" width="400"/>
    |   Jenis Pin |              Name | Pin | Data Type |                 Units |  Min |  Max |
    | ----------- | ----------------- | --- | --------- | --------------------- | ---- | ---- |
    | Virtual Pin | Prediksi Penyakit |  V4 |    String |                     - |    - |    - |
    | Virtual Pin |    Sensor Nutrisi |  V3 |    Double | Parts Per Milion, ppm |    0 | 2000 |
    | Virtual Pin |         Sensor pH |  V2 |    Double |                  None |    0 |   14 |
    | Virtual Pin |        SHTC3_Suhu |  V1 |    Double |           Celcius, °C |  -40 |  125 |
    | Virtual Pin |  SHTC3_Kelembaban |  V0 |    Double |         Precentage, % |    0 |  100 |
5. Creating a web dashboard as an interface that allows to monitor plant conditions remotely through a web browser.
    <img alt="web dashboard" src="./images/blynk_create web dashboard.png"/>
    | Widget Box |             Title |             Datastream |
    | ---------- | ----------------- | ---------------------- |
    |      Label | Prediksi Penyakit | Prediksi Penyakit (V4) |
    |      Gauge |     Kadar Nutrisi |    Sensor Nutrisi (V3) |
    |      Gauge |                pH |         Sensor pH (V2) |
    |      Gauge |              Suhu |        SHTC3_Suhu (V1) |
    |      Gauge |        Kelembaban |  SHTC3_Kelembaban (V0) |
    |      Chart |         Kadar PPM |    Sensor Nutrisi (V3) |
    |      Chart |          Kadar pH |         Sensor pH (V2) |
    |      Chart |              Suhu |        SHTC3_Suhu (V1) |
    |      Chart |        Kelembaban |  SHTC3_Kelembaban (V0) |
6. Then click "Save And Play".
7. After that, add the device by clicking "New Device" -> "From template".  
    <img alt="add device blynk" src="./images/blynk_add device.png" width="500"/>  
    <img alt="add new device" src="./images/blynk_add new device.png" width="500"/>  
8. Select the "Raspberry Pi 4B" template and name it the same name.  
    <img alt="new device blynk" src="./images/blynk_new device.png" width="500"/>  
9. Finish.


#### F. Automation Nutrition and Disease Detection System
1. Connect the device according to the [schematics diagram](#iii-schematics-diagram) and after that turn on the Raspberry Pi.
2. Connect the Raspberry Pi to the internet.
3. Update system packages.
    ```bash
    sudo apt update && sudo apt upgrade
    ```
4. Create and activate a virtual environment.
    ```bash
    mkdir project && cd project
    python3 -m venv .venv
    source .venv/bin/activate
    ```
5. Install dependencies.
    ```bash
    pip3 install adafruit-circuitpython-shtc3 adafruit-circuitpython-ads1x15 RPi.GPIO tflite-runtime image pillow numpy pytz
    ```
6. Upload [automation nutrition and disease detection code](./code/IoT/ta-script.py) and model on Raspberry Pi.
7. Run the code with the following command.
    ```bash
    python3 ta-script.py
    ``` 
8. The results of disease prediction and the pH and ppm content values of the solution as well as temperature and humidity values can be seen on the Blynk Dashboard.

### VII. Result
#### Blynk Dashboard
<img alt="Blynk Dashboard" src="./results/hasil_blynk_dashboard_6.png"/>  

#### Hydroponic Installation
<img alt="Hydroponic Installation" src="./results/0_hasil%20implementasi%20rancangan%20ta.jpg" width="500"/>  
<img alt="Hydroponic Installation" src="./results/0_hasil%20implementasi%20rancangan%20ta_3.jpg" width="500"/>  
<img alt="Hydroponic Installation" src="./results/0_hasil%20implementasi%20rancangan%20ta_10.jpg" width="500"/>  
<img alt="Hydroponic Installation" src="./results/0_hasil%20implementasi%20rancangan%20ta_8.jpg" width="500"/>  

#### Sensor
**Temperature Sensor**  
accuracy: 99,05%
| Test | Actual Value (°C) | Sensor Value (°C) |
| ---- | ----------------- | ----------------- |
| 1 | 31 | 31 |
| 2 | 30 | 30 |
| 3 | 31 | 32 |
| 4 | 29 | 29 |
| 5 | 32 | 32 |
| 6 | 34 | 34 |
| 7 | 33 | 34 |
| 8 | 36 | 36 |
| 9 | 34 | 35 |
| 10| 26 | 26 |

**Humidity Sensor**  
accuracy: 99,54%
| Test | Actual Value (%) | Sensor Value (%) |
| ---- | ----------------- | ----------------- |
| 1 | 74 | 74 |
| 2 | 70 | 70 |
| 3 | 69 | 69 |
| 4 | 72 | 72 |
| 5 | 72 | 72 |
| 6 | 64 | 64 |
| 7 | 55 | 56 |
| 8 | 56 | 57 |
| 9 | 55 | 56 |
| 10| 60 | 60 |

**PH Sensor**  
accuracy: 98,60%
| Test | Actual Value | Sensor Value |
| ---- | ----------------- | ----------------- |
| 1 | 2,6 | 2,5 |
| 2 | 3,3 | 3,3 |
| 3 | 4,1 | 4,0 |
| 4 | 5,3 | 5,2 |
| 5 | 6,4 | 6,5 |
| 6 | 7,0 | 6,9 |
| 7 | 7,3 | 7,4 |
| 8 | 8,1 | 8,0 |
| 9 | 9,2 | 9,1 |
| 10| 11,1 | 11,0 |

**TDS Sensor**  
accuracy: 96,76%
| Test | Actual Value (ppm) | Sensor Value (ppm) |
| ---- | ----------------- | ----------------- |
| 1 | 5 | 5 |
| 2 | 291 | 298 |
| 3 | 328 | 346 |
| 4 | 475 | 532 |
| 5 | 540 | 536 |
| 6 | 684 | 643 |
| 7 | 749 | 747 |
| 8 | 867 | 842 |
| 9 | 927 | 938 |
| 10| 1.052 | 1.025 |

#### Model
**Model Evaluation Results Using Data from Datasets**
|                                 Model | Epoch | Akurasi | Ukuran File Model |
| ------------------------------------- | ----- | ------- | ----------------- |
|                                   CNN |   100 |     87% |            4,62MB | 
| Transfer Learning dengan MobileNet V2 |   100 |     92% |            2,54MB | 
| Transfer Learning dengan Inception V3 |   100 |     93% |           21,31MB | 
| Transfer Learning dengan ResNet50     |   100 |     48% |           23,06MB | 
| Transfer Learning dengan DesNet121    |   100 |     88% |            7,19MB | 

**Classification Report Model Results with MobileNetV2 from Datasets**
|             Class | Precision | Recall | F1-Score |
| ----------------- | --------- | ------ | -------- |
|       Karat Putih |      0,81 |   0,87 |     0,84 |
| Kekurangan Mangan |      1,00 |   1,00 |     1,00 |
|             Sehat |      1,00 |   1,00 |     1,00 |
|    Virus Keriting |      0,86 |   0,80 |     0,83 |

**Confusion Matrix Result**  
<img alt="confusion matrix result" src="./results/hasil_model_confusion matrix_dataset daun tunggal.png" width="500"/>  


**Model Evaluation Results Using Data Field Data**
|                                 Model | Epoch | Akurasi | Ukuran File Model |
| ------------------------------------- | ----- | ------- | ----------------- |
|                                   CNN |   100 |     29% |            4,62MB | 
| Transfer Learning dengan MobileNet V2 |   100 |     57% |            2,54MB | 
| Transfer Learning dengan Inception V3 |   100 |     27% |           21,31MB | 
| Transfer Learning dengan ResNet50     |   100 |     29% |           23,06MB | 
| Transfer Learning dengan DesNet121    |   100 |     30% |            7,19MB | 

**Classification Report Model Results with MobileNetV2 Using Data Field Data**
|             Class | Precision | Recall | F1-Score |
| ----------------- | --------- | ------ | -------- |
|       Karat Putih |      0,35 |   0,55 |     0,43 |
| Kekurangan Mangan |      0,54 |   0,47 |     0,50 |
|             Sehat |      0,67 |   0,53 |     0,59 |
|    Virus Keriting |      0,79 |   0,73 |     0,76 |

**Confusion Matrix Result**  
<img alt="confusion matrix result Using Data Field Data" src="./results/mobilenet_confusion matrix_dataset daun banyak.png" width="500"/>  
