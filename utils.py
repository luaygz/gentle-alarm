import os
import argparse
from time import sleep
from datetime import datetime

from typing import List, Tuple

def is_song(file: str) -> bool:
	return file.endswith(".mp3") or file.endswith(".flac")

def list_songs(root_dir: str) -> List[str]:
	"""
	Get a list of all songs in a directory recursively.

	Returns:
		A list of song paths.
	"""	
	songs = []
	for dir, _, files in os.walk(root_dir):
		for file in files:
			if is_song(file):
				path = os.path.join(dir, file)
				songs.append(path)
	return songs

def parse_time(time: str) -> Tuple[int, int]:
	"""
	Parse the hour and minute of a time string.
	
	The time string can be either 12:00 or 24:00 hour format. If 12:00 format is used, whether AM or PM must be specified.
		e.g. 8:00, 15:30, 8:00am, 3:30pm.

	Arguments:
		time (str): The time to parse.

	Returns:
		hour (str), minute (str)
	"""
	try:
		if time.lower().endswith(("am", "pm")):
			time_dt = datetime.strptime(time, '%I:%M%p') # 12:00 format
		else:
			time_dt = datetime.strptime(time, '%H:%M') # 24:00 format
		return time_dt.hour, time_dt.minute
	except ValueError:
		return False

def wait_until(time: str) -> None:
	"""
	Wait until the specified time.

	Arguments:
		time (str): What time to wait until.
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
