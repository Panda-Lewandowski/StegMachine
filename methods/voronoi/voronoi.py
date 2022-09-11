import numpy as np
import random
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi
from multiprocessing import Pool, Process, pool

from splitting import split_to_workspace, get_clusters_points_in_box, \
					  get_rescale_clusters, get_rescale_box, get_unrescale_clusters
from hashing import get_comparable_hash, get_md5_hash
from averaging import colorized_voronoi


class NoDaemonProcess(Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)


class NoDaemonPool(pool.Pool):
    Process = NoDaemonProcess


class StegoVoronoi:
	def __init__(self, cn=10000, delta=10, num_of_proc=2, seed=None):
		self.cn = cn
		self.delta = delta
		self.proc_num = num_of_proc
		if seed:
			np.random.seed(seed)

	@property
	def proc_num(self):
		return self.__proc_num

	@proc_num.setter
	def proc_num(self, num):
		self.__proc_num = num

	def __str__(self):
		return f"Voronoi Stego class with {self.proc_num} process"

	def pick_hash(self, block, clusters, img, box, mini_box):
		piece = img.crop(box)
		points_in_piece = get_clusters_points_in_box(clusters, box)
		points_in_piece = get_rescale_clusters(points_in_piece, box[:2])
		points_in_win = get_clusters_points_in_box(clusters, mini_box)
		points_in_win = get_rescale_clusters(points_in_win, box[:2])

		vor_piece = Voronoi(points_in_piece)

		colorized_piece = colorized_voronoi(vor_piece, piece)
		to_crop = get_rescale_box(mini_box, box[:2])
		hash = get_md5_hash(np.array(colorized_piece.crop(to_crop)))

		while hash[0] != block:
			point_to_swap = random.choice(points_in_win)
			# check that point now in win
			point_to_swap_new = (point_to_swap[0] + random.randint(-self.delta, self.delta), 
								point_to_swap[1] + random.randint(-self.delta, self.delta))
			points_in_piece.remove(point_to_swap)
			points_in_piece.append(point_to_swap_new)
			vor_piece_new = Voronoi(points_in_piece)
			colorized_piece = colorized_voronoi(vor_piece_new, piece) 
			to_crop = get_rescale_box(mini_box, box[:2])
			hash = get_md5_hash(np.array(colorized_piece.crop(to_crop)))
			# print(hash)

			if hash[0] != block:
				points_in_piece.append(point_to_swap)
				points_in_piece.remove(point_to_swap_new)	

		return get_unrescale_clusters(points_in_piece, box[:2])
	
	def embed(self, msg, img, l=8):
		size = img.size
		msg_len = len(msg)
		clusters = np.array(tuple(zip(np.random.rand(self.cn) * size[0], 
								  np.random.rand(self.cn) * size[1])))

		boxes, mini_boxes = split_to_workspace(size, msg_len)
		new_cluster = []


		pool = Pool(self.proc_num)
		iter_args = [(msg[i], clusters, img, boxes[i], mini_boxes[i]) for i in range(msg_len)]
		new_cluster_map = pool.starmap(self.pick_hash, iter_args)
		for new in new_cluster_map:
			new_cluster.extend(new)
		pool.close()
		pool.join()

		vor_main = Voronoi(new_cluster)
		stego = colorized_voronoi(vor_main, img)
		return stego


	def extract(self, img, n, l=8):
		size = img.size
		_, windows = split_to_workspace(size, n)
		windows = [np.array(img.crop(win)) for win in windows]
		pool = Pool(self.proc_num)
		msg = pool.map(get_md5_hash, windows)
		return b"".join([block[:1] for block in msg])


if __name__ == '__main__':
	img = Image.open("test.jpg")
	msg = b'\xb2\x1a\xe7\x04z\xce\x80iv\r\nu\xd4e\xf33'
	# msg = b'\xb2\x1a'
	svor = StegoVoronoi(num_of_proc=3) 
	stego_img = svor.embed(msg[:12], img)
	# stego_img.show()
	# stego_img.save("stego.png")
	print(svor.extract(stego_img, len(msg[:12])))


	