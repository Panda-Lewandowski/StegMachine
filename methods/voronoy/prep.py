from PIL import Image
from tessellation_fast import tessel_fast, averaging_fast
from tessellation_low import tessel_low_mem, averaging_low
import numpy as np

if __name__ == '__main__':
	img = Image.open("photo.jpg")
	img = np.array(img)

	# np.random.seed(int(args.seed))

	# cn = int(0.1 * np.min(img.shape))
	# print(np.min(img.shape))
	cn = 5000
	clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[0], np.random.rand(cn) * img.shape[1])))
	dist_low = tessel_low_mem(clusters, img.shape)
	dist_fast = tessel_fast(clusters, img.shape)

	img_fast = averaging_fast(cn, img, dist_fast)
	img_low = averaging_low(cn, img, dist_fast)

	img_fast = Image.fromarray(img_fast)
	img_fast.save("fast.jpg")
	img_low = Image.fromarray(img_low)
	img_low.save("low.jpg")


