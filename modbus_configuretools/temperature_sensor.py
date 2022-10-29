from modbus_configuretools.derived_modbus_wrapper import PyModbusWrapper
import numpy as np
# These decorators are designed for RS485_Jiandarenke


def decode_16bit_complemental_code(func):
    def wrapper(self, *args, **kwargs):
        # This values shoud be a list
        values_in_registers = func(self, *args, **kwargs)
        values_in_registers_decoded = []
        for value in values_in_registers:
            values_in_registers_decoded.append(decodeint16(value))
        return values_in_registers_decoded
    return wrapper


def calculate_temperature_and_humidity(func):
    def wrapper(self, *args, **kwargs):
        # This values shoud be a list
        values_in_registers = func(self, *args, **kwargs)
        values_in_registers_decoded = []
        for value in values_in_registers:
            values_in_registers_decoded.append(float(value)/10)
        return values_in_registers_decoded
    return wrapper


def decodeint16(value):
    return np.int16(value)


def encodeint16(value):

    if (value > 32767 or value < -32768):
        return None
    if value >= 0:
        return value
    if value < 0:
        value = abs(value)
        value_in_bits = bin(value).replace("0b", "")
        print(value_in_bits)
        _decode_buffers = ["1"] * 15
        for index, _value in enumerate(value_in_bits):
            if _value == "0":
                _decode_buffers[14 + index - len(value_in_bits) + 1] = "1"
            elif _value == "1":
                _decode_buffers[14 + index - len(value_in_bits) + 1] = "0"
        _decode_value = "0b1"
        for _value in _decode_buffers:
            _decode_value = _decode_value + _value
        # only on system with more than 16 bits
        decode_value = int("0b1" + bin(int(_decode_value, 2) + 1)[-15:], 2)
        return decode_value


ADDRESS_HUMIDITY = 0x0000
ADDRESS_TEMPERATURE_DEW_POINT = 0x0001
ADDRESS_TEMPERATURE = 0x0002
ADDRESS_TEMPERATURE_CALI = 0x0050
ADDRESS_HUMUDITY_CALI = 0x0051
ADDRESS_SLAVEID = 0x07D0
ADDRESS_BAUDRATE = 0x07D1

TEMPERATURE_CALI = 164
HUMIDITY_CALI = 7


class JDRKAddressConfig():

    def __init__(self, add_humidity, add_temperature_dew_point, add_temperature,  add_salveid, add_baudrate, add_temperature_cali, add_humidity_cali, temperature_cali, humidity_cali):
        self.ADDRESS_HUMIDITY = add_humidity
        self.ADDRESS_TEMPERATURE_DEW_POINT = add_temperature_dew_point
        self.ADDRESS_TEMPERATURE = add_temperature
        self.ADDRESS_TEMPERATURE_CALI = add_temperature_cali
        self.ADDRESS_HUMUDITY_CALI = add_humidity_cali
        self.ADDRESS_SLAVEID = add_salveid
        self.ADDRESS_BAUDRATE = add_baudrate

        self.TEMPERATURE_CALI = temperature_cali
        self.HUMIDITY_CALI = humidity_cali


jdrk_config = JDRKAddressConfig(ADDRESS_HUMIDITY, ADDRESS_TEMPERATURE_DEW_POINT, ADDRESS_TEMPERATURE, ADDRESS_SLAVEID,
                                ADDRESS_BAUDRATE, ADDRESS_TEMPERATURE_CALI, ADDRESS_HUMUDITY_CALI, TEMPERATURE_CALI, HUMIDITY_CALI)


class RS485_Jiandarenke(PyModbusWrapper):

    def __init__(self, port, baudrate=4800, timeout=1, jdrk_cfg=jdrk_config):
        super().__init__(method='rtu', port=port, parity='N',
                         stopbits=1, bytesize=8, baudrate=baudrate, timeout=timeout)
        self.cfg = jdrk_cfg

    
    # temperature_cali and humidity_cali should be 10 times, and integer
    def CalibrationJiandarenke(self, temperature_cali, humidity_cali, slaveID=1):
        is_success = self.WriteRegisgers(self.cfg.ADDRESS_TEMPERATURE_CALI, [
                                         encodeint16(temperature_cali)], slaveID)
        if (not is_success):
            print("Fail to write Temperture Calibtration register")
        is_success = self.WriteRegisgers(
            self.cfg.ADDRESS_HUMUDITY_CALI, [encodeint16(humidity_cali)], slaveID)
        if (not is_success):
            print("Fail to write Humidity Calibtration register")

    def DumpNonZeroRegisters(self, output_filename, begin_address, end_address, slaveID=1):
        read_address = begin_address
        pass

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureAndHumidity(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_HUMIDITY, 3, slaveID)
        if (not is_success):
            print("Fail to read Temperature and Humidity register")
            return []
        else:
            return [self.GetValueInResult()[2], self.GetValueInResult()[1], self.GetValueInResult()[0]]

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperature(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_TEMPERATURE, 1, slaveID)
        if (not is_success):
            print("Fail to read Temperature register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureDewPoint(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_TEMPERATURE_DEW_POINT, 1, slaveID)
        if (not is_success):
            print("Fail to read Temperature Dew Point register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadHumidity(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_HUMIDITY, 1, slaveID)
        if (not is_success):
            print("Fail to read Humidity register")
            return []
        else:
            return self.GetValueInResult()

    @calculate_temperature_and_humidity
    @decode_16bit_complemental_code
    def ReadTemperatureAndHumidityCalibration(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_TEMPERATURE_CALI, 2, slaveID)
        if (not is_success):
            print("Fail to read Temperature and Humidity register")
            return []
        else:
            return self.GetValueInResult()

    def ReadSlaveIDAndBaudrate(self, slaveID=1):
        is_success = self.ReadHoldingRegisters(
            self.cfg.ADDRESS_SLAVEID, 2, slaveID)
        if (not is_success):
            print("Fail to read SlaveID and Baudrate register")
            return []
        else:
            return self.GetValueInResult()

    def WriteSlaveIDAndBaudrate(self, baudrate, slaveID=1):
        is_success = self.WriteRegisgers(
            self.cfg.ADDRESS_SLAVEID, [slaveID, baudrate], slaveID)
        if (not is_success):
            print("Fail to write SlaveID and Baudrate register")
