def enqueue(file_path: str) -> None:
	"""Enqueue a song."""
	subprocess.run(["rhythmbox-client", "--enqueue", file_path])

def enqueue_batch(file_paths: List[str]) -> None:
	"""Enqueue a list of songs."""
	for fp in file_paths:
		enqueue(fp)

def clear_queue() -> None:
	"""Clear the song queue."""
	subprocess.run(["rhythmbox-client", "--clear-queue"])

def play() -> None:
	"""Start playing music."""
	subprocess.run(["rhythmbox-client", "--play"])

def stop() -> None:
	"""Stop playing music."""
	subprocess.run(["rhythmbox-client", "--stop"])

def set_volume(level: float) -> None:
	"""
	Set the music volume.

	Arguments:
		level (float): The volume level, a float between 0.0 and 1.0.
	"""
	subprocess.run(["rhythmbox-client", "--set-volume", str(level)])

def increase_volume_gradually(start_volume: float, end_volume: float, duration: int) -> None:
	"""
	Increase the volume gradually from `start_volume` until `end_volume`, taking `duration` seconds to do so.

	Arguments:
		start_volume (float): The volume to start at.
		end_volume (float): The volume to end at.
		duration (int): The number of seconds to take to transition from `start_volume` until `end_volume`.
	"""
	volume_increments = get_increments(start_volume, end_volume, duration) # Increment once per second
	for vol in volume_increments:
		set_volume(vol)
		sleep(1)
