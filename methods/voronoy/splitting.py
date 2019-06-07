from PIL import Image, ImageDraw
from math import sqrt, ceil, floor
import numpy as np


def is_point_in_box(point, box):
	"""Checks if a point belongs to box
	
	:param point: point (x, y)
	:type point: tuple
	:param box: box (x, y, x + width, y + height)
	:type box: tuple
	:return: True or False
	:rtype: boolean
	"""
	return  point[0] > box[0] + 1 and point[0] < box[2] - 1  \
		 and point[1] > box[1] + 1 and point[1] < box[3] - 1


def get_scheme_of_splitting(n):
	"""Calculates the optimal number of boxes on each side
	
	:param n: minimum number of boxes
	:type n: int
	:return: number of boxes in x and number of boxes in y
	:rtype: tuple
	"""
	sqrt_n = sqrt(n)
	if sqrt_n % 1: # not square
		a = floor(sqrt_n)
		b = ceil(sqrt_n)
		if n < (a ** 2 + (b ** 2 - a ** 2) / 2):
			return a + 1, a
		else:
			return a + 2, a
	else:
		sqrt_n = int(sqrt_n)
		return sqrt_n, sqrt_n
		

def split_to_workspace(img_size, n): 
	"""Splits the image plane into workspaces and windows
	
	:param img_size: image size
	:type img_size: tuple
	:param n:  minimum number of workspace
	:type n: int
	:return: list of workspaces and list of windows
	:rtype: tuple
	"""
	w, h = img_size
	w_n, h_n = get_scheme_of_splitting(n)
	w_step = w // w_n
	h_step = h // h_n 
	w_step_z = w_step // 4
	h_step_z = h_step // 4
	boxes = []
	mini_boxes = []
	for i in range(0, h, h_step):
		for j in range(0, w, w_step):
			if j + w_step <= w and i + h_step <= h:
				boxes.append((j, i, j+w_step, i+h_step))
				mini_boxes.append((j + w_step_z, i + h_step_z, 
					j + w_step - w_step_z, i + h_step - h_step_z))
	return boxes, mini_boxes


def get_clusters_points_in_box(clusters, box):
	"""Returns a list of points that belong to the box
	
	:param clusters: list of all points 
	:type clusters: list
	:param box: points of box
	:type box: tuple
	:return: list of points in the box
	:rtype: list
	"""
	return [tuple(point) for point in clusters if is_point_in_box(point, box)]


def get_rescale_clusters(clusters, new_zero):
	"""Rescales points in box coordinates
	
	:param clusters: list of points 
	:type clusters: list
	:param new_zero: upper left corner of the box
	:type new_zero: tuple
	:return:  list of rescaled points 
	:rtype: list
	"""
	return [(point[0] - new_zero[0], point[1] - new_zero[1]) for point in clusters]


def get_rescale_box(box, new_zero):
	return box[0] - new_zero[0], box[1] - new_zero[1], \
		   box[2] - new_zero[0], box[3] - new_zero[1]


if __name__ == "__main__":
	img = Image.open('test.jpg')
	b, m = split_to_workspace(img.size, 27)
	img = np.array(img)
	cn = 2000
	clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[0], np.random.rand(cn) * img.shape[1])))
	# img = Image.fromarray(img_fast)
	
	draw = ImageDraw.Draw(img)
	for box in b:
		draw.rectangle(box)
	
	for mbox in m:
		draw.rectangle(mbox)

	# img.save("test2.png")
	
	# draw.point(clusters.flatten(), fill=(0,0,0))
	img.save("test_rect.png")
	for box in b:
		draw.point(get_clusters_points_in_box(clusters, box), fill=(255, 0, 0))
	
	for mbox in m:
		draw.point(get_clusters_points_in_box(clusters, mbox), fill=(0, 0, 255))

	img.save("test_points.png")
	k = 0 
	for box in b:
		img_box = img.crop(box)
		draw_box = ImageDraw.Draw(img_box)
		points = get_clusters_points_in_box(clusters, box)
		draw_box.point(get_rescale_clusters(points, box[:2]), fill=(255, 255, 0))
		img_box.save(f"test/{k}.png")
		k += 1



