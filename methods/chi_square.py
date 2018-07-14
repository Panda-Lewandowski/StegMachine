from scipy import stats
from PIL import Image

def chi_squared_test(channel):
    #logging.info('Calculating colors for '+ img.filename +' ...')
    hist = calc_colors(channel)

    expected_freq, observed_freq = calc_freq(hist)

    chis, probs = stats.chisquare(observed_freq, expected_freq)
      
    return chis, probs

def calc_colors(channel):
    hist = channel.histogram()
    hist = list(map(lambda x: 1 if x == 0 else x, hist)) 
    return hist

def calc_freq(histogram):
    expected = []
    observed = []
    for k in range(0, len(histogram) // 2):
        expected.append(((histogram[2 * k] + histogram[2 * k + 1]) / 2))
        observed.append(histogram[2 * k])

    return expected, observed

if __name__ == "__main__":
    img = Image.open("test4.png")
    print(chi_squared_test(img))