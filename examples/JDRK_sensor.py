from modbus_configuretools.temperature_sensor import JDRKAddressConfig, RS485_Jiandarenke
import time
import logging
JDRK_sensor_logger = logging.getLogger("JDRK_sensor")
JDRK_sensor_logger.propagate = False
JDRK_sensor_logger.setLevel(level=logging.INFO)
file_handler = logging.FileHandler("JDRK_sensor.log")
logger_fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(logger_fmt)
JDRK_sensor_logger.addHandler(file_handler)
JDRK_sensor_logger.info(
    "Begin read temperature(in degree celsius) dew_point_temperature(in degree celsius) relative_humidity(in %)")
JDRK_sensor_logger.info(
    "Recording values is stored in JDRK_sensor.log")



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

PORT_NUMBER = "/dev/ttyUSB0"
PORT_BAUDRATE = 4800
PORT_TIMEOUT = 1
mysensor = RS485_Jiandarenke(
    port=PORT_NUMBER, baudrate=PORT_BAUDRATE, timeout=PORT_TIMEOUT)
mysensor.InitClient()

try:
    while True:
        temperature, temperature_dewpoint, humidity = mysensor.ReadTemperatureAndHumidity(
            JDRK_RS485_wangzike_config)
        _message_to_write = "{0}\t{1}\t{2}".format(
            temperature, temperature_dewpoint, humidity)
        JDRK_sensor_logger.info(_message_to_write)
        time.sleep(60)
except KeyboardInterrupt as error:
    JDRK_sensor_logger.warning("End write temperature into JDRK_sensor.log")
    mysensor.CloseClient()
