# This file implement ModbusWrapper in pymodbus
# These decorators are designed for PyModbusWrapper

from modbus_configuretools.modbus_wrapper import ModbusWrapper
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusIOException
from modbus_configuretools.helper_function import check_is_port_connected, check_result
from custom_logger import CustomLoggerWrapper, FMT_WITH_MODULENAME
import logging

logger_wrapper = CustomLoggerWrapper("derived_modbus_wrapper", logger_level=logging.WARNING, logger_fmt=FMT_WITH_MODULENAME, log_filename="derived_modbus_wrapper.log")
logger_wrapper.InitLogger()
mylogger = logger_wrapper.GetInitedLogger()

class PyModbusWrapper(ModbusWrapper):

    def __init__(self, method, port, parity, stopbits, bytesize, baudrate, timeout):
        super().__init__(method, port, parity, stopbits, bytesize, baudrate, timeout)

    def InitClient(self):
        self._client = ModbusClient(method=self.method, port=self.port,
                                    parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize, baudrate=self.baudrate, timeout=self.timeout)
        self.is_port_connected = self._client.connect()
        if (self.is_port_connected is False):
            mylogger.error("Fail to connect client in InitClient().")

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

    def CheckResult(self):
        if (isinstance(self._result, ModbusIOException)):
            mylogger.error("Modbus IOException occurs.")
            return False
        if (self._result is None):
            mylogger.warning("self._result is None")
            return None
        else:
            if self._result.isError():
                mylogger.warning("isError() check failed")
                return False
            else:
                return True