import re
from time import sleep
from datetime import datetime

from typing import List, Tuple

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

def validate_input(time: str, start_volume: float, end_volume: float, duration: int) -> None:
	"""Validate input."""
	assert parse_time(time), "Time is invalid."
	assert start_volume >= 0.0 and start_volume <= 1.0, "Start volume should be between 0 and 1."
	assert end_volume >= 0.0 and end_volume <= 1.0, "End volume should be between 0 and 1."
	assert start_volume <= end_volume, "Start volume should be less that or equal to end volume."
	assert duration >= 0, "Duration needs to be greater than or equal to zero."