import pyvisa
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import itertools



OHMs = "\u03A9"

def print_with_colour(colour, string):
	colours = {
		"black": "\033[30m",
		"red": "\033[31m",
		"green": "\033[32m",
		"yellow": "\033[33m",
		"blue": "\033[34m",
		"magenta": "\033[35m",
		"cyan": "\033[36m",
		"white": "\033[37m",
		"reset": "\033[0m"
	}
	
	if colour.lower() in colours:
		print(f"{colours[colour.lower()]}{string}{colours["reset"]}")
	else:
		print(f"{string}")

class Generic_Visa_Device:
	def __init__(self, device_id):
		self.device = self._Connect_To_Device(device_id)
		if self.device == None:
			raise ValueError("Failed to connect to device")
		self.terminal_width = 80

	def _Connect_To_Device(self, device_name="Ask the user"):
		resource_manager = pyvisa.ResourceManager()
		available_devices = resource_manager.list_resources()
		
		if device_name in available_devices:
			device_to_use = device_name
		elif len(available_devices) == 0:
			print("No device found.")
			return None
		elif len(available_devices) == 1:
			device_to_use = available_devices[0]
		else:
			while True:
				for index, device_id in enumerate(available_devices):
					print(f"[{index}] {device_id}")

				user_input = int(input("Please select the device: "))
				if user_input < len(available_devices):
					device_to_use = available_devices[user_input]
					break
				else:
					print("Invalid entry, please select an ID from the list")

		try:
			local_device = resource_manager.open_resource(device_to_use)
			local_device.write("*IDN?")
			print(f"Successfully connected to\n{local_device.read()}")
			return local_device
		except Exception as error_reason:
			print(f"Failed to connect: {error_reason}")
			return None
			

	def _Write_Only(self, command):
		try:
			self.device.write(command)
		except Exception as error_reason:
			print(f"Error writing: {error_reason}")

	def _Read_Only(self):
		try:
			message = self.device.read()
			return message
		except Exception as error_reason:
			print(f"Error reading: {error_reason}")
			return None
	 
	def _Read_Command(self, command):
		self._Write_Only(command)
		print(f"[Write]\t{command}")
		response = self._Read_Only()
		print(f"[Read]\t{response}")
		return response

	def _Write_Command(self, command):
		self._Write_Only(command)
		if len(command) > self.terminal_width:
			print(f"[Write]\t{command[:self.terminal_width]}...")
		else:
			print(f"[Write]\t{command}")

if __name__ == "__main__":
	def live_plot():
		def measure_value():
			while True:
				measurement = float(U2741A._Read_Command("READ?"))
				print_with_colour("Blue", f"Resistance: {measurement}{OHMs}")
				yield measurement

		# Initialize the plot
		fig, ax = plt.subplots()
		xdata, ydata = [], []
		ln, = plt.plot([], [], 'b-')
		yLowerLimit = 0
		yUpperLimit = 1

		def init():
			ax.set_xlim(0, 100)
			ax.set_ylim(0, 1)
			return ln,

		def update(frame):
			nonlocal yLowerLimit, yUpperLimit
			xdata.append(frame)
			ydata.append(next(measurement))

			# Keep only the last 100 data points
			if len(xdata) > 100:
				xdata.pop(0)
				ydata.pop(0)

			ln.set_data(xdata, ydata)

			if frame >= 1:
				ax.set_xlim(max(0, frame-100), frame)
			else:
				ax.set_xlim(0,1)
				
			A = 0.63
			if frame == 0:
				yLowerLimit = min(ydata)
				yUpperLimit = max(ydata)
			else:
				delta = (max(ydata) - min(ydata)) / 100
				yLowerLimit = yLowerLimit * A + (min(ydata) - delta) * (1 - A)
				yUpperLimit = yUpperLimit * A + (max(ydata) + delta) * (1 - A)

			ax.set_ylim(yLowerLimit, yUpperLimit)

			return ln,

		measurement = measure_value()
		frame_gen = itertools.count()

		ani = animation.FuncAnimation(fig, update, frames=frame_gen, init_func=init, blit=False)
		plt.show()

	try:
		U2741A = Generic_Visa_Device("USB0::0x0957::0x4918::MY64010002::0::INSTR")
		U2741A._Write_Command("CONF:RES AUTO, MAX")
		live_plot()
	except Exception as error_reason:
		print(f"Failed during operation: {error_reason}")
