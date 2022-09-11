import unittest

from PIL import Image

from modules.analysis import Analyzer


class TestTestCase(unittest.TestCase):
    def test_hello_world(self):
        test_str = "hello world"
        self.assertEqual(test_str, "hello world")


class AnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        self.img_name = "she.png"
        self.an = Analyzer(display=False)
    def test_exif(self):
        exif = self.an.exif(self.img_name)
        exif.pop('File:FileAccessDate')
        self.assertDictEqual({'SourceFile': 'she.png', 
                              'ExifTool:ExifToolVersion': 11.06,
                              'File:FileName': 'she.png', 
                              'File:Directory': '.', 
                              'File:FileSize': 281404, 
                              'File:FileModifyDate': '2019:04:21 16:58:26+03:00', 
                              'File:FileInodeChangeDate': '2019:04:21 16:58:26+03:00',
                              'File:FilePermissions': 644,
                              'File:FileType': 'PNG', 
                              'File:FileTypeExtension': 'PNG', 
                              'File:MIMEType': 'image/png', 
                              'File:ExifByteOrder': 'MM', 
                              'PNG:ImageWidth': 696, 
                              'PNG:ImageHeight': 320, 
                              'PNG:BitDepth': 8, 
                              'PNG:ColorType': 2, 
                              'PNG:Compression': 0, 
                              'PNG:Filter': 0, 
                              'PNG:Interlace': 0, 
                              'EXIF:ImageDescription': 'kx0znibp', 
                              'EXIF:Make': 'Subscribe To PewDiePie', 
                              'EXIF:Model': 'Nokia 3310', 
                              'EXIF:ResolutionUnit': 2, 
                              'EXIF:Software': 'InsertTxt', 
                              'EXIF:Artist': 'Who is she?', 
                              'EXIF:YCbCrPositioning': 1,
                              'EXIF:ExifVersion': '0231',
                              'EXIF:DateTimeOriginal': '2018:12:01 16:00:49', 
                              'EXIF:CreateDate': '2018:11:30 14:00:36', 
                              'EXIF:ComponentsConfiguration': '1 2 3 0', 
                              'EXIF:UserComment': 'rel luminance', 
                              'EXIF:FlashpixVersion': '0100', 
                              'Composite:ImageSize': '696x320', 
                              'Composite:Megapixels': 0.22272}, exif)


def start_tests():
    analyzerTestSuit = unittest.TestSuite()
    analyzerTestSuit.addTest(unittest.makeSuite(AnalyzerTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(analyzerTestSuit)


if __name__ == '__main__':
    unittest.main()