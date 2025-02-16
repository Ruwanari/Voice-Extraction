# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:07:00 2019

@author: Ruwanari
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa
import IPython.display as ipd

import librosa.display

audio_path = 'YanaThanaka.mp3'
y , sr = librosa.load(audio_path)



# And compute the spectrogram magnitude and phase
S_full, phase = librosa.magphase(librosa.stft(y))
idx = slice(*librosa.time_to_frames([30, 35], sr=sr))


# We'll compare frames using cosine similarity, and aggregate similar frames
# by taking their (per-frequency) median value.
#
# To avoid being biased by local continuity, we constrain similar frames to be
# separated by at least 2 seconds.
#
# This suppresses sparse/non-repetetitive deviations from the average spectrum,
# and works well to discard vocal elements.

S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))

# The output of the filter shouldn't be greater than the input
# if we assume signals are additive.  Taking the pointwise minimium
# with the input spectrum forces this.
S_filter = np.minimum(S_full, S_filter)
# We can also use a margin to reduce bleed between the vocals and instrumentation masks.
# Note: the margins need not be equal for foreground and background separation
margin_i, margin_v = 2, 10
power = 2

mask_i = librosa.util.softmask(S_filter,
                               margin_i * (S_full - S_filter),
                               power=power)

mask_v = librosa.util.softmask(S_full - S_filter,
                               margin_v * S_filter,
                               power=power)

# Once we have the masks, simply multiply them with the input spectrum
# to separate the components

S_foreground = mask_v * S_full
S_background = mask_i * S_full
D_foreground = S_foreground * phase
y_foreground = librosa.istft(D_foreground)
librosa.output.write_wav('newfile', y_foreground, sr)

'''
audio_path2 = 'newfile'
y2 , sr2 = librosa.load(audio_path2)



# And compute the spectrogram magnitude and phase
S_full2, phase2 = librosa.magphase(librosa.stft(y2))
idx2 = slice(*librosa.time_to_frames([30, 35], sr=sr2))


# We'll compare frames using cosine similarity, and aggregate similar frames
# by taking their (per-frequency) median value.
#
# To avoid being biased by local continuity, we constrain similar frames to be
# separated by at least 2 seconds.
#
# This suppresses sparse/non-repetetitive deviations from the average spectrum,
# and works well to discard vocal elements.

S_filter2 = librosa.decompose.nn_filter(S_full2,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr2)))

# The output of the filter shouldn't be greater than the input
# if we assume signals are additive.  Taking the pointwise minimium
# with the input spectrum forces this.
S_filter2 = np.minimum(S_full2, S_filter2)
# We can also use a margin to reduce bleed between the vocals and instrumentation masks.
# Note: the margins need not be equal for foreground and background separation
margin_i2, margin_v2 = 2, 10
power2 = 2

mask_i2 = librosa.util.softmask(S_filter2,
                               margin_i * (S_full2 - S_filter2),
                               power=power2)

mask_v2 = librosa.util.softmask(S_full2 - S_filter2,
                               margin_v2 * S_filter2,
                               power=power2)

# Once we have the masks, simply multiply them with the input spectrum
# to separate the components

S_foreground2 = mask_v2 * S_full2
S_background2 = mask_i2 * S_full2
D_foreground2 = S_foreground2 * phase2
y_foreground2 = librosa.istft(D_foreground2)
librosa.output.write_wav('newfile2', y_foreground2, sr2)
'''
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(S_full[:, idx], ref=np.max),
                         y_axis='log', sr=sr)
plt.title('Full spectrum')
plt.colorbar()

plt.subplot(3, 1, 2)
librosa.display.specshow(librosa.amplitude_to_db(S_background[:, idx], ref=np.max),
                         y_axis='log', sr=sr)
plt.title('Background')
plt.colorbar()
plt.subplot(3, 1, 3)
librosa.display.specshow(librosa.amplitude_to_db(S_foreground[:, idx], ref=np.max),
                         y_axis='log', x_axis='time', sr=sr)
plt.title('Foreground')
plt.colorbar()
plt.tight_layout()
plt.show()
