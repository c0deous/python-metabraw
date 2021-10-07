#!/usr/bin/python3

import subprocess, os, sys, platform
from pathlib import Path, PosixPath

class metadata:
	def parse_extmeta(self):
		metalist = self.extmeta.stdout.split(b'\n')
		clip_metalist_str = []
		ff_metalist_str = []
		# Format raw data into keyval
		ff_indexswitch = False
		for index, i in enumerate(metalist):
			if i == b'' or i == b'Clip Metadata': continue
			if i == b'Frame 0 Metadata': ff_indexswitch = True; continue
			if ff_indexswitch == True:
					ff_metalist_str.append(i.decode('latin1'))
					continue
			clip_metalist_str.append(i.decode('latin1'))

		def pythonic_formatting(keyval):
			integer_valued = ['braw_codec_bitrate', 'multicard_volume_number', 'multicard_volume_count', 'take', 'post_3dlut_embedded_size', 'viewing_bmdgen', '.multicard_timecode', 'as_shot_kelvin', 'as_shot_tint', 'iso', 'white_balance_kelvin', 'white_balance_tint']
			float_valued = ['analog_gain', 'firmware_version', 'tone_curve_contrast', 'tone_curve_saturation', 'tone_curve_highlights', 'tone_curve_shadows', 'tone_curve_video_black_level', 'post_3dlut_embedded_bmd_gamma', 'format_frame_rate', 'exposure', 'shutter_value']
			bool_valued = ['analog_gain_is_constant', 'good_take', 'anamorphic_enable']
			tuple_valued = ['crop_origin', 'crop_size', 'sensor_rate']

			# hacky encoding shitfixes
			if keyval[0] == 'shutter_value': keyval[1] = keyval[1][:-1]
			if keyval[0] == '.multicard_timecode': keyval[0] = keyval[0][1:]
			if platform.system() == 'Windows' and keyval[0] in tuple_valued: keyval[1] = keyval[1][:-1].replace(',', ' ')

			# change types for specific values
			if keyval[1] == None or keyval[1] == '': return keyval
			if keyval[0] in integer_valued: keyval[1] = int(keyval[1])
			if keyval[0] in float_valued: keyval[1] = float(keyval[1])
			if keyval[0] in bool_valued: keyval[1] = bool(keyval[1])
			if keyval[0] in tuple_valued:foo = keyval[1].split(' '); keyval[1] = (foo[0], foo[1])
			return keyval

		# Set Clip metadata
		for index, i in enumerate(clip_metalist_str):
			f = pythonic_formatting(i.split(': '))
			self.clip[f[0]] = f[1]

		# Set First-frame metadata
		for index, i in enumerate(ff_metalist_str):
			f = pythonic_formatting(i.split(': '))
			self.firstframe[f[0]] = f[1]

	def list_clip_keys(self):
		return [*self.clip]

	def list_firstframe_keys(self):
		return [*self.firstframe]

	def __init__(self, filepath, brawsdk_path=None):
		# Locate the BRAW SDK
		self.extmeta_path = ''
		multiplatform = {
		'Darwin': PosixPath('/Applications/Blackmagic RAW/Blackmagic RAW SDK/Mac/'),
		'Windows': Path('C:\\Program Files (x86)\\Blackmagic Design\\Blackmagic RAW\\Win\\'),
		'Linux': PosixPath('/usr/lib64/blackmagic/BlackmagicRAWSDK/Linux/')
		}
		system = platform.system()
		if brawsdk_path:
			user_brawsdk_path = Path(brawsdk_path)
			if not user_brawsdk_path.exists():
				raise IOError('Invalid user-specified BRAW SDK path')
			self.extmeta_path = user_brawsdk_path / 'Samples' / 'ExtractMetadata' / 'ExtractMetadata'
		elif system in [*multiplatform]:
			if not multiplatform[system].exists():
				raise IOError('System-default BRAW SDK not found. Install dependency or specify path by passing brawsdk_path\nEx: /Applications/Blackmagic RAW/Blackmagic RAW SDK/Mac/')
			self.extmeta_path = multiplatform[system] / 'Samples' / 'ExtractMetadata' / 'ExtractMetadata'

		# Check for .braw file legitimacy
		filepath = Path(filepath)
		if not filepath.exists(): raise IOError('Invalid path to .braw file')
		self.filepath = filepath.resolve()


		self.extmeta = subprocess.run([self.extmeta_path.resolve(), str(self.filepath)], cwd=self.extmeta_path.resolve().parent, stdout=subprocess.PIPE)
		self.clip = {}
		self.firstframe = {}
		self.parse_extmeta()
