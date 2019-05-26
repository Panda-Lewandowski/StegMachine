import numpy as np

def tessel_low_mem(clusters, shape):
    dist = np.zeros(shape[0:2], dtype=np.uint16)  # The 2D cluster membership array (up to 65536 clusters)
    for i in range(1, shape[0] + 1):
        for j in range(1, shape[1] + 1):
            subdists = (clusters[:, 0] - i) ** 2 + (clusters[:, 1] - j) ** 2
            clus = np.argmin(np.array(subdists))
            dist[i - 1, j - 1] = clus  # I can't see why I start i,j from 1, and then subtract 1 at the end.
                # But I am keeping it like this in hope that my past self had some rationale.
    return dist


def averaging_low(cn, img, dist):
	s = set(dist.flatten())
	for i in (set(list(range(cn))) & s):  # To exclude centers without any membership
		indarray = (dist == i)
		img[indarray, 0] = int(np.mean(img[indarray, 0]))  # The vanilla averaging
		img[indarray, 1] = int(np.mean(img[indarray, 1]))
		img[indarray, 2] = int(np.mean(img[indarray, 2]))

	return img
