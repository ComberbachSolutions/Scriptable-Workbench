import time
import spd3303x



def Delay_In_Seconds(seconds=1.0):
    seconds = max(seconds, 0.25)
    time.sleep(seconds)

def Display_Live_Values():
    with spd3303x.EthernetDevice("169.254.140.1") as dev:
        print("*****CH1*****")
        print(f"Set to\t{dev.CH1.get_voltage()}V\t{dev.CH1.get_current()}A")
        print(f"Actual\t{dev.CH1.measure_voltage()}V\t{dev.CH1.measure_current()}A\t{dev.CH1.measure_power()}W")
        print("*****CH2*****")
        print(f"Set to\t{dev.CH2.get_voltage()}V\t{dev.CH2.get_current()}A")
        print(f"Actual\t{dev.CH2.measure_voltage()}V\t{dev.CH2.measure_current()}A\t{dev.CH2.measure_power()}W")

def Setup_For_MUA():
    with spd3303x.EthernetDevice("169.254.140.1") as dev:
        dev.CH1.set_output(False)
        # dev.CH1.set_voltage(3.3)
        # dev.CH1.set_voltage(6.6)
        # dev.CH1.set_voltage(10.0)
        # dev.CH1.set_voltage(12.0)
        # dev.CH1.set_current(0.05)
        # dev.CH1.set_output(True)

        dev.CH2.set_output(False)
        dev.CH2.set_voltage(30.0)
        dev.CH2.set_current(0.10)
        dev.CH2.set_output(True)
        Delay_In_Seconds(1.0)
        dev.CH2.set_current(0.05)

        dev.CH3.set_output(False)
    Delay_In_Seconds(1.0)
    Display_Live_Values()

