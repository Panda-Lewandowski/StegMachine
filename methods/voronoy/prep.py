import numpy as np
import random
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi

from splitting import split_to_workspace, get_clusters_points_in_box, get_rescale_clusters
from hashing import get_comparable_hash


def extract(img, z, n, l=8):
	size = img.size
	_, windows = split_to_workspace(size, n)
	msg = b""
	for win in windows:
		win = img.crop(win)
		win = np.array(win)
		bin = get_comparable_hash(win)[:l]
		msg += int(bin, 2).to_bytes(1, byteorder='big')

	return msg
		


if __name__ == '__main__':
	img_origin = Image.open("test.jpg")
	size = img_origin.size
	img = np.array(img_origin)
	n = 15

	# np.random.seed(int(args.seed))

	# cn = int(0.1 * np.min(img.shape))
	cn = 2000 # необходимо вычислять примерно одна точка на 100 пикселей 
	clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[1], np.random.rand(cn) * img.shape[0])))
	vor = Voronoi(clusters)

	points = vor.vertices.tolist()
	clus = clusters.tolist()
	draw = ImageDraw.Draw(img_origin)
	for i in range(len(points)):
		points[i] = tuple(points[i])
	for j in range(len(clus)):
		clus[j] = tuple(clus[j])

	
	draw.point(clus, fill=(255, 0, 0))
	for region in vor.regions:
		if not -1 in region:
			polygon = [tuple(vor.vertices[i]) for i in region]
			if polygon:
				draw.polygon(polygon)

	draw.point(points, fill=(0, 0, 255))
	# img_origin.show()
	
	t = 8
	boxes, mini_boxes = split_to_workspace(size, n)
	draw.rectangle(mini_boxes[t])
	img_origin.crop(boxes[t]).save("test/wow1.png")

	piece = Image.open("test.jpg").crop(boxes[t])
	points_in_piece = get_clusters_points_in_box(clusters, boxes[t])
	points_in_piece = get_rescale_clusters(points_in_piece, boxes[t][:2])
	vor_piece = Voronoi(points_in_piece)

	points = vor_piece.vertices.tolist()
	draw_piece = ImageDraw.Draw(piece)
	
	for i in range(len(points)):
		points[i] = tuple(points[i])

	draw_piece.point(points_in_piece, fill=(255, 0, 0))
	draw_piece.rectangle(mini_boxes[t], fill=(0, 255, 255))
	for region in vor_piece.regions:
		if not -1 in region:
			polygon = [tuple(vor_piece.vertices[i]) for i in region]
			if polygon:
				draw_piece.polygon(polygon)

	draw_piece.point(points, fill=(0, 0, 255))
	piece.save("test/wow2.png")

	points_in_win = get_clusters_points_in_box(clusters, mini_boxes[t])
	points_in_win = get_rescale_clusters(points_in_win, boxes[t][:2])
	point_to_swap = random.choice(points_in_win)
	point_to_swap_new = (point_to_swap[0] + random.randint(-10, 10), 
					 point_to_swap[1] + random.randint(-10, 10))
	points_in_piece.remove(point_to_swap)
	points_in_piece.append(point_to_swap_new)
	vor_piece_new = Voronoi(points_in_piece)
	draw_piece_new = ImageDraw.Draw(piece)
	draw_piece_new.point(point_to_swap_new, fill=(0, 255, 255))
	for region in vor_piece_new.regions:
		if not -1 in region:
			polygon = [tuple(vor_piece_new.vertices[i]) for i in region]
			if polygon:
				draw_piece_new.polygon(polygon)
	piece.save("test/wow3.png")

	