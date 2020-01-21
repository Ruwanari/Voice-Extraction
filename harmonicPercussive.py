# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:26:56 2019

@author: Ruwanari
"""
import librosa
import numpy as np
import librosa.display

audio_path = 'Buddanubawena.mp3'

y, sr = librosa.load(audio_path)
D = librosa.stft(y)
H, P = librosa.decompose.hpss(D)
import matplotlib.pyplot as plt

plt.figure()
plt.subplot(3, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D),
                                                 ref=np.max),
                         y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Full power spectrogram')
plt.subplot(3, 1, 2)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(H),
                                                 ref=np.max),
                        y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Harmonic power spectrogram')
plt.subplot(3, 1, 3)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(P),
                                                 ref=np.max),
                         y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Percussive power spectrogram')
plt.tight_layout()
plt.show()
'''
harmonic = librosa.istft(H)
percussive = librosa.istft(P)

librosa.output.write_wav('nadeeGangapercussive.mp3', percussive, sr)

librosa.output.write_wav('hp6.wav',harmonic,sr)

from pydub import AudioSegment
sound = AudioSegment.from_mp3("hp1")
sound.export("hp1.wav", format="wav")

'''
