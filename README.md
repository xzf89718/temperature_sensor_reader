# temperature_sensor_reader
This is a temperature sensor package designed for modbus. Implemented in pymodbus only.

## Jiandarenke modbus RS485 as example  
### Import modules  
from modbus_configuretools import temperature_sensor.RS485_Jiandarenke as RS485_JDRK  
from modbus_configuretools import temperature_sensor.JDRKAddressConfig as Config
### Configure parameters for Jiandarenke RS485 sensor
\# Modify these config values 
\# Please configure these value in temperature_sensor before read or write values  
\# ADDRESS_HUMIDITY = 0x0000  
\# ADDRESS_TEMPERATURE_DEW_POINT = 0x0001  
\# ADDRESS_TEMPERATURE = 0x0002  
\# ADDRESS_TEMPERATURE_CALI = 0x0050  
\# ADDRESS_HUMUDITY_CALI = 0x0051  
\# ADDRESS_SLAVEID = 0x07D0  
\# ADDRESS_BAUDRATE = 0x07D1  
\# TEMPERATURE_CALI = 164  
\# HUMIDITY_CALI = 7  
myconfig = Config(ADDRESS_HUMIDITY, ADDRESS_TEMPERATURE_DEW_POINT, ADDRESS_TEMPERATURE, ADDRESS_SLAVEID, ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI)
### Calibration of sensor. Not necessary calibration every time  
sensor.CalibrationJiandarenke(sensor.cfg.ADDRESS_TEMPERATURE_CALI, sensor.cfg.ADDRESS_HUMUDITY_CALI, slaveID=1)  
### Init and read registers from sensor  
\# Create a wrapper for JDRK sensor  
sensor = RS485_JDRK(port="/dev/ttyUSB0", myconfig)  
\# Init and connect client
sensor.InitClient()  
\# Read slaveID and baudrate  
slaveID, baudrate = sensor.ReadSalveIDAndBaudrate(salveID=1)  
\# Read temperature, dew point, humidity in one request  
\# Only correct for specified sensor
temperature, dew_point_temperature, humidity = sensor.ReadTemperatureAndHumidity(slaveID=1)  
\# Read temperature only  
temperature = sensor.ReadTemperature(slaveID=1)  
\# Read dew point temperature  
dew_point_temperature = sensor.ReadTemperatureDewPoint(SlaveID=1)  
\# Read humidity only  
humidity = sensor.ReadTemperature(slaveID=1)  
### Close the sensor
sensor.close()
