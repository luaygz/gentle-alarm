import os
import argparse
from time import sleep
from datetime import datetime

from typing import List, Tuple

def get_songs(song_dir: str) -> List[str]:
	"""
	Get the list of songs to play.

	Returns:
		A list of song paths.
	"""	
	songs = []
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

def is_valid_time(time: str) -> str:
	if not parse_time(time):
		raise argparse.ArgumentTypeError("{} is an invalid time.".format(time))
	return time

def is_valid_dir(dir: str) -> str:
	if not os.path.exists(dir):
		raise argparse.ArgumentTypeError("The directory {} does not exist.".format(dir))
	return dir

def is_valid_start_volume(start_volume: int) -> int:
	start_volume = int(start_volume)
	if start_volume < 0 or start_volume > 100:
		raise argparse.ArgumentTypeError("The start volume must be between 0 and 100.")
	return start_volume

def is_valid_end_volume(end_volume: int) -> int:
	end_volume = int(end_volume)
	if end_volume < 0 or end_volume > 100:
		raise argparse.ArgumentTypeError("The end volume must be between 0 and 100.")
	return end_volume

def is_valid_duration(duration: int) -> int:
	duration = int(duration)
	if duration < 0:
		raise argparse.ArgumentTypeError("The duration must be zero or more.")
	return duration
