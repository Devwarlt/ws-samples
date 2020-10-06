from datetime import datetime
import os

class TimedProfiler(object):
	LOG_FILE = "web-scraping-report-logs.txt"

	def __init__(self, callback, target = None):
		self.start_time = None
		self.callback = callback
		self.target = target
		self.enable_logging = False
		self.session_logs = list()

	@property
	def total_elapsed(self):
		if self.start_time is None: return 0
		else:
			delta = datetime.now() - self.start_time
			return delta.total_seconds() * 1000

	@property
	def enable_logging(self):
		return self.__enable_logging

	@enable_logging.setter
	def enable_logging(self, val):
		if type(val) == bool: self.__enable_logging = val

	def start(self) -> type(None):
		self.start_time = datetime.now()

	def stop(self) -> type(None):
		self.endTime = datetime.now()
		input = "[{0}] -> msg: '{1}', elapsed: {2} ms{3}"
		input = input.format(
			type(self).__name__,
			self.target,
			self.total_elapsed,
			"\n" if self.enable_logging else ""
		)

		if self.enable_logging:
			self.attach_logs(input)
		
	def log(self, input) -> type(None):
		pattern = "[{0}] -> msg: '{1}'\n"
		pattern = pattern.format(
			type(self).__name__,
			input
		)
		self.attach_logs(pattern)

	def attach_logs(self, input) -> type(None):
		now = datetime.now()
		time_format = now.strftime("%d/%m/%Y - %H:%M:%S")
		pattern = f"[{time_format}] {input}"
		self.callback(pattern)
		self.session_logs.append(pattern)
	
	def save_logs(self) -> type(None):
		self.callback("Salvando os logs...")
		output = ">>> Init of report\n"
		for session_log in self.session_logs:
			output += session_log
		output += ">>> End of report\n"
		if os.path.exists(self.LOG_FILE):
			f = open(self.LOG_FILE, "a")
			f.write(output)
			f.close()
		else:
			f = open(self.LOG_FILE, "w")
			f.write(output)
			f.close()