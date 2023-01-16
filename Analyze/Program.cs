using ImageMagick;
using System;
using System.IO;

public class Program
{

    /*public bool it_hall(MagickImage final_image,MagickImage stego_container)
    {
        bool result = false;


        return result;
    }*/
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
    static int Main()
    {
        var origin_image="";
        var stego_container = "";
        Console.WriteLine("Write path to origine image:");
        origin_image = Convert.ToString(Console.ReadLine());
        Console.WriteLine("Write path to stego container:");
        stego_container = Convert.ToString(Console.ReadLine());
        
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
        return 1;
    }
}