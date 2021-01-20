import vlc
import random
import numpy as np
from time import sleep
from threading import Thread

from typing import List

from utils import get_songs

class MusicPlayer:
	"""A music player with basic functionality."""
	def __init__(self):
		self.instance = vlc.Instance()
		self.playlist = self.instance.media_list_new()
		self.player = self.instance.media_list_player_new()
		self.player.set_media_list(self.playlist)

	def enqueue(self, song: str) -> None:
		"""
		Enqueue a song.

		Arguments:
			song (str): A song file path.
		"""
		self.playlist.add_media(self.instance.media_new(song))

	def enqueue_list(self, songs: List[str]) -> None:
		"""
		Enqueue a list of songs.

		Arguments:
			songs (List[str]): A list of song file paths.
		"""
		for song in songs:
			self.enqueue(song)

	def enqueue_from_path(self, songs_dir: str) -> None:
		songs = get_songs(songs_dir)
		self.enqueue_list(songs)

	def set_volume(self, volume: int) -> None:
		"""Set music volume"""
		self.player.get_media_player().audio_set_volume(volume)

	def gradually_increase_volume(self, start_volume: int, end_volume: int, duration: int) -> None:
		"""
		Gradually increase volume from `start_volume` to `end_volume` over the course of `duration` seconds.

		Arguments:
			start_volume (int): The volume to start at.
			end_volume (int): The volume to end at.
			duration (int): How long to take to transition from the start to end volume.
		"""
		# Generate n equally spaced increments between `start_volume` and `end_volume`, not inclusive of `end_volume`
		# e.g. start_volume = 0, end_volume = 100, n = 10 => [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
		volume_increments = np.linspace(start_volume, end_volume, duration+1).tolist()[:-1] # One increment per second
		for vol in volume_increments:
			self.set_volume(int(vol))
			sleep(1)
		self.set_volume(int(end_volume))

	def wait_until_done_playing(self) -> None:
		"""Waits until playback finishes."""
		while not self.player.get_media_player().get_state() == vlc.State.Ended:
			sleep(1)

	def play(self, start_volume: int = 100, end_volume: int = 100, duration: int = 60, shuffle: bool = False, loop: bool = True) -> None:
		"""
		Start playing music.

		Gradually increases volume from `start_volume` to `end_volume` over the course of `duration` seconds.

		Arguments:
			start_volume (int): The volume to start at.
			end_volume (int): The volume to end at.
			duration (int): How long to take to transition from the start to end volume.
			shuffle (bool): Whether to play random songs. Will run indefinitely if true, else will loop the playlist if loop is true.
			loop (bool): Whether to loop the playlist. Only applies if shuffle=False.
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
