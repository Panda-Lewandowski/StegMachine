import numpy as np
import random
from PIL import Image

from splitting import split_to_workspace, get_clusters_points_in_box, get_rescale_clusters
from tessellation_fast import averaging_fast, tessel_fast
from tessellation_low import averaging_low, tessel_low_mem
from hashing import get_comparable_hash


def extract(img, z, n, l=8):
	size = img.size
	_, windows = split_to_workspace(size, n, z)
	msg = b""
	for win in windows:
		win = img.crop(win)
		win = np.array(win)
		bin = get_comparable_hash(win)[:l]
		msg += int(bin, 2).to_bytes(1, byteorder='big')

	return msg
		


if __name__ == '__main__':
	img_origin = Image.open("photo.jpg")
	size = img_origin.size
	img = np.array(img_origin)
	z = 50 # вычислять 
	n = 25
	# extract(img_origin, z, n)

	# np.random.seed(int(args.seed))

	# cn = int(0.1 * np.min(img.shape))
	# print(np.min(img.shape))
	cn = 5000 # необходимо вычислять примерно одна точка на 100 пикселей 
	# clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[0], np.random.rand(cn) * img.shape[1])))
	# dist_fast = tessel_fast(clusters, img.shape)
	# img_fast = averaging_fast(cn, img, dist_fast)

	# b, m = split_to_workspace(size, n, z)
	# img = Image.fromarray(img_fast)
	# sim1 = img.crop(b[0])
	
	# img.crop(m[15])

	# points_in_box = get_clusters_points_in_box(clusters, b[0])
	# points_in_win = get_clusters_points_in_box(clusters, m[0])
	# point_to_swap = random.choice(points_in_win)
	# point_to_swap_new = (point_to_swap[0] + random.randint(-z/10, z/10), 
	# 				 point_to_swap[1] + random.randint(-z/10, z/10))
	# pixels = sim1.load()
	# for p in get_rescale_clusters(points_in_box, b[15][:2]):
	# 	pixels[int(p[0]), int(p[1])] = (0, 0, 0)
	# sim1.show()
	

	# points_in_box.remove(point_to_swap)
	# points_in_box.append(point_to_swap_new)
	# points_in_box = get_rescale_clusters(points_in_box, b[15][:2]) # FIXME
	

	# sim2 = np.array(img_origin.crop(b[0]))
	# cluster_sim2 = np.array(points_in_box) 
	# dist_sim2 = tessel_fast(cluster_sim2, sim2.shape)

	# sim2_fast = averaging_fast(len(cluster_sim2), sim2, dist_sim2)
	# sim2 = Image.fromarray(sim2_fast)
	# sim2.save("test/sim2.png")


	# sim1.save("test/sim1.png")
	
	# img_low = averaging_low(cn, img, dist_fast)

	# img_fast = Image.fromarray(img_fast)
	# img_fast.show()
	# img_fast.save("fast.jpg")
	# img_low = Image.fromarray(img_low)
	# img_low.save("low.jpg")
