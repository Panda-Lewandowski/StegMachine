from PIL import Image
from math import sqrt



def rs_test(img, m=2, n=2):
    height, width = img.size

    mask = [[], []]

    for i in range(n):
        for j in range(m):
            if ((j % 2) == 0 and (i % 2) == 0) or ((j % 2) == 1 and (i % 2) == 1):
                mask[0].append(1)
                mask[1].append(0)
            else:
                mask[0].append(0)
                mask[1].append(1)

    mask_size_x = m
    mask_size_y = n

    r, g, b = img.split()

    average_overlapping_value = (analyze(r.load(), True, mask, mask_size_x, mask_size_y, height, width) + \
                                 analyze(g.load(), True, mask, mask_size_x, mask_size_y, height, width) + \
                                 analyze(b.load(), True, mask, mask_size_x, mask_size_y, height, width)) / 3

    average_nonoverlapping_value = (analyze(r.load(), False, mask, mask_size_x, mask_size_y, height, width) + \
                                    analyze(g.load(), False, mask, mask_size_x, mask_size_y, height, width) + \
                                    analyze(b.load(), False, mask, mask_size_x, mask_size_y, height, width)) / 3
    
    return (average_nonoverlapping_value + average_overlapping_value) / 2


def analyze(channel, overlap, mask, mask_x, mask_y, h, w):
    startx = 0
    starty = 0
    block = [0]*mask_x*mask_y
    regular = 0
    singular = 0
    negregular = 0
    negsingular = 0
    unusable = 0
    negunusable = 0

    while startx < w and starty < h:
        for m in [0, 1]:
            l = 0
            for i in range(0, mask_y):
                for j in range(0, mask_x):
                    block[l] = channel[startx + j, starty + i]
                    l += 1

            variation_B = get_variation(block)

            block = flip_block(block, mask[m])
            variation_P = get_variation(block)

            block = flip_block(block, mask[m])

            mask[m] = invert_mask(mask[m])
            variation_N = get_negative_variation(block, mask[m])
            mask[m] = invert_mask(mask[m])

            if variation_P > variation_B:
                regular += 1
            if variation_P < variation_B:
                singular += 1
            if variation_P == variation_B:
                unusable += 1

            if variation_N > variation_B:
                negregular += 1
            if variation_N < variation_B:
                negsingular += 1
            if variation_N == variation_B:
                negunusable += 1

        if overlap:
            startx += 1
        else:
            startx += mask_x

        if startx >= (w - 1):
            startx = 0
            if overlap:
                starty += 1
            else:
                starty += mask_y

        if starty >= (h - 1):
            break

    allpixels = get_all_pixel_flips(channel, overlap, mask, mask_x, mask_y, h, w)

    x = get_x(regular, negregular, allpixels[0], allpixels[2],
              singular, negsingular, allpixels[1], allpixels[3])

    if 2 * (x - 1) == 0:
        epf = 0
    else:
        epf = abs(x / (2 * (x - 1)))

    if x - 0.5 == 0:
        ml = 0
    else:
        ml = abs(x / (x - 0.5))

    # estimatedHiddenMessageLength = (Width * Height * 3) * ml) / 8      
    return ml

def get_variation(block):
    variation = 0
    for i in range(0, len(block), 4):
        variation += abs(block[0 + i] - block[1 + i])
        variation += abs(block[1 + i] - block[3 + i])
        variation += abs(block[3 + i] - block[2 + i])
        variation += abs(block[2 + i] - block[0 + i])

    return variation

def get_negative_variation(block, mask):
    variation = 0
    for i in range(0, len(block), 4):
        val1 = block[0 + i]
        val2 = block[1 + i]

        if mask[0 + i] == -1:
            val1 = invertLSB(val1)
        if mask[1 + i] == -1:
            val2 = invertLSB(val2)
        
        variation += abs(val1 - val2)

        val1 = block[1 + i]
        val2 = block[3 + i]

        if mask[0 + i] == -1:
            val1 = invertLSB(val1)
        if mask[1 + i] == -1:
            val2 = invertLSB(val2)
        
        variation += abs(val1 - val2)

        val1 = block[3 + i]
        val2 = block[2 + i]

        if mask[0 + i] == -1:
            val1 = invertLSB(val1)
        if mask[1 + i] == -1:
            val2 = invertLSB(val2)
        
        variation += abs(val1 - val2)

        val1 = block[2 + i]
        val2 = block[0 + i]

        if mask[0 + i] == -1:
            val1 = invertLSB(val1)
        if mask[1 + i] == -1:
            val2 = invertLSB(val2)
        
        variation += abs(val1 - val2)

    return variation

def flip_block(block, mask):
    for i in range(len(block)):
        if mask[i] == 1:
            block[i] = negateLSB(block[i])
        elif mask[i] == -1:
            block[i] = invertLSB(block[i])
    return block


def invert_mask(mask):
    return list(map(lambda x: -x, mask))


def invertLSB(x):
    if x == 255:
        return 256
    if x == 256:
        return 255
    return (negateLSB(x + 1) - 1)

def negateLSB(x):
    tmp = x & 0xfe
    if tmp == x:
        return x | 0x1
    else:
        return tmp

def get_all_pixel_flips(channel, overlap, mask, mask_x, mask_y, h, w):
    all_mask = [1]*mask_x*mask_y

    startx = 0
    starty = 0
    block = [0]*mask_x*mask_y
    regular = 0
    singular = 0
    negregular = 0
    negsingular = 0
    unusable = 0
    negunusable = 0

    while startx < w and starty < h:
        for m in [0, 1]:
            l = 0
            for i in range(0, mask_y):
                for j in range(0, mask_x):
                    block[l] = channel[startx + j, starty + i]
                    l += 1

            block = flip_block(block, all_mask)
            variation_B = get_variation(block)

            block = flip_block(block, mask[m])
            variation_P = get_variation(block)

            block = flip_block(block, mask[m])

            mask[m] = invert_mask(mask[m])
            variation_N = get_negative_variation(block, mask[m])
            mask[m] = invert_mask(mask[m])

            if variation_P > variation_B:
                regular += 1
            if variation_P < variation_B:
                singular += 1
            if variation_P == variation_B:
                unusable += 1

            if variation_N > variation_B:
                negregular += 1
            if variation_N < variation_B:
                negsingular += 1
            if variation_N == variation_B:
                negunusable += 1

        if overlap:
            startx += 1
        else:
            startx += mask_x

        if startx >= (w - 1):
            startx = 0
            if overlap:
                starty += 1
            else:
                starty += mask_y

        if starty >= (h - 1):
            break

    return regular, singular, negregular, negsingular

def get_x(r, rm, r1, rm1, s, sm, s1, sm1):
    x = 0
    dzero = r - s 
    dminuszero = rm - sm
    done = r1 - s1
    dminusone = rm1 - sm1

    a = 2 * (done + dzero)
    b = dminuszero - dminusone - done - (3 * dzero)
    c = dzero - dminuszero

    if a == 0:
        x = c / b

    discriminant = b**2 - (4 * a * c)

    if discriminant >= 0:
        rootpos = ((-1 * b) + sqrt(discriminant)) / (2 * a)
        rootneg = ((-1 * b) - sqrt(discriminant)) / (2 * a)

        if abs(rootpos) <= abs(rootneg):
            x = rootpos
        else:
            x = rootneg
    else:
        cr = (rm - r) / (r1 - r + rm - rm1)
        cs = (sm - s) / (s1 - s + sm - sm1)
        x = (cr + cs) / 2

    if x == 0:
        a_r = ((rm1 - r1 + r - rm) + (rm - r) / x) / (x - 1)
        a_s = ((sm1 - s1 + s - sm) + (sm - s) / x) / (x - 1)

        if a_s > 0 or a_r < 0:
            cr = (rm - r) / (r1 - r + rm - rm1)
            cs = (sm - s) / (s1 - s + sm - sm1)
            x = (cr + cs) / 2

    return x

if __name__ == "__main__":
    img = Image.open("pure.png")
    print(rs_test(img))
