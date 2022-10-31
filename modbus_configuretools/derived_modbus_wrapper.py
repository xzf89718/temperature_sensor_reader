# This file implement ModbusWrapper in pymodbus
# These decorators are designed for PyModbusWrapper

from modbus_configuretools.modbus_wrapper import ModbusWrapper
from pymodbus.client import ModbusSerialClient as ModbusClient
from modbus_configuretools.helper_function import check_is_port_connected, check_result
import logging
logger = logging.getLogger("modbus_configuretools")


class PyModbusWrapper(ModbusWrapper):

    def __init__(self, method, port, parity, stopbits, bytesize, baudrate, timeout):
        super().__init__(method, port, parity, stopbits, bytesize, baudrate, timeout)

    def InitClient(self):
        self._client = ModbusClient(method=self.method, port=self.port,
                                    parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize, baudrate=self.baudrate, timeout=self.timeout)
        self.is_port_connected = self._client.connect()
        if (self.is_port_connected is False):
            logger.error("Fail to connect client.")

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
