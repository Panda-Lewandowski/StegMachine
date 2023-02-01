using ImageMagick;
using System;
using System.IO;

public class Program
{

    public static bool is_hallucinate(string path_container)
    {
        bool result = false;
        using ( MagickImage comp_image = new MagickImage(path_container))
        {
            comp_image.ColorSpace = ColorSpace.sRGB;
            using (var pc = comp_image.GetPixels())
            {
                var popular_colors = comp_image.UniqueColors();
                popular_colors.Write("/home/avsjanka/Desktop/Projects/Stegano project/Analyze/colors.png");
            }
        }
        using (MagickImage color_image = new MagickImage("/home/avsjanka/Desktop/Projects/Stegano project/Analyze/colors.png"))
        {
            int size = color_image.Width;
            int count = 0;
            using (var pc = color_image.GetPixels())
            {
                for (int x = 0; x < color_image.Width; x++)
                {
                    var pixel = pc.GetPixel(x, 0);
                    if (pixel.GetChannel(0) - pixel.GetChannel(1) >= 50 &&
                        pixel.GetChannel(0) - pixel.GetChannel(2) >= 50)
                        count++;
                }
            }
            if (Convert.ToDouble(count) / Convert.ToDouble(size) > 0.5)
                result = true;
        }
        return result;
    }
    public static bool is_deegg(string path)
    {
        byte[] bytes = File.ReadAllBytes(path);
        File.WriteAllText(path:@"/home/avsjanka/Desktop/Projects/Stegano project/Analyze/bin_img_hex.bat",Convert.ToHexString(bytes));
        string hex_picture = File.ReadAllText(path:@"/home/avsjanka/Desktop/Projects/Stegano project/Analyze/bin_img_hex.bat");
        bool result = false;
        int res = hex_picture.IndexOf("242326292A402628235E2A00D19890FF");
        if( Convert.ToInt32(hex_picture.IndexOf("242326292A402628235E2A00D19890FF")) != -1)
            result = true;
        return result;
    }

    public static bool is_anubis(string path)
    {
        byte[] bytes = File.ReadAllBytes(path);
        File.WriteAllText(path:@"/home/avsjanka/Desktop/Projects/Stegano project/Analyze/bin_img_hex.bat",Convert.ToHexString(bytes));
        string hex_picture = File.ReadAllText(path:@"/home/avsjanka/Desktop/Projects/Stegano project/Analyze/bin_img_hex.bat");
        bool result = false;
        if (
            Convert.ToInt32(hex_picture.IndexOf("6c696d6974657231")) != -1 &&
            Convert.ToInt32(hex_picture.IndexOf("6c696d6974657232")) != -1 &&
            Convert.ToInt32(hex_picture.IndexOf("696e736572746564206c656e67746820626567696e73")) != -1
        ) result = true;
        return result;
    }

    public static void ReturnColors(string path)
    {
        using ( MagickImage comp_image = new MagickImage(path))
        {
            comp_image.ColorSpace = ColorSpace.sRGB;
            //Console.WriteLine($"{comp_image.UniqueColors()}");
           using (var pc = comp_image.GetPixels())
           {
               for (int y = 0; y < comp_image.Height; y++)
               {
                   for (int x = 0; x < comp_image.Width; x++)
                   {
                       var pixel = pc.GetPixel(x, y);
                       //if( pixel.GetChannel(0)-pixel.GetChannel(1)>=100 && pixel.GetChannel(0)-pixel.GetChannel(2)>=100) 
                           Console.Write($"{pixel.GetChannel(0)},{pixel.GetChannel(1)},{pixel.GetChannel(2)} ");
                   }
                   Console.WriteLine();
               }
               var popular_colors = comp_image.UniqueColors();
               popular_colors.Write("/home/avsjanka/Desktop/Projects/Stegano project/Analyze/colors.png");
               //Console.WriteLine($"{popular_colors}");
           }
        }
    }
    
    
    static int Main()
    {
        var origin_image="";
        var stego_container = "";
        Console.WriteLine("Write path to origine image:");
        origin_image = Convert.ToString(Console.ReadLine());
        Console.WriteLine("Write path to stego container:");
        stego_container = Convert.ToString(Console.ReadLine());
        origin_image = "/home/avsjanka/Desktop/Start.jpg";
        stego_container = "/home/avsjanka/Desktop/OUT.png";
        Console.WriteLine($"Using of DeEgger is {is_deegg(stego_container)}");
        Console.WriteLine($"Using of Anubis is {is_anubis(stego_container)}");
        var diffImagePath = @"/home/avsjanka/Desktop/Projects/Stegano project/Analyze/OUT_New.png";
        Console.WriteLine("Write path to compare image:");
        diffImagePath = Convert.ToString(Console.ReadLine());
        using (MagickImage origin = new MagickImage(origin_image))
        using (MagickImage stego = new MagickImage(stego_container))
        using (MagickImage diffImage = new MagickImage())
        {
            origin.Compare(stego, ErrorMetric.Absolute, diffImage);
            diffImage.Write(diffImagePath);
        }
        Console.WriteLine($"Using of Hallucinate is {is_hallucinate(diffImagePath)}");
        return 1;
    }
}
