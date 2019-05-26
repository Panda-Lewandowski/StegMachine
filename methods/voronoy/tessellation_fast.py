import numpy as np
from multiprocessing import Pool, Process, Manager


def foo_i(data):
    global dt
    dt = data

    
def foo_w(i):
    return np.where(dt == i)


def foo_w2(dt):
    return np.mean(dt)


def initfoo(data):
	global clus
	clus = data


def workerfoo(ind):
	subdists = (clus[:, 0] - ind[0]) ** 2 + (clus[:, 1] - ind[1]) ** 2
	return np.argmin(np.array(subdists))


def tessel_fast(clusters, shape):
	indices = [(i, j) for i in range(shape[0]) for j in range(shape[1])]
	clus = None
	with Pool(initializer=initfoo, initargs=(clusters, )) as P:
		dist = np.array(P.map(workerfoo, indices, chunksize=100))
	dist = dist.reshape(shape[0:2])
	return dist


def averaging_fast(cn, img, dist):
	s = set(dist.flatten())
	with Pool(initializer=foo_i, initargs=(dist,)) as P:
		locs = list(P.map(foo_w, list(set(list(range(cn))) & s), chunksize=50))
		with Pool() as P:
			mnsr = list(P.map(foo_w2, [img[x + (0,)] for x in locs]))
			mnsg = list(P.map(foo_w2, [img[x + (1,)] for x in locs]))
			mnsb = list(P.map(foo_w2, [img[x + (2,)] for x in locs]))
		for i in range(len(locs)):
			img[locs[i] + (0,)] = mnsr[i]
			img[locs[i] + (1,)] = mnsg[i]
			img[locs[i] + (2,)] = mnsb[i]

	return img
	
