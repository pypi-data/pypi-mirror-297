import multiprocessing
import os
import subprocess
import sys
import wx
import TestWXPython
import logging

# Get the directory of the executable or script
if getattr(sys, 'frozen', False):
	# Running in a bundle
	base_dir = os.path.dirname(sys.executable)
else:
	# Running in a normal Python environment
	base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the log file path
log_file = os.path.join(base_dir, 'app.log')

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file, filemode='w')

# Redirect stdout and stderr to the log file
sys.stdout = open(log_file, 'a')
sys.stderr = open(log_file, 'a')

def handle_exception(exc_type, exc_value, exc_traceback):
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	print("Main: Unhandled exception:", exc_type, exc_value)
	
if __name__ == "__main__":
	app = wx.App(False)
	logging.debug('Main: calling UI code... ')
	frame = TestWXPython.SpreadsheetApp(None, "RyteBox Format Maker")
	#frame.show(true)
	try:
		app.MainLoop()
	except Exception as e:
		logging.error("Main: Exception occurred", exc_info=True)