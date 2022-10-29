# ModbusWrapper base class implement in Python

class ModbusWrapper():

    def __init__(self, method, port, parity, stopbits, bytesize, baudrate, timeout):
        # More parameter is welcome!
        self.method = method
        self.port = port
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.baudrate = baudrate
        self.timeout = timeout
        self._client = None
        self._result = None
        self.is_port_connected = False

    def InitClient(self):

        raise NotImplementedError("InitClient need to be reimplement")

    def CloseClient(self):

        raise NotImplementedError("CloseClient need to be reimplement")

    def GetValueInResult(self):

        raise NotImplementedError("GetValueInResult need to be reimplement")

    def ReadHoldingRegisters(self, address, count, slaveID):

        raise NotImplementedError(
            "ReadHoldingRegisters need to be reimplement")

    def WriteRegisgers(self, address, list_of_values, slaveID):

        raise NotImplementedError("WriteRegisgers need to be reimplement")

    def CheckResult(self):
        # Return True means OK
        # Return False means not OK

        raise NotImplementedError("CheckResult need to be reimplement")
