from PIL import Image
from math import sqrt, ceil
import numpy as np


def is_point_in_box(point, box):
	return  point[0] > box[0] and point[0] < box[2] \
		 and point[1] > box[1] and point[1] < box[3]
		

def split_to_workspace(img_size, n, z):
	a, b = img_size
	x = sqrt(a * b / n)
	w_x, h_x = int(a / ceil(a / x)), int(b / ceil(b / x))
	boxes = []
	mini_boxes = []
	for i in range(0, b, h_x):
		for j in range(0, a, w_x):
			boxes.append((j, i, j + w_x, i + h_x))
			mini_boxes.append((j + z, i + z, j + w_x - z, i + h_x - z))
	return boxes, mini_boxes


def get_clusters_points_in_box(clusters, box):
	return [tuple(point) for point in clusters if is_point_in_box(point, box)]


def get_rescale_clusters(clusters, new_zero):
	return [(point[0]-new_zero[0], point[1]-new_zero[1]) for point in clusters]

if __name__ == "__main__":
	# img = Image.open('fast.jpg')
	# b, m = split_to_workspace(img, 25, 20)
	# k = 0
	# for i in b:
	#     img.crop(i).save(f"test/{k}.png")
	#     k += 1
	img = Image.open("photo.jpg")
	b, m = split_to_workspace(img.size, 25, 50)
	img = np.array(img)
	cn = 5000 
	clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[0], np.random.rand(cn) * img.shape[1])))
	print(get_clusters_points_in_box(clusters, m[15]))
