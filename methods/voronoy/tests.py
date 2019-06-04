from tessellation_fast import averaging_fast, tessel_fast
from tessellation_low import averaging_low, tessel_low_mem
from message import split_message_to_bits, InvaligBlockLength
from hashing import get_comparable_hash, get_md5_hash, get_sha256_hash
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
		self.path_to_img = "test/fast.jpg"
		self.md5_hash = "36deb3fab78994cc135745d5cde05cc2"
		self.sha256_hash = "6f6ad8d0345a8f7dc99c921a6aa7ad13f787a8e5dc43c9aa2c1b096392a46f9c"
		self.comparable_hash = "ffffffe002030300"


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
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(VoronoyTestSuit)


if __name__ == "__main__":
	unittest.main()