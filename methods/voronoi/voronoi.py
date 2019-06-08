import numpy as np
import random
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi

from splitting import split_to_workspace, get_clusters_points_in_box, \
					  get_rescale_clusters, get_rescale_box, get_unrescale_clusters
from hashing import get_comparable_hash, get_md5_hash
from averaging import colorized_voronoi


class StegoVoronoi:
	def __init__(self, cn=10000, delta=10, seed=None):
		self.cn = cn
		self.delta = delta
		if seed:
			np.random.seed(seed)
	
	def embed(self, msg, img, l=8):
		size = img.size
		clusters = np.array(tuple(zip(np.random.rand(self.cn) * size[0], 
								  np.random.rand(self.cn) * size[1])))
		new_cluster = []
		boxes, mini_boxes = split_to_workspace(size, len(msg))
		print(len(msg),len(boxes))
		for i in range(len(boxes)):
			piece = img.crop(boxes[i])
			points_in_piece = get_clusters_points_in_box(clusters, boxes[i])
			points_in_piece = get_rescale_clusters(points_in_piece, boxes[i][:2])
			vor_piece = Voronoi(points_in_piece)

			char = msg[i]
			points_in_win = get_clusters_points_in_box(clusters, mini_boxes[i])
			points_in_win = get_rescale_clusters(points_in_win, boxes[i][:2])

			point_to_swap = random.choice(points_in_win)
			point_to_swap_new = (point_to_swap[0] + random.randint(-self.delta, self.delta), 
							point_to_swap[1] + random.randint(-self.delta, self.delta))
			points_in_piece.remove(point_to_swap)
			points_in_piece.append(point_to_swap_new)
			vor_piece_new = Voronoi(points_in_piece)
			colorized_piece = colorized_voronoi(vor_piece_new, piece)
			to_crop = get_rescale_box(mini_boxes[i], boxes[i][:2])
			hash = get_md5_hash(np.array(colorized_piece.crop(to_crop)))

			while hash[0] != char:
				points_in_piece.append(point_to_swap)
				points_in_piece.remove(point_to_swap_new)
				point_to_swap = random.choice(points_in_win)
				point_to_swap_new = (point_to_swap[0] + random.randint(-10, 10), 
								point_to_swap[1] + random.randint(-10, 10))
				points_in_piece.remove(point_to_swap)
				points_in_piece.append(point_to_swap_new)
				vor_piece_new = Voronoi(points_in_piece)
				colorized_piece = colorized_voronoi(vor_piece_new, piece) 
				to_crop = get_rescale_box(mini_boxes[i], boxes[i][:2])
				hash = get_md5_hash(np.array(colorized_piece.crop(to_crop)))
			
			new_cluster.extend(get_unrescale_clusters(points_in_piece, boxes[i][:2]))

		vor_main = Voronoi(new_cluster)
		stego = colorized_voronoi(vor_main, img)
		return stego


	def extract(self, img, n, l=8):
		size = img.size
		_, windows = split_to_workspace(size, n)
		msg = b""
		for win in windows:
			win = img.crop(win)
			win = np.array(win)
			msg += get_md5_hash(win)[:1]

		return msg
		

if __name__ == '__main__':
	img = Image.open("test.jpg")
	msg = b'\xb2\x1a\xe7'
	svor = StegoVoronoi() 
	stego_img = svor.embed(msg, img)
	print(svor.extract(stego_img, len(msg)))


	