# This file implement ModbusWrapper in pymodbus
# These decorators are designed for PyModbusWrapper

from modbus_configuretools.modbus_wrapper import ModbusWrapper
from pymodbus.client import ModbusSerialClient as ModbusClient


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


class PyModbusWrapper(ModbusWrapper):

    def __init__(self, method, port, parity, stopbits, bytesize, baudrate, timeout):
        super().__init__(method, port, parity, stopbits, bytesize, baudrate, timeout)

    def InitClient(self):
        self._client = ModbusClient(method=self.method, port=self.port,
                                    parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize, baudrate=self.baudrate, timeout=self.timeout)
        self.is_port_connected = self._client.connect()
        if (self.is_port_connected is False):
            print("PyModbusWrapper WARNING Fail to connect client.")

        return self.is_port_connected

    @check_is_port_connected
    def CloseClient(self):
        self._client.close()
        self.is_port_connected = False

    def GetValueInResult(self):
        return self._result.registers

    @check_result
    @check_is_port_connected
    def ReadHoldingRegisters(self, address, count, slaveID):
        self._result = self._client.read_holding_registers(
            address, count, slaveID)

    @check_result
    @check_is_port_connected
    def WriteRegisgers(self, address, list_of_values, slaveID):
        self._result = self._client.write_registers(
            address, list_of_values, slaveID)

    @check_is_port_connected
    def CheckResult(self):
        if (self._result is not None):
            # For pymodbus isError()
            # False means no Error
            # True means error occured
            return not self._result.isError()
        else:
            return None
