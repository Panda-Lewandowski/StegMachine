import zlib 

def deflate_compress(b_str):
    return zlib.compress(b_str)

def deflate_decompress(b_str):
    return zlib.decompress(b_str)


if __name__ == "__main__":
    source = input('Укажите текст для сжатия/распаковки: ')
    compress_data = deflate_compress(source.encode('utf-8'))
    print(f"Сжатые данные: {compress_data}")
    decompress_data = deflate_decompress(compress_data).decode('utf-8')
    print(f"Распакованные данные: {decompress_data}")