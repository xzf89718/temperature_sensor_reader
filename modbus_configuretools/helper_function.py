# helper function for modbus_configuretools
import numpy as np
# helper function for derived_modbus_wrapper
def check_is_port_connected(func):
    def wrapper(self, *args, **kwargs):
        if (self.is_port_connected == False):
            print(
                "check_is_port_connected WARNING The port {0} is not connected.\nThe program will continue, but the temperature and humidity can't be recorded.".format(self.port))
            return False
        else:
            func(self, *args, **kwargs)
            return True
    return wrapper


def check_result(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if (self.CheckResult() is None):
            print(
                "check_isError WARNING _result is None. Read/Write registers first before check_isError.\nThe program will continue, but the temperature and humidity can't be recorded.")
            return False
        if (self.CheckResult() == False):
            print(
                "check_isError WARNING Read/Write registers is not correct.\nThe program will continue, but the temperature and humidity can't be recorded.")
            return False
        else:
            return True
    return wrapper

# helper function for temperature_sensor
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
    