# temperature_sensor_reader
This is a temperature sensor package designed for modbus. Implemented in pymodbus only.

Wrapper for Jiandarenke sensors usage:  
from modbus_configuretools import temperature_sensor 
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

from modbus_configuretools import temperature_sensor.RS485_Jiandarenke as RS485_JDRK  
sensor = RS485_JDRK(port="/dev/ttyUSB0")  
sensor.InitClient()  
slaveID, baudrate = sensor.ReadSalveIDAndBaudrate(salveID=1)  
temperature, dew_point_temperature, humidity = sensor.ReadTemperatureAndHumidity(slaveID=1)  
sensor.close()