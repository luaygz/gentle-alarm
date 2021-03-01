import argparse

from music import MusicPlayer
from utils import wait_until
from utils import is_valid_dir
from utils import is_valid_time
from utils import is_valid_duration
from utils import is_valid_end_volume
from utils import is_valid_start_volume

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='An alarm clock that gradually increases in volume to wake you up gently.')
	parser.add_argument("time", type=is_valid_time,
						help="When to ring the alarm, in either 12:00 or 24:00 format e.g. 8:30, 13:00, 11:00am, 5:30pm.")
	parser.add_argument("song_dirs", nargs='+', type=is_valid_dir,
						help="One or more directory paths that contains your music.")
	parser.add_argument("--start-volume", type=is_valid_start_volume, default=50, 
						help="What volume to start at. A number between 0 and 100. Default is 50.")
	parser.add_argument("--end-volume", type=is_valid_end_volume, default=100, 
						help="What volume to end at. A number between 0 and 100. Must be greater than or equal to the start volume. Default is 100.")
	parser.add_argument("--duration", type=is_valid_duration, default=60, 
						help="How long to take to transition from the start to end volume, in seconds. Default is 60.")
	parser.add_argument("--shuffle", action="store_true",
						help="Whether to shuffle the playlist.")
	args = parser.parse_args()

	if args.start_volume > args.end_volume:
		raise argparse.ArgumentTypeError("The start volume must be less than or equal to the end volume.")
	
	print("Alarm will ring at " + args.time + ".")
	
	wait_until(args.time)
	
	print("Alarm ringing!")

	music_player = MusicPlayer()
	for dir in args.song_dirs:
		music_player.enqueue_dir(dir)

	music_player.play(start_volume=args.start_volume, end_volume=args.end_volume, duration=args.duration, shuffle=args.shuffle)
