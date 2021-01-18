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
	