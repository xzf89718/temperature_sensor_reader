from temperature_data_analysis.data_wrapper import JDRKDataWrapper
from temperature_data_analysis.plot_wrapper import makeTemperatureAndHumidity

# Init a wrapper
data_wrapper = JDRKDataWrapper()
# Read data from a file
data_wrapper.ReadDataFile(r"C:\Users\zifeng\Documents\zifengCode\hgtd-peb\Demonstration\MUX64_QFN88_TEST\script\MUX64_reliability\MUX64_TC_test_temperature_log\MUX64_TC_test_Nov14_Nov28.log")
measure_time, measure_temp, measure_humi = data_wrapper.GetDataToPlot()
makeTemperatureAndHumidity(measure_time, measure_temp, measure_humi)