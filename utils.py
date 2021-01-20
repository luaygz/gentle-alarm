import os
from time import sleep
from datetime import datetime

from typing import Tuple

def parse_time(time: str) -> Tuple[int, int]:
	try:
		if time.lower().endswith(("am", "pm")):
			time_dt = datetime.strptime(time, '%I:%M%p')
		else:
			time_dt = datetime.strptime(time, '%H:%M')
		return time_dt.hour, time_dt.minute
	except ValueError:
		return False

def wait_until(time: str) -> None:
	"""
	Wait until the specified time.

	Arguments:
		time (str): What time to wait until e.g. 8:00, 15:30, 8:00am, 3:30pm.
	"""
	hour, minute = parse_time(time)
	while True:
		now = datetime.now()
		if hour == now.hour and minute == now.minute:
			break
		sleep(1)

def validate_input(time: str, songs_dir: str, start_volume: float, end_volume: float, duration: int) -> None:
	"""Validate input."""
	assert parse_time(time), "Time is invalid."
	assert os.path.exists(songs_dir), "Directory does not exist."
	assert start_volume >= 0 and start_volume <= 100, "Start volume should be between 0 and 1."
	assert end_volume >= 0 and end_volume <= 100, "End volume should be between 0 and 1."
	assert start_volume <= end_volume, "Start volume should be less that or equal to end volume."
	assert duration >= 0, "Duration needs to be greater than or equal to zero."