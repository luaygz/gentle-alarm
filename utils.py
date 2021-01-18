import re
from time import sleep
from datetime import datetime

from typing import List

import numpy as np

def get_increments(lower: float, upper: float, n: int) -> List[float]:
	"""
	Divide a number range into `n` equally spaced points, inclusive of both endpoints.

	e.g. 
		lower = 0.5, upper = 1.0, n = 5
		-> [0.5, 0.625, 0.75, 0.875, 1.0]

	Arguments:
		lower (float): The lower bound.
		upper (float): The upper bound.
		n (int): The number of points.
	
	Returns:
		A list of `n` equally spaced numbers, between `lower` and `upper` (both inclusive).
	"""
	increments = np.linspace(lower, upper, n).tolist()
	return increments

def parse_time(time: str) -> str:
	"""
	Convert time to 24:00 format.
	
	Arguments:
		time (str): Time in either 24:00 hour format or am/pm e.g. 15:00, 8:30am, 5:30pm.

	Returns:
		Time in 24:00 format.
	"""
	hour_has_two_digits = len(time.split(":")[0]) == 2
	if not hour_has_two_digits:
		time = "0" + time

	if time.endswith("am") or time.endswith("AM"):
		time = time[:-2] # Strip AM
		if time.startswith("12"):
			time = "00" + time[2:] # 12:00am is 00:00am
	elif time.endswith("pm") or time.endswith("PM"):
		time = time[:-2] # Strip PM
		hour = int(time[:2])
		hour_as_24 = hour + 12
		time = str(hour_as_24) + time[2:]
	
	return time

def wait_until(time: str) -> None:
	"""
	Wait until the specified time.

	Arguments:
		time (str): What time to wait until; must be in 24:00 hour format e.g. 8:00, 15:30.
	"""
	time = parse_time(time)
	while True:
		now = datetime.now()
		current_time = now.strftime("%H:%M")
		if time == current_time:
			break
		sleep(1)

def is_valid_time(time: str) ->  bool:
	"""
	Check if time is a valid time string.

	Accepted formats are 24:00 format, or 12:00 hour format followed by am/pm/AM/PM.
		e.g. 13:00, 5:30pm.

	Arguments:
		time (str): A time string.

	Returns:
		Whether the time string is in the correct format.
	"""
	valid_24hr_time_regex = re.compile("^([0-1]?[0-9]|2[0-4]):[0-5][0-9]$")
	is_valid_24hr_time = True if valid_24hr_time_regex.match(time) else False

	valid_am_pm_time_regex = re.compile("^(0?[1-9]|1[1-2]):[0-5][0-9](am|pm|AM|PM)$")
	is_valid_am_pm_time = True if valid_am_pm_time_regex.match(time) else False

	is_valid_time = is_valid_24hr_time or is_valid_am_pm_time
	return is_valid_time

def validate_input(time: str, start_volume: float, end_volume: float, duration: int) -> None:
	"""Validate input."""
	assert is_valid_time(time), "Time is invalid."
	assert start_volume >= 0.0 and start_volume <= 1.0, "Start volume should be between 0 and 1."
	assert end_volume >= 0.0 and end_volume <= 1.0, "End volume should be between 0 and 1."
	assert start_volume <= end_volume, "Start volume should be less that or equal to end volume."
	assert duration >= 0, "Duration needs to be greater than or equal to zero."