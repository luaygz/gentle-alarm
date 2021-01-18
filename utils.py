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
	hour_has_two_digits = len(time.split(":")[0]) == 2
	if not hour_has_two_digits:
		time = "0" + time

	while True:
		now = datetime.now()
		current_time = now.strftime("%H:%M")
		if time == current_time:
			break
		sleep(1)
