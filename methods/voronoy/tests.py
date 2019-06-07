from tessellation_fast import averaging_fast, tessel_fast
from tessellation_low import averaging_low, tessel_low_mem
from message import split_message_to_bits, InvaligBlockLength
from hashing import get_comparable_hash, get_md5_hash, get_sha256_hash
from splitting import is_point_in_box, get_scheme_of_splitting, split_to_workspace, \
	get_clusters_points_in_box, get_rescale_clusters
from PIL import Image
from bitstring import BitArray

import numpy as np
import time
import unittest


class MessageSplittingTestCase(unittest.TestCase):
	def setUp(self):
		self.msg = b'\xb2\x1a\xe7\x04z\xce\x82i\xdc}\xf3\x08\xea\xba\xe1\xf70i4c\xda'
		self.msg_split_default = ['10110010', '00011010', '11100111', '00000100', '01111010', 
					  			  '11001110', '10000010', '01101001', '11011100', '01111101', 
								  '11110011', '00001000', '11101010', '10111010', '11100001', 
								  '11110111', '00110000', '01101001', '00110100', '01100011',
								  '11011010']
		self.msg_split_5 = ['10110', '01000', '01101', '01110', '01110', '00001', 
							'00011', '11010', '11001', '11010', '00001', '00110', 
							'10011', '10111', '00011', '11101', '11110', '01100', 
							'00100', '01110', '10101', '01110', '10111', '00001', 
							'11110', '11100', '11000', '00110', '10010', '01101', 
							'00011', '00011', '11011', '010']

		self.msg_split_6 = ['101100', '100001', '101011', '100111', '000001', 
							'000111', '101011', '001110', '100000', '100110', 
							'100111', '011100', '011111', '011111', '001100', 
							'001000', '111010', '101011', '101011', '100001', 
							'111101', '110011', '000001', '101001', '001101', 
							'000110', '001111', '011010']

	def test_split_default_bit(self):
		split_str = split_message_to_bits(self.msg)
		self.assertEqual(len(split_str), len(self.msg_split_default))
		for i in range(len(split_str)):
			self.assertEqual(split_str[i], self.msg_split_default[i])
			self.assertEqual(len(split_str[i]), 8)

	def test_split_even_bit(self):
		split_str = split_message_to_bits(self.msg, length=5)
		self.assertEqual(len(split_str), len(self.msg_split_5))
		for i in range(len(split_str) - 1):
			self.assertEqual(split_str[i], self.msg_split_5[i])
			self.assertEqual(len(split_str[i]), 5)
		self.assertEqual(split_str[-1], self.msg_split_5[-1])
		self.assertEqual(len(split_str[-1]), 3)
		
	def test_split_odd_bit(self):
		split_str = split_message_to_bits(self.msg, length=6)
		self.assertEqual(len(split_str), len(self.msg_split_6))
		for i in range(len(split_str)):
			self.assertEqual(split_str[i], self.msg_split_6[i])
			self.assertEqual(len(split_str[i]), 6)

	def test_split_more_10(self):
		self.assertRaisesRegex(InvaligBlockLength, 
							   "Length of block must be less than 10!", 
							   split_message_to_bits,
							   self.msg, length=11)


class HashingTestCase(unittest.TestCase):
	def setUp(self):
		self.path_to_img = "test.jpg"
		self.md5_hash = "0a9a5d0b2bf5e3d40718bf5409bcc55a"
		self.sha256_hash = "e71652011b5f196020a2bde0182c994e3aa573eb7cd9934e66aa8603a0bae2b0"
		self.comparable_hash = "f8ffff7300000000"

	def test_md5_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_md5_hash(img)
		self.assertEqual(len(hash), 32)
		self.assertEqual(hash, self.md5_hash)

	def test_sha256_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_sha256_hash(img)
		self.assertEqual(len(hash), 64)
		self.assertEqual(hash, self.sha256_hash)

	def test_comparable_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_comparable_hash(img)
		self.assertEqual(len(hash), 16)
		self.assertEqual(hash, self.comparable_hash)


class SplittingTestCase(unittest.TestCase):
	def setUp(self):
		self.boxes = [(0, 0, 10, 10), (10, 0, 20, 10), (20, 0, 30, 10), 
							 (30, 0, 40, 10), (40, 0, 50, 10), (0, 10, 10, 20), 
							 (10, 10, 20, 20), (20, 10, 30, 20), (30, 10, 40, 20), 
							 (40, 10, 50, 20), (0, 20, 10, 30), (10, 20, 20, 30), 
							 (20, 20, 30, 30), (30, 20, 40, 30), (40, 20, 50, 30), 
							 (0, 30, 10, 40), (10, 30, 20, 40), (20, 30, 30, 40), 
							 (30, 30, 40, 40), (40, 30, 50, 40), (0, 40, 10, 50), 
							 (10, 40, 20, 50), (20, 40, 30, 50), (30, 40, 40, 50), 
							 (40, 40, 50, 50)]
		self.mini_boxes = [(2, 2, 8, 8), (12, 2, 18, 8), (22, 2, 28, 8), 
							 (32, 2, 38, 8), (42, 2, 48, 8), (2, 12, 8, 18), 
							 (12, 12, 18, 18), (22, 12, 28, 18), (32, 12, 38, 18), 
							 (42, 12, 48, 18), (2, 22, 8, 28), (12, 22, 18, 28), 
							 (22, 22, 28, 28), (32, 22, 38, 28), (42, 22, 48, 28), 
							 (2, 32, 8, 38), (12, 32, 18, 38), (22, 32, 28, 38),
							 (32, 32, 38, 38), (42, 32, 48, 38), (2, 42, 8, 48), 
							 (12, 42, 18, 48), (22, 42, 28, 48), (32, 42, 38, 48), 
							 (42, 42, 48, 48)]

		self.clusters = [(3.01234948, 3.65434035),
						(18.95317273, 9.67615443),
						(16.27880307, 21.24067984),
						(32.76976852, 34.90158977),
						(12.81967335, 3.22666219),
						(4.30452246, 33.42122797)]

	def test_point_in_box(self):
		answer = is_point_in_box((2, 2), (0, 0, 10, 10))
		self.assertEqual(answer, True)

	def test_point_not_in_box(self):
		answer = is_point_in_box((12, 12), (0, 0, 5, 5))
		self.assertEqual(answer, False)

	def test_point_on_corner(self):
		answer = is_point_in_box((10, 10), (0, 0, 10, 10))
		self.assertEqual(answer, False)

	def test_point_on_border(self):
		answer = is_point_in_box((0, 5), (0, 0, 10, 10))
		self.assertEqual(answer, False)

	def test_splitting_square(self):
		answer = get_scheme_of_splitting(25)
		self.assertEqual(answer, (5, 5))

	def test_splitting_bottom_half(self):
		answer = get_scheme_of_splitting(27)
		self.assertEqual(answer, (6, 5))

	def test_splitting_top_half(self):
		answer = get_scheme_of_splitting(32)
		self.assertEqual(answer, (7, 5))

	def test_splitting_image_accur(self):
		b, m = split_to_workspace((50, 50), 25)
		self.assertEqual(b, self.boxes)
		self.assertEqual(m, self.mini_boxes)

	def test_splitting_image_not_accur(self):
		b, m = split_to_workspace((52, 50), 25)
		self.assertEqual(b, self.boxes)
		self.assertEqual(m, self.mini_boxes)

	def test_get_points_in_box(self):
		point = get_clusters_points_in_box(self.clusters, self.mini_boxes[0])
		self.assertEqual(point, [(3.01234948, 3.65434035)])

	def test_get_rescale(self):
		point = get_clusters_points_in_box(self.clusters, self.mini_boxes[0])
		self.assertEqual(get_rescale_clusters(point, self.mini_boxes[0]), 
						[(1.0123494800000001, 1.65434035)])


def speed_test():
	img_origin = Image.open("test.jpg")
	size_origin = img_origin.size
	
	cn_origin = 5000
	scaling = [round(x, 2) for x in np.arange(0.1, 1.1, 0.1)]
	with open("test.txt", "w") as file:
		for sc in scaling:
			size = (int(round(size_origin[0] * sc)), int(round(size_origin[1] * sc)))
			img = img_origin.resize(size)
			img = np.array(img)
			cn = int(round(cn_origin * sc))

			clusters = np.array(tuple(zip(np.random.rand(cn) * img.shape[0], np.random.rand(cn) * img.shape[1])))

			print(f"Start calculating with scale {sc}...")

			fast_start = time.perf_counter()
			dist_fast = tessel_fast(clusters, img.shape)
			img_fast = averaging_fast(cn, img, dist_fast)
			fast_end = time.perf_counter()

			low_start = time.perf_counter()
			dist_low = tessel_low_mem(clusters, img.shape)
			img_low = averaging_fast(cn, img, dist_low)
			low_end = time.perf_counter()

			file.write("{}\t{}\t{}\n".format(size, fast_end - fast_start, low_end - low_start))
			print(f"End calculating with scale {sc}...")


def start_tests():
	VoronoyTestSuit = unittest.TestSuite()
	VoronoyTestSuit.addTest(unittest.makeSuite(MessageSplittingTestCase))
	VoronoyTestSuit.addTest(unittest.makeSuite(HashingTestCase))
	VoronoyTestSuit.addTest(unittest.makeSuite(SplittingTestCase))
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(VoronoyTestSuit)


if __name__ == "__main__":
	unittest.main()