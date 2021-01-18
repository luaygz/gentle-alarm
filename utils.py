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
	"""Convert time to 24:00 format."""
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
		time (str): What time to wait until, in 24:00 hour format.
	`time` must be in 24:00 hour format.

	e.g.
		8:30
		12:00
		15:45
	"""
	time = parse_time(time)
	while True:
		now = datetime.now()
		current_time = now.strftime("%H:%M")
		if time == current_time:
			break
		sleep(1)

def time_is_valid(time: str):
	pattern = re.compile("^[0-9]{1,2}:[0-9]{1,2}$")
	is_valid_time = pattern.match(string)
	return is_valid_time