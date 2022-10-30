# temperature_sensor_reader
This is a temperature sensor package designed for modbus. Implemented in pymodbus only. PyPI website: https://pypi.org/project/modbus-configuretools-xzf8971/
## Install
from pypi:  
```bash
pip install modbus-configuretools-xzf8971  
```
from github:  
```bahs
pip install git+https://github.com/xzf89718/temperature_sensor_reader
```
## Jiandarenke modbus RS485 as example  
### Before run scripts
Check the COM and chmod  
```bash
chmod 666 \dev\ttyUSBx
```
### Import modules  
```python
from modbus_configuretools import temperature_sensor.RS485_Jiandarenke as RS485_JDRK  
from modbus_configuretools import temperature_sensor.JDRKAddressConfig as Config
```
### Configure parameters for Jiandarenke RS485 sensor
It's OK to set None for unkown value
```python
# Modify these config values 
# Please configure these value in temperature_sensor before read or write values  
# SLAVEID must be specified. If SLAVEID is none, set to 1  
# ADDRESS_HUMIDITY = 0x0000  
# ADDRESS_TEMPERATURE_DEW_POINT = 0x0001  
# ADDRESS_TEMPERATURE = 0x0002  
# ADDRESS_TEMPERATURE_CALI = 0x0050  
# ADDRESS_HUMUDITY_CALI = 0x0051  
# ADDRESS_SLAVEID = 0x07D0  
# ADDRESS_BAUDRATE = 0x07D1  
# TEMPERATURE_CALI = 164  
# HUMIDITY_CALI = 7  
# SLAVEID = 1
# BAUDRATE = 1
myconfig = Config(ADDRESS_HUMIDITY, ADDRESS_TEMPERATURE_DEW_POINT, ADDRESS_TEMPERATURE, ADDRESS_SLAVEID, ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI, SLAVEID, BAUDRATE)
```
### Calibration of sensor. Not necessary calibration every time  
```python
sensor.CalibrationJiandarenke(myconfig)  
```
### Set slaveID and baudrate
Please make sure only 1 sensor connect to the modbus bus
```python
sensor.WriteSlaveIDAndBaudrate(myconfig)
```
### Init and read measured values from sensor  
```python
# Create a wrapper for JDRK sensor  
sensor = RS485_JDRK(port="/dev/ttyUSB0")  
# Init and connect client
sensor.InitClient()  
# Read slaveID and baudrate  
slaveID, baudrate = sensor.ReadSalveIDAndBaudrate(myconfig)  
# Read temperature, dew point, humidity in one request  
# Only correct for specified sensor
temperature, dew_point_temperature, humidity = sensor.ReadTemperatureAndHumidity(myconfig)  
# Read temperature only  
temperature = sensor.ReadTemperature(myconfig)  
# Read dew point temperature  
dew_point_temperature = sensor.ReadTemperatureDewPoint(myconfig)  
# Read humidity only  
humidity = sensor.ReadTemperature(myconfig)  
```
### Close the sensor
```python
sensor.close()
```
