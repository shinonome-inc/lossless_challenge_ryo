from codec import Encoder
from sys import argv

# ex) python encode.py TMW/camera.pgm encoded
enc = Encoder(argv[1], argv[2], argv[3])
print('bpp', enc.encode())
