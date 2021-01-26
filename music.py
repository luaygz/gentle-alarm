import vlc
import random
import numpy as np
from time import sleep
from threading import Thread

from typing import List

from utils import list_songs

class MusicPlayer:
	"""
	A music player with basic functionality.
	"""
	def __init__(self):
		self.instance = vlc.Instance()
		self.playlist = self.instance.media_list_new()
		self.player = self.instance.media_list_player_new()
		self.player.set_media_list(self.playlist)

	def enqueue(self, song: str) -> None:
		"""
		Enqueue a song.

		Arguments:
			song (str): The song's file path.
		"""
		self.playlist.add_media(self.instance.media_new(song))

	def enqueue_dir(self, dir: str) -> None:
		"""
		Enqueue all the songs in a directory recursively.

		Arguments:
			dir (str): The directory that contains the songs to enqueue.
		"""
		songs = list_songs(dir) # Recursive
		for song in songs:
			self.enqueue(song)

	def set_volume(self, volume: int) -> None:
		"""
		Set music volume.

		Arguments:
			volume (int): The volume to set.
		"""
		self.player.get_media_player().audio_set_volume(volume)

	def gradually_increase_volume(self, start_volume: int, end_volume: int, duration: int) -> None:
		"""
		Gradually increase volume from `start_volume` to `end_volume` over the course of `duration` seconds.

		Arguments:
			start_volume (int): The volume to start at.
			end_volume (int): The volume to end at.
			duration (int): How long to take to transition from the start to end volume.
		"""
		# Generate n+1 points at regular intervals between `start_volume` and `end_volume`, then omit `end_volume`.
		# e.g. start_volume = 0, end_volume = 100, n = 10 => [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
		volume_increments = np.linspace(start_volume, end_volume, duration+1).tolist()[:-1] # One increment per second
		for vol in volume_increments:
			self.set_volume(int(vol))
			sleep(1)
		self.set_volume(int(end_volume))

	def wait_until_done_playing(self) -> None:
		"""
		Wait until playback finishes.
		"""
		while not self.player.get_media_player().get_state() == vlc.State.Ended:
			sleep(1)

	def play(self, start_volume: int = 100, end_volume: int = 100, duration: int = 60, shuffle: bool = False, loop: bool = True) -> None:
		"""
		Start playing music.

		Gradually increases volume from `start_volume` to `end_volume` over the course of `duration` seconds.

		If `shuffle` is true, will run indefinitely. Otherwise will loop the playlist if `loop` is true.

		Arguments:
			start_volume (int): The volume to start at.
			end_volume (int): The volume to end at.
			duration (int): How long to take to transition from the start to end volume in seconds.
			shuffle (bool): Whether to play songs randomly.
			loop (bool): Whether to loop the playlist.
		"""
		self.set_volume(0)
		Thread(target=self.gradually_increase_volume, args=(start_volume, end_volume, duration)).start()
		if shuffle:
			while True:
				i = random.randrange(0, len(self.playlist))
				self.player.play_item_at_index(i)
				self.wait_until_done_playing()
		else:
			if loop:
				self.player.set_playback_mode(vlc.PlaybackMode.loop)
			self.player.play()
			self.wait_until_done_playing()
