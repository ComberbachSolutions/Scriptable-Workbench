import spd3303x
import time



# with spd3303x.EthernetDevice("169.254.140.1") as dev:
#     dev.CH1.set_voltage(8)
#     dev.CH1.set_current(0.75)
#     dev.CH1.set_output(True)
#     print(dev.CH1.get_current())
#     print(dev.CH1.get_voltage())
#     print(dev.CH1.measure_voltage())
#     print(dev.CH1.measure_current())
#     dev.CH3.set_output(True)

time_to_sleep = 0.25 # 250ms isn't perfect, but it does work most of the time
with spd3303x.EthernetDevice("169.254.140.1") as dev:
    dev.CH1.set_output(True)
    for voltage in range(0,32+1):
        dev.CH1.set_voltage(voltage)
        dev.CH1.set_current(voltage/10)
        time.sleep(time_to_sleep)
    dev.CH1.set_voltage(0)