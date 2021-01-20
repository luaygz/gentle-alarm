import os
import argparse

from typing import List

from utils import validate_input, wait_until
from music import MusicPlayer


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

	return taylor_swift_songs

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='An alarm clock that gradually increases in volume to wake you up gently.')
	parser.add_argument("time", type=str,
						help="When to ring the alarm in either 12:00 or 24:00 format e.g. 8:30, 13:00, 11:00am, 5:30pm.")
	parser.add_argument("--start-volume", type=float, default=50, 
						help="What volume to start at. A number between 0 and 100.")
	parser.add_argument("--end-volume", type=float, default=100, 
						help="What volume to end at. A number between 0 and 100. Must be greater than or equal to the start volume.")
	parser.add_argument("--duration", type=int, default=60, 
						help="How long to take to transition from the start to end volume, in seconds.")
	parser.add_argument("--no-shuffle", action="store_true",
						help="Whether to shuffle the playlist, will shuffle by default if omitted.")
	args = parser.parse_args()

	validate_input(args.time, args.start_volume, args.end_volume, args.duration)
	
	print("Alarm will ring at " + args.time + ".")
	wait_until(args.time)
	print("Alarm activated!")

	songs = get_songs()
	music_player = MusicPlayer(songs, shuffle=not args.no_shuffle)
	music_player.play(args.start_volume, args.end_volume, args.duration)
	music_player.join()
