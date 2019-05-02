# -*- coding: utf-8 -*-
"""
Created on Wed May  1 09:25:09 2019

@author: Ruwanari
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd

import librosa.display
audio_path = 'Greshan Ananda - Sihina Ahase.mp3'
y , sr = librosa.load(audio_path)
sound_monoL = librosa.to_mono(y)[0]
sound_monoR = librosa.to_mono(y)[1]

# Invert phase of the Right audio file
sound_monoR_inv = sound_monoR.invert_phase()

# Merge two L and R_inv files, this cancels out the centers
sound_CentersOut = sound_monoL.overlay(sound_monoR_inv)

# Export merged audio file
fh = sound_CentersOut.export(myAudioFile_CentersOut, format="mp3")