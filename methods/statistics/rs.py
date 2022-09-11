from PIL import Image
from math import floor, sqrt

def rs_test(img, bw=2, bh=2, mask=[1, 0, 0, 1]):
    height, width = img.size

    invert_mask = list(map(lambda x: -x, mask))

    blocks_in_row = floor(width / bw)
    blocks_in_col = floor(height / bh)
    r, g, b = img.split()[:3]
    r = r.load()
    g = g.load()
    b = b.load() 

    group_couters = [
		{'R': 0, 'S': 0, 'U': 0, 'mR': 0, 'mS': 0, 'mU': 0, 'iR': 0, 'iS': 0, 'iU': 0, 'imR': 0, 'imS': 0, 'imU': 0},
		{'R': 0, 'S': 0, 'U': 0, 'mR': 0, 'mS': 0, 'mU': 0, 'iR': 0, 'iS': 0, 'iU': 0, 'imR': 0, 'imS': 0, 'imU': 0},
		{'R': 0, 'S': 0, 'U': 0, 'mR': 0, 'mS': 0, 'mU': 0, 'iR': 0, 'iS': 0, 'iU': 0, 'imR': 0, 'imS': 0, 'imU': 0}]


    for y in range(blocks_in_col):
        for x in range(blocks_in_row):
            counter_R = []
            counter_G = []
            counter_B = []
            for v in range(bh): 
                for h in range(bw):
                    counter_R.append(r[y + v, x + h])  # not vice versa?
                    counter_G.append(g[y + v, x + h])
                    counter_B.append(b[y + v, x + h])

            group_couters[0][get_group(counter_R, mask)] += 1
            group_couters[1][get_group(counter_G, mask)] += 1
            group_couters[2][get_group(counter_B, mask)] += 1
            group_couters[0]['m' + get_group(counter_R, invert_mask)] += 1
            group_couters[1]['m' + get_group(counter_G, invert_mask)] += 1
            group_couters[2]['m' + get_group(counter_B, invert_mask)] += 1

            counter_R = lsb_flip(counter_R)
            counter_G = lsb_flip(counter_G)
            counter_B = lsb_flip(counter_B)

            group_couters[0]['i' + get_group(counter_R, mask)] += 1
            group_couters[1]['i' + get_group(counter_G, mask)] += 1
            group_couters[2]['i' + get_group(counter_B, mask)] += 1
            group_couters[0]['im' + get_group(counter_R, invert_mask)] += 1
            group_couters[1]['im' + get_group(counter_G, invert_mask)] += 1
            group_couters[2]['im' + get_group(counter_B, invert_mask)] += 1

    return (solve(group_couters[0]) + solve(group_couters[1]) + solve(group_couters[2])) / 3


def get_group(pix, mask):
    flip_pix = pix[:]

    for i in range(len(mask)):
        if mask[i] == 1:
            flip_pix[i] = flip(pix[i])
        elif mask[i] == -1:
            flip_pix[i] = invert_flip(pix[i])

    d1 = smoothness(pix)
    d2 = smoothness(flip_pix)

    if d1 >  d2: 
        return 'S'
    
    if d1 < d2:
        return 'R'

    return 'U'


def flip(val):
    if val & 1:
        return val - 1

    return val + 1


def invert_flip(val):
    if val & 1:
        return val + 1

    return val - 1


def smoothness(pix):
    s = 0
    for i in range(len(pix) - 1):
        s += abs(pix[i + 1] - pix[i])

    return s


def lsb_flip(pix):
    return list(map(lambda x: x ^ 1, pix))


def solve(groups):
    d0 = groups['R'] - groups['S']
    dm0 = groups['mR'] - groups['mS']
    d1  = groups['iR']  - groups['iS']
    dm1 = groups['imR']  - groups['imS']
    a = 2 * (d1 + d0)
    b = dm0 - dm1 - d1 - d0 * 3
    c = d0 - dm0

    D = b * b - 4 * a * c

    if D < 0:
        return 0 

    b *= -1

    if D == 0:
        return (b / 2 / a) / (b / 2 / a - 0.5)

    D = sqrt(D)

    x1 = (b + D) / 2 / a
    x2 = (b - D) / 2 / a

    if abs(x1) < abs(x2):
        return x1 / (x1 - 0.5)

    return x2 / (x2 - 0.5)

if __name__ == "__main__":
    img = Image.open("pure.png")
    print(rs_test(img))

