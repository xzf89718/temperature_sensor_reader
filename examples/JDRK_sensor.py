from modbus_configuretools.temperature_sensor import JDRKAddressConfig, RS485_Jiandarenke
import time
from custom_logger import CustomLoggerWrapper
logger_wrapper = CustomLoggerWrapper("JDRK_sensor", log_filename="MUX64_TC_test.log")
logger_wrapper.InitLogger()
JDRK_sensor_logger = logger_wrapper.GetInitedLogger()

ADDRESS_HUMIDITY = 0x0000
ADDRESS_TEMPERATURE_DEW_POINT = 0x0001
ADDRESS_TEMPERATURE = 0x0002
ADDRESS_TEMPERATURE_CALI = 0x0050
ADDRESS_HUMUDITY_CALI = 0x0051
ADDRESS_SLAVEID = 0x07D0
ADDRESS_BAUDRATE = 0x07D1

TEMPERATURE_CALI = 164
HUMIDITY_CALI = 7
SLAVEID = 1
BAUDRATE = 1

JDRK_RS485_wangzike_config = JDRKAddressConfig(ADDRESS_HUMIDITY, ADDRESS_TEMPERATURE_DEW_POINT, ADDRESS_TEMPERATURE, ADDRESS_SLAVEID,
                                               ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI, SLAVEID, BAUDRATE)

JDRK_RS485_box_config = JDRKAddressConfig(0x0000, None, 0x0001, ADDRESS_SLAVEID,
                                               ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI, SLAVEID, BAUDRATE)


PORT_NUMBER = "/dev/ttyUSB0"
PORT_BAUDRATE = 4800
PORT_TIMEOUT = 1
mysensor = RS485_Jiandarenke(
    port=PORT_NUMBER, baudrate=PORT_BAUDRATE, timeout=PORT_TIMEOUT)
mysensor.InitClient()

try:
    while True:
        temperature = mysensor.ReadTemperature(JDRK_RS485_box_config)
        # Check if read temperature success
        if (len(temperature) > 0):
            temperature = temperature[0]
        else:
            temperature = "NULL"
        humidity = mysensor.ReadHumidity(JDRK_RS485_box_config)
        # Check if read humidity success
        if (len(humidity) > 0):
            humidity = humidity[0]
        else:
            humidity = "NULL"
        _message_to_write = "{0}\t{1}".format(
            temperature, humidity)
        JDRK_sensor_logger.info(_message_to_write)
        # Get temperature and humidity every 30s
        time.sleep(30)
except KeyboardInterrupt as error:
    JDRK_sensor_logger.warning("End write temperature into log")
    mysensor.CloseClient()
