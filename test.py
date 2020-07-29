import numpy as np 
import imageio
import matplotlib.pyplot as plt 


from codec import Encoder, Decoder
from codecfile import compress, extract
from llc_io import imread, imwrite

INPUT_IMG = imageio.imread("/Users/ryomasutani/Desktop/machine-learning/CV/image_processing/image_compression/sample.png")

def test_decoder():
    enc = Encoder(INPUT_IMG, 1, 1)

    # Encoding test
    encoded = enc.encode()
    with open("encoded", "wb") as f:
        f.write(encoded)

    # Decoding test
    dec = Decoder("encoded")
    decoded = dec.decode()
    print(decoded)

    plt.figure(1)
    plt.imshow(decoded)
    plt.show()


    # Reconstruction test
    for i in range(784):
        if INPUT_IMG.ravel()[i] != decoded.ravel()[i]:
            print("Error at index {}.".format(i))
            return 
    
    print("Decoder test: passed")

def test_compress():
    out = compress(INPUT_IMG)
    print(out)

def test_imwrite():
    imwrite(INPUT_IMG, "encoded")

def test_llc_io():
    imwrite(INPUT_IMG, "encoded")
    
    decoded = imread("encoded")

    plt.figure(1)
    plt.imshow(decoded)
    plt.show()

    for i in range(784):
        if INPUT_IMG.ravel()[i] != decoded.ravel()[i]:
            print("Error at index {}.".format(i))
            return 
    
    print("llc_io test: Passed")


def main():
    # test_decoder()
    test_llc_io()


if __name__ == "__main__":
    main()

