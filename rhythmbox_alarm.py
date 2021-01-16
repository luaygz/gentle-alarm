import os
from time import sleep
from random import shuffle

from typing import List

import numpy as np


def get_songs() -> List[str]:
	"""
	Get the list of songs to play.

	Implement this yourself.

	Returns:
		A list of song paths.
	"""
	all_songs = [os.path.join(root, song) for root, _, filenames in os.walk("/mnt/HDD/Music") for song in filenames if song.endswith(".mp3") or song.endswith(".flac")]
	taylor_swift_songs = [song for song in all_songs if "Taylor Swift" in song]
	shuffle(taylor_swift_songs)

	return taylor_swift_songs

def enqueue(file_path: str) -> None:
	"""Enqueue a song."""
	os.system("rhythmbox-client --enqueue \"" + file_path + "\"")

def enqueue_batch(file_paths: List[str]) -> None:
	"""Enqueue a list of songs."""
	for fp in file_paths:
		enqueue(fp)

def clear_queue() -> None:
	"""Clear the song queue"""
	os.system("rhythmbox-client --clear-queue")

def play() -> None:
	"""Start playing music."""
	os.system("rhythmbox-client --play")

def stop() -> None:
	"""Stop playing music."""
	os.system("rhythmbox-client --stop")

def set_volume(level: float) -> None:
	"""
	Set the music volume.

	Arguments:
		level (float): The volume level, a float between 0.0 and 1.0.
	"""
	os.system("rhythmbox-client --set-volume " + str(level))

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
	volume_increments = np.linspace(lower, upper, n).tolist()
	return volume_increments

def increase_volume_gradually(start_volume: float, end_volume: float, duration: int) -> None:
	"""
	Increase the volume slowly from `start_volume` until `end_volume`, taking `duration` seconds to do so.

	Arguments:
		start_volume (float): The volume to start at.
		end_volume (float): The volume to end at.
		duration (int): The number of seconds to take to transition from `start_volume` until `end_volume`.
	"""
	volume_increments = get_increments(start_volume, end_volume, duration) # Increment once per second
	for vol in volume_increments:
		set_volume(vol)
		sleep(1)

# Volume range is 0.0 to 1.0
start_volume = 0.5
end_volume = 1.0
duration = 200 # In seconds, how long it takes to go from `start_volume` to `end_volume`

# Reset
stop()
set_volume(0.0)
clear_queue()

songs = get_songs()
enqueue_batch(songs)
play()
increase_volume_gradually(start_volume, end_volume, duration)