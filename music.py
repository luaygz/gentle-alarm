import vlc
import random
from time import sleep

from typing import List

from utils import get_increments

class MusicPlayer:
	"""
	A music player with basic functionality.

	Arguments:
		songs (List[str]): A list of audio file paths that will play.
		loop (bool): Whether to loop the playlist.
		shuffle (bool): Whether to shuffle the playlist.
	"""
	def __init__(self, songs: List[str] = [], loop: bool = True, shuffle: bool = False):
		self.instance = vlc.Instance()
		self.playlist = self.instance.media_list_new()
		self.enqueue(songs, shuffle)
		self.player = self.instance.media_list_player_new()
		self.player.set_media_list(self.playlist)
		if loop:
			self.player.set_playback_mode(vlc.PlaybackMode.loop)

	def enqueue(self, songs: List[str], shuffle: bool = False) -> None:
		"""
		Enqueue a list of songs.

		Arguments:
			songs (List[str]): A list of file paths.
			shuffle (bool): Whether to shuffle the playlist.
		"""
		if shuffle:
			songs = random.sample(songs, len(songs))
		for song in songs:
			self.playlist.add_media(self.instance.media_new(song))

	def play(self, start_volume: int = 50, end_volume: int = 100, duration: int = 60) -> None:
		"""
		Start playing music.

		Gradually increases volume from `start_volume` to `end_volume` over the course of `duration` seconds.

		Arguments:
			start_volume (int): The volume to start at.
			end_volume (int): The volume to end at.
			duration (int): How long to take to transition from the start to end volume.
		"""
		self.player.get_media_player().audio_set_volume(0)
		self.player.play()
		volume_increments = get_increments(start_volume, end_volume, duration) # Increment once per second
		for vol in volume_increments:
			self.player.get_media_player().audio_set_volume(int(vol))
			sleep(1)
		# Wait until done playing
		while not self.player.get_media_player().get_state() == vlc.State.Ended:
			sleep(1)
