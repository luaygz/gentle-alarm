import os
import sys
import argparse
from random import shuffle

from typing import List

from rhythmbox import *
from utils import *


def get_songs() -> List[str]:
	"""
	Get the list of songs to play.

	Implement this yourself.

	Returns:
		A list of song paths.
	"""	
	all_songs = []
	for dir, _, filenames in os.walk("/mnt/HDD/Music"):
		for filename in filenames:
			filepath = os.path.join(dir, filename)
			if filepath.endswith(".mp3") or filepath.endswith(".flac"):
				all_songs.append(filepath)

	taylor_swift_songs = [song for song in all_songs if "Taylor Swift" in song]
	shuffle(taylor_swift_songs)

	return taylor_swift_songs

def validate_input(time: str, start_volume: float, end_volume: float, duration: int) -> None:
	valid_time_regex = re.compile("^([0-1]?[0-9]|2[0-4]):[0-5][0-9]$")
	is_valid_time = True if valid_time_regex.match(time) else False
	assert is_valid_time, "Time is invalid."
	assert start_volume >= 0.0 and start_volume <= 1.0, "Start volume should be between 0 and 1."
	assert end_volume >= 0.0 and end_volume <= 1.0, "End volume should be between 0 and 1."
	assert start_volume <= end_volume, "Start volume should be less that or equal to end volume."
	assert duration >= 0, "Duration needs to be greater than or equal to zero."

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='An alarm clock that interfaces with Rhythmbox to play music.')
	parser.add_argument("time", type=str,
						help="When to ring the alarm. Must be in 24:00 hour format e.g. 8:00, 13:30.")
	parser.add_argument("--start-volume", type=float, default=0.5, 
						help="What volume to start at. A number between 0.0 and 1.0.")
	parser.add_argument("--end-volume", type=float, default=1.0, 
						help="What volume to end at. A number between 0.0 and 1.0. Must be greater than or equal to the start volume.")
	parser.add_argument("--duration", type=int, default=60, 
						help="How long to take to transition from the start to end volume, in seconds.")
	args = parser.parse_args()

	validate_input(args.time, args.start_volume, args.end_volume, args.duration)

	# Reset
	stop()
	set_volume(0.0)
	clear_queue()

	print("Alarm will ring at " + args.time + ".")
	wait_until(args.time)
	print("Alarm activated!")

	songs = get_songs()
	enqueue_batch(songs)
	play()
	increase_volume_gradually(args.start_volume, args.end_volume, args.duration)
	