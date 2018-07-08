from PIL import Image
import numpy 
import random

def get_groups(img, mask, channel='r'):
    grp = []
    m, n = img.size
    if channel == 'r':
        ch = img.split()[0]
    elif channel == 'g':
        ch = img.split()[1]
    elif channel == 'b':
        ch = img.split()[2]
    else:
        ch = None
    if ch:
        pix = ch.load()
        x, y = numpy.abs(mask).shape
        for i in range(m-x):
            for j in range(n-y):
                group = [pix[k, l] for k in range(i, i + x + 1) for l in range(j , j + y + 1)]
                grp.append(group)
    return grp

def smoothness(groups):
    numbers = []
    for g in groups:
        s = 0
        for i in range(len(g) - 1):
            s += numpy.abs(g[i + 1] - g[i])
        numbers.append(s)

    return numbers

def invert_lsb(x):
    return x ^ 1

def not_change(x):
    return x 

def invert_lsb_to_msb(x):
    pass

def flipping(groups, mask):
    for g in groups:
        for i in range(len_grps):
            if mask[i] == 0:
                g[i] = invert_lsb(g[i])
            elif mask[i] == 1:
                g[i] = not_change(g[i])
            
    return groups

def count_groups(groups, flipped_groups):
    not_flipped = smoothness(groups)
    flipped = smoothness(flipped_groups)
    R = 0
    S = 0
    U = 0 
    for i in range(len(not_flipped)):
        if flipped[i] > not_flipped[i]:
            R += 1
        elif flipped[i] < not_flipped[i]:
            S += 1
        else:
            U += 1
    print(U)
    return R, S
            

def rs_method_test(img):
    pass

if __name__ == "__main__":
    img = Image.open("200.png")
    mask = numpy.array( [[1,0],[0,1]] )
    grp = get_groups(img, mask)
    len_grps = len(grp[0])
    flipping_mask = [random.choice([0, 1]) for i in range(len_grps)]
    invert_flipping_mask = [i ^ 1 for i in flipping_mask]
    # print(flipping_mask, invert_flipping_mask)
    grp_r = flipping(grp, flipping_mask)
    grp_s = flipping(grp, invert_flipping_mask)
    print(count_groups(grp, grp_r), count_groups(grp, grp_s))
