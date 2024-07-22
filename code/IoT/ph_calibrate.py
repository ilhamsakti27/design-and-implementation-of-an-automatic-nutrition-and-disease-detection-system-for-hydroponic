import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from DFRobot_PH import DFRobot_PH

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

channelPH = AnalogIn(ads, ADS.P0)

# setup ph
ph = DFRobot_PH()
ph.begin()

while True :
	temperature = 25
	#Set the IIC address
	#ads1115.setAddr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	#ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
	#Get the Digital Value of Analog of selected channel
	adc0 = channelPH.voltage*1000
	print(f"A0: {adc0}mV")
	#Calibrate the calibration data
	ph.calibration(adc0)
	time.sleep(1.0)