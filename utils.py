import os
from time import sleep
from datetime import datetime

from typing import List, Tuple

def get_songs(song_dirs: List[str]) -> List[str]:
	"""
	Get the list of songs to play.

	Returns:
		A list of song paths.
	"""	
	songs = []
	for song_dir in song_dirs:
		for dir, _, filenames in os.walk(song_dir):
			for filename in filenames:
				filepath = os.path.join(dir, filename)
				if filepath.endswith(".mp3") or filepath.endswith(".flac"):
					songs.append(filepath)
	return songs

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

def validate_input(time: str, song_dirs: str, start_volume: float, end_volume: float, duration: int) -> None:
	"""Validate input."""
	assert parse_time(time), "Time is invalid."
	for song_dir in song_dirs:
		assert os.path.exists(song_dir), "The directory " + song_dir + " does not exist."
	assert start_volume >= 0 and start_volume <= 100, "Start volume should be between 0 and 1."
	assert end_volume >= 0 and end_volume <= 100, "End volume should be between 0 and 1."
	assert start_volume <= end_volume, "Start volume should be less that or equal to end volume."
	assert duration >= 0, "Duration needs to be greater than or equal to zero."