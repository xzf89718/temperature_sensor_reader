import re
import time
import datetime
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class DataCell():
    def __init__(self, measure_time, temp, humidity):
        self.measure_time = measure_time
        self.temp = temp
        self.humidity = humidity


class DataWrapperBase():

    def __init__(self):
        # self.re_measure_time = re.compile(re_measure_time)
        # self.re_temp = re.compile(re_temp)
        # self.re_humidity = re.compile(re_humidity)
        self.all_data = []
        self._line = None

    def ReadDataFile(self, filename):
        pass

    def ReadTimeFromLine(self):
        pass

    def ReadTempAndHumidityFromLine(self):
        pass

    def GetHumidityAndTemperature(self, measure_time):
        pass

    def GetDataToPlot(self):
        _data_measure_time = []
        _data_temp = []
        _data_humidity = []

        for _data in self.all_data:
            _data_measure_time.append(_data.measure_time)
            _data_temp.append(_data.temp)
            _data_humidity.append(_data.humidity)
        return _data_measure_time, _data_temp, _data_humidity


class JDRKDataWrapper(DataWrapperBase):

    def __init__(self):
        super().__init__()

    def ReadDataFile(self, filename):
        with open(filename, "r") as file_object:
            self._line = "DEFAULT"
            while (self._line != ""):
                self._line = file_object.readline()
                measure_measure_time = self.ReadTimeFromLine()
                # print(measure_measure_time)
                measure_temp, measure_humidity = self.ReadTempAndHumidityFromLine()
                # print(measure_temp, measure_humidity)
                if (measure_measure_time is None):
                    continue
                if (not(measure_temp or measure_humidity)):
                    continue
                self.all_data.append(
                    DataCell(measure_measure_time, measure_temp, measure_humidity))

    def ReadTimeFromLine(self):
        re_measure_time = re.compile(
            "\d{4}-\d{1,2}-\d{1,2} \d{1,2}\:\d{1,2}\:\d{1,2}")
        str_measure_time = re_measure_time.findall(self._line)

        if (len(str_measure_time) > 0):
            return datetime.datetime.strptime(str_measure_time[0], DATETIME_FMT)
        else:
            return None

    def ReadTempAndHumidityFromLine(self):
        re_temperature = re.compile("[-+]*\d{1,}\.\d{1,2}")
        re_humidity = re.compile("[-+]*\d{1,}\.\d{1,2}")
        str_temperature = re_temperature.findall(self._line)
        str_humidity = re_humidity.findall(self._line)

        _temp = None
        _humi = None
        if (len(str_temperature) == 0):
            pass
        if (len(str_temperature) == 2):
            _temp = float(str_temperature[0])
            _humi = float(str_temperature[1])

        return _temp, _humi

    def GetHumidityAndTemperature(self, measure_time):
        if (not isinstance(measure_time, datetime.datetime)):
            raise NotImplementedError("time must be datetime.datetime")
        data_index = None
        for index, data in enumerate(self.all_data[:-1]):
            if (measure_time > data.measure_time and measure_time < self.all_data[index + 1].measure_time):
                data_index = index
        if (data_index is None):
            print("Fail find a suitable time interval.")
            return None, None
        return self.all_data[data_index], self.all_data[data_index + 1]
