#!/usr/bin/env python3
# coding:UTF-8

""" 
This module contains the required functions to implement 
chi-squared attack.

:author: Pandora Lewandowski 
"""

from scipy import stats
from PIL import Image

def chi_squared_test(channel):
    """Main function for the attack

    Using chi-squared implementation
    from scipy.

    :param channel: Channel for analyzing 

    """
    hist = calc_colors(channel)

    expected_freq, observed_freq = calc_freq(hist)

    chis, probs = stats.chisquare(observed_freq, expected_freq)
      
    return chis, probs

def calc_colors(channel):
    """Prepare color histogram for further calculations"""
    hist = channel.histogram()
    hist = list(map(lambda x: 1 if x == 0 else x, hist)) # to avoid dividing by zero 
    return hist

def calc_freq(histogram):
    """Calculating expacted and observed freqs"""
    expected = []
    observed = []
    for k in range(0, len(histogram) // 2):
        expected.append((histogram[2 * k] + histogram[2 * k + 1]) / 2)
        observed.append(histogram[2 * k])

    return expected, observed

if __name__ == "__main__":
    img = Image.open("test4.png")
    print(chi_squared_test(img))