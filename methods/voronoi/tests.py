from message import split_message_to_bits, InvaligBlockLength
from hashing import get_comparable_hash, get_md5_hash, get_sha256_hash
from splitting import is_point_in_box, get_scheme_of_splitting, split_to_workspace, \
	get_clusters_points_in_box, get_rescale_clusters
from PIL import Image
from bitstring import BitArray
from voronoi import StegoVoronoi
from voronoi_low import StegoVoronoiLow

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
		self.path_to_img = "photo.jpg"
		self.md5_hash = b"\xfa\x1b\t\xbb\xa9\x10\x15E\xd5\x88[\x8a9\x8f'J"
		self.sha256_hash =  b'\xa2\xd0\xa2pn\xa8P<\xef\x90U\x83\x08*\xa1\x87\xe17\xfdqPC\x91&?\xc7C\x93\xbcR\x82\\'
		self.comparable_hash = b'\xff\xff\xff\xe0\x02\x03\x03\x00'

	def test_md5_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_md5_hash(img)
		self.assertEqual(len(hash), 16)
		self.assertEqual(hash, self.md5_hash)

	def test_sha256_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_sha256_hash(img)
		self.assertEqual(len(hash), 32)
		self.assertEqual(hash, self.sha256_hash)

	def test_comparable_hash(self):
		img = Image.open(self.path_to_img)
		img = np.array(img)
		hash = get_comparable_hash(img)
		self.assertEqual(len(hash), 8)
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


def speed_test_with_proccess_embed():
	img = Image.open("test.jpg")
	msg = b'\xb2\x1a\xe7\x04z\xce'

	print("Create voronoi classes...")
	svor_low = StegoVoronoiLow()
	svor_default = StegoVoronoi()
	svor_len = StegoVoronoi(num_of_proc=len(msg))
	# svor_2proc = StegoVoronoi(num_of_proc=2) # as default
	svor_4proc = StegoVoronoi(num_of_proc=4)
	svor_more = StegoVoronoi(num_of_proc=len(msg)+2)

	svors = [svor_low, svor_default, svor_len, svor_4proc, svor_more]

	print("Starting speed test...")
	attempts = 10
	with open("embed_test.txt", "w") as file:
		for svor in svors:
			average_time = 0
			real_attempts = 0
			for i in range(attempts):
				print(f"Starting {svor} speed test. Attempt № {i}")
				try:
					start = time.perf_counter()
					stego_img = svor_low.embed(msg, img)
					end = time.perf_counter()
				except ZeroDivisionError:
					print(f"{svor} got down by exception :(")
				else:
					t = end - start
					print(f"Finishing {svor} speed test. Attempt № {i}. Result: {t}")
					real_attempts += 1
					average_time += t

			work_time = average_time/real_attempts
			print(f"Finishing {attempts} for {svor}. Average time - {work_time}")
			file.write(f"{svor}:\t{work_time}  sec\n")


def speed_test_with_proccess_extract():
	msg = b'\xb2\x1a\xe7\x04z\xce'
	img = Image.open("stego.png")

	print("Create voronoi classes...")
	svor_low = StegoVoronoiLow()
	svor_default = StegoVoronoi()
	svor_len = StegoVoronoi(num_of_proc=len(msg))
	# svor_2proc = StegoVoronoi(num_of_proc=2) # as default
	svor_4proc = StegoVoronoi(num_of_proc=4)
	svor_more = StegoVoronoi(num_of_proc=len(msg)+2)

	svors = [svor_low, svor_default, svor_len, svor_4proc, svor_more]

	print("Starting speed test...")
	attempts = 10
	with open("extract_test.txt", "w") as file:
		for svor in svors:
			average_time = 0
			real_attempts = 0
			for i in range(attempts):
				print(f"Starting {svor} speed test. Attempt № {i}")
				try:
					start = time.perf_counter()
					svor.extract(img, len(msg))
					end = time.perf_counter()
				except ZeroDivisionError:
					print(f"{svor} got down by exception :(")
				else:
					t = end - start
					print(f"Finishing {svor} speed test. Attempt № {i}. Result: {t}")
					real_attempts += 1
					average_time += t

			work_time = average_time/real_attempts
			print(f"Finishing {attempts} for {svor}. Average time - {work_time}")
			file.write(f"{svor}:\t{work_time}  sec\n")


def min_cn():
	img = Image.open("photo.jpg")
	msg_buff = b'\x80iv\r\nu\xd4e\xf33'
	cn = 3000
	
	for i in range(5, len(msg_buff)):
		end_flag = False
		while not end_flag:
			try:
				print(f"Trying with {cn} for {i} bytes...")
				msg = msg_buff[:i]
				svor = StegoVoronoi(cn=cn, num_of_proc=2) 
				stego_img = svor.embed(msg, img)
				if svor.extract(stego_img, len(msg)) != msg:
					raise IndexError("blabla")
			except IndexError as e:
				print(e)
				cn += 500
			else:
				end_flag = True
				print(cn, i)
				cn = 3000

	
def msg_size_speed():
	img = Image.open("test.jpg")
	msg = b'\xb2\x1a\xe7\x04z\xce\x80iv\r\nu\xd4e\xf33'
	attempts = 5
	for i in range(5, len(msg)):
		average_time = 0
		real_attempts = 0
		for j in range(attempts):
			print(f"Starting {i} bytes speed test. Attempt № {j}")
			msg = msg[:i]
			svor = StegoVoronoi(num_of_proc=2) 
			start = time.perf_counter()
			stego_img = svor.embed(msg, img)
			end = time.perf_counter()
			t = end - start
			real_attempts += 1
			average_time += t
			print(f"Finishing for {i} bytes in {j} attempt. Time - {t}")

		work_time = average_time/real_attempts
		print(f"Finishing for {i} bytes. AvTime - {work_time}")

def start_tests():
	VoronoiTestSuit = unittest.TestSuite()
	VoronoiTestSuit.addTest(unittest.makeSuite(MessageSplittingTestCase))
	VoronoiTestSuit.addTest(unittest.makeSuite(HashingTestCase))
	VoronoiTestSuit.addTest(unittest.makeSuite(SplittingTestCase))
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(VoronoiTestSuit)


if __name__ == "__main__":
	unittest.main()
	# msg_size_speed()