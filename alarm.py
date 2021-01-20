import os
import argparse

from utils import validate_input, wait_until
from music import MusicPlayer

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='An alarm clock that gradually increases in volume to wake you up gently.')
	parser.add_argument("time", type=str,
						help="When to ring the alarm in either 12:00 or 24:00 format e.g. 8:30, 13:00, 11:00am, 5:30pm.")
	parser.add_argument("songs_dir", type=str,
						help="The directory path that contains your music.")
	parser.add_argument("--start-volume", type=float, default=50, 
						help="What volume to start at. A number between 0 and 100. Default is 50.")
	parser.add_argument("--end-volume", type=float, default=100, 
						help="What volume to end at. A number between 0 and 100. Must be greater than or equal to the start volume. Default is 100.")
	parser.add_argument("--duration", type=int, default=60, 
						help="How long to take to transition from the start to end volume, in seconds. Default is 60.")
	parser.add_argument("--no-shuffle", action="store_true",
						help="Whether to shuffle the playlist, will shuffle by default if omitted.")
	args = parser.parse_args()

	validate_input(args.time, args.songs_dir, args.start_volume, args.end_volume, args.duration)
	
	print("Alarm will ring at " + args.time + ".")
	wait_until(args.time)
	print("Alarm activated!")

	music_player = MusicPlayer()
	music_player.enqueue_from_path(args.songs_dir)
	music_player.play(args.start_volume, args.end_volume, args.duration, shuffle=(not args.no_shuffle))
