from PIL import Image, ImageDraw
from scipy.spatial import Voronoi
from matplotlib.path import Path
from functools import reduce
import numpy as np
from multiprocessing import Pool


def get_polygon_color(pol, im):
	centerPoint = (0,0)
	color = []
	count = 0

	for p in pol:
		p = list(p)
		if p[0] >= im.size[0]:
			p[0] = im.size[0] - 1
		
		if p[0] < 0:
			p[0] = 0
			
		if p[1] >= im.size[1]:
			p[1] = im.size[1] - 1

		if  p[1] < 0:
			p[1] = 0

		count += 1
		color.append(im.getpixel(tuple(p)))
		centerPoint = (centerPoint[0]+p[0], centerPoint[1]+p[1])
		
	centerPoint = (centerPoint[0]/count, centerPoint[1]/count)

	color.append(im.getpixel(centerPoint))
	color.append(im.getpixel(centerPoint))
	color.append(im.getpixel(centerPoint))

	div = float(len(color))
	color = reduce(lambda rec, x : ((rec[0]+x[0]), (rec[1]+x[1]), (rec[2]+x[2])), color, (0,0,0))
	color = (color[0]/div, color[1]/div, color[2]/div)
	color = tuple(map(lambda x : int(x), color))

	return color


def voronoi_finite_polygons(vor, radius=None):
	if vor.points.shape[1] != 2:
		raise ValueError("Requires 2D input")

	new_regions = []
	new_vertices = vor.vertices.tolist()

	center = vor.points.mean(axis=0)
	if radius is None:
		radius = vor.points.ptp().max()

	# Construct a map containing all ridges for a given point
	all_ridges = {}
	for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
		all_ridges.setdefault(p1, []).append((p2, v1, v2))
		all_ridges.setdefault(p2, []).append((p1, v1, v2))

	# Reconstruct infinite regions
	for p1, region in enumerate(vor.point_region):
		vertices = vor.regions[region]

		if all(v >= 0 for v in vertices):
			# finite region
			new_regions.append(vertices)
			continue

		# reconstruct a non-finite region
		ridges = all_ridges[p1]
		new_region = [v for v in vertices if v >= 0]

		for p2, v1, v2 in ridges:
			if v2 < 0:
				v1, v2 = v2, v1
			if v1 >= 0:
				# finite ridge: already in the region
				continue

			# Compute the missing endpoint of an infinite ridge

			t = vor.points[p2] - vor.points[p1] # tangent
			t /= np.linalg.norm(t)
			n = np.array([-t[1], t[0]])  # normal

			midpoint = vor.points[[p1, p2]].mean(axis=0)
			direction = np.sign(np.dot(midpoint - center, n)) * n
			far_point = vor.vertices[v2] + direction * radius

			new_region.append(len(new_vertices))
			new_vertices.append(far_point.tolist())

		# sort region counterclockwise
		vs = np.asarray([new_vertices[v] for v in new_region])
		c = vs.mean(axis=0)
		angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
		new_region = np.array(new_region)[np.argsort(angles)]

		new_regions.append(new_region.tolist())

	return new_regions, np.asarray(new_vertices)


def draw_polygon(region, vertices, img_copy, draw):
	polygon = [tuple(vertices[i]) for i in region]
	if polygon:
		color = get_polygon_color(polygon, img_copy)
		draw.polygon(polygon, fill=color)


def colorized_voronoi(voronoi, img):
	img_copy = img.copy()
	draw = ImageDraw.Draw(img_copy) 
	regions, vertices = voronoi_finite_polygons(voronoi)
	for region in regions:
		draw_polygon(region, vertices, img_copy, draw)
	return img_copy


# def colorized_voronoi_fast(voronoi, img):
# 	img_copy = img.copy()
# 	draw = ImageDraw.Draw(img_copy) 
# 	pool = Pool()
# 	regions, vertices = voronoi_finite_polygons(voronoi)
# 	iter_args = [(region, vertices, img_copy, draw) for region in regions]
# 	pool.starmap(draw_polygon, iter_args)
# 	return img_copy


if __name__ == "__main__":
	img = Image.open("test.jpg")
	draw = ImageDraw.Draw(img) 
	cn = 100
	clusters = np.array(tuple(zip(np.random.rand(cn) * img.size[0], 
								  np.random.rand(cn) * img.size[1])))

	clus = clusters.tolist()
	for j in range(len(clus)):
 		clus[j] = tuple(clus[j])
	
	vor = Voronoi(clusters)
	# regions, vertices = voronoi_finite_polygons(vor)
	for region in vor.regions:
		if not -1 in region:
			polygon = [tuple(vor.vertices[i]) for i in region]
			if polygon:
				# color = get_polygon_color(polygon, img)
				draw.polygon(polygon) 
	img.show()

