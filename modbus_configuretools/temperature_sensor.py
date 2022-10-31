from modbus_configuretools.derived_modbus_wrapper import PyModbusWrapper
from modbus_configuretools.helper_function import encodeint16, decodeint16, decode_16bit_complemental_code, calculate_temperature_and_humidity
import numpy as np
import logging
logger = logging.getLogger("modbus_configuretools")
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


class JDRKAddressConfig():
    """
    It's OK to set None for unknown value. SLAVEID must specified.
    """

    def __init__(self, add_humidity, add_temperature_dew_point, add_temperature,  add_salveid, add_baudrate, add_temperature_cali, add_humidity_cali, temperature_cali, humidity_cali, slaveID, baudrate):
        self.ADDRESS_HUMIDITY = add_humidity
        self.ADDRESS_TEMPERATURE_DEW_POINT = add_temperature_dew_point
        self.ADDRESS_TEMPERATURE = add_temperature
        self.ADDRESS_TEMPERATURE_CALI = add_temperature_cali
        self.ADDRESS_HUMUDITY_CALI = add_humidity_cali
        self.ADDRESS_SLAVEID = add_salveid
        self.ADDRESS_BAUDRATE = add_baudrate

        self.TEMPERATURE_CALI = temperature_cali
        self.HUMIDITY_CALI = humidity_cali
        if (slaveID < 256 and slaveID > 0):
            self.SLAVEID = slaveID
        else:
            print(
                "JDRKAddressConfig WARNING slaveID must < 256 and < 0. Specified to default value 1")
            self.SLAVEID = 1
        self.BAUDRATE = baudrate


jdrk_config = JDRKAddressConfig(ADDRESS_HUMIDITY, ADDRESS_TEMPERATURE_DEW_POINT, ADDRESS_TEMPERATURE, ADDRESS_SLAVEID,
                                ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI, SLAVEID, BAUDRATE)


class RS485_Jiandarenke(PyModbusWrapper):

    def __init__(self, port, baudrate=4800, timeout=1):
        super().__init__(method='rtu', port=port, parity='N',
                         stopbits=1, bytesize=8, baudrate=baudrate, timeout=timeout)

    # temperature_cali and humidity_cali should be 10 times, and integer

    def CalibrationJiandarenke(self, JDRK_config=jdrk_config):
        is_success = self.WriteRegisgers(JDRK_config.ADDRESS_TEMPERATURE_CALI, [
                                         encodeint16(JDRK_config.TEMPERATURE_CALI)], JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to write Temperture Calibtration register")
        is_success = self.WriteRegisgers(
            JDRK_config.ADDRESS_HUMUDITY_CALI, [encodeint16(JDRK_config.ADDRESS_HUMUDITY_CALI)], JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to write Humidity Calibtration register")

    def DumpNonZeroRegisters(self, output_filename, begin_address, end_address, JDRK_config=jdrk_config):
        read_address = begin_address
        pass

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureAndHumidity(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_HUMIDITY, 3, JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to read Temperature and Humidity register")
            return []
        else:
            return [self.GetValueInResult()[2], self.GetValueInResult()[1], self.GetValueInResult()[0]]

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperature(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_TEMPERATURE, 1, JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to read Temperature register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureDewPoint(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_TEMPERATURE_DEW_POINT, 1, JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to read Temperature Dew Point register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadHumidity(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_HUMIDITY, 1, JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to read Humidity register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureAndHumidityCalibration(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_TEMPERATURE_CALI, 2, JDRK_config)
        if (not is_success):
            logger.error("Fail to read Temperature and Humidity register")
            return []
        else:
            return self.GetValueInResult()

    def ReadSlaveIDAndBaudrate(self, JDRK_config=jdrk_config):
        is_success = self.ReadHoldingRegisters(
            JDRK_config.ADDRESS_SLAVEID, 2, JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to read SlaveID and Baudrate register")
            return []
        else:
            return self.GetValueInResult()

    # Only usable for sepecified sensor. Like Jiandarenke 485
    def WriteSlaveIDAndBaudrate(self, JDRK_config=jdrk_config):
        is_success = self.WriteRegisgers(
            JDRK_config.ADDRESS_SLAVEID, [JDRK_config.SLAVEID, JDRK_config.BAUDRATE], JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to write SlaveID and Baudrate register")

    def WriteSlaveID(self, JDRK_config=jdrk_config):
        is_success = self.WriteRegisgers(
            JDRK_config.ADDRESS_SLAVEID, [JDRK_config.SLAVEID], JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to write SlaveID register")

    def WriteBaudrate(self, JDRK_config=jdrk_config):
        is_success = self.WriteRegisgers(
            JDRK_config.ADDRESS_BAUDRATE, [JDRK_config.BAUDRATE], JDRK_config.SLAVEID)
        if (not is_success):
            logger.error("Fail to write Baudrate register")
