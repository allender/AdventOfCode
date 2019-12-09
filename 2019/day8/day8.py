# pylint: disable=missing-docstring, unused-import, mixed-indentation
import sys

imageWidth = 25
imageHeight = 6
numLayers = 0

class Layer():
    def __init__(self, num_pixels):
        self._num_pixels = num_pixels
        self.pixel_counts = { }
        self.data = [ ]
        for digit in range(10):
            self.pixel_counts[digit] = 0

    def add_pixel(self, pixel):
        self.data.append(pixel)
        self.pixel_counts[pixel] += 1

    def get_pixel(self, pixel):
        return self.data[pixel]

class Image():


    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels_per_layer = self.width * self.height
        self.layers = [ ]

        current_pixel = 0
        while (True):
            current_layer = Layer(self.pixels_per_layer)

            for _ in range(self.pixels_per_layer):
                current_layer.add_pixel( pixels[current_pixel] )
                current_pixel += 1

            self.layers.append(current_layer)
            if current_pixel >= len(pixels):
                break
            
            
    
if __name__ == '__main__':
    filename = 'input.txt'
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    with open(filename) as f:
        pixels = list(map(int, f.read().strip()))

    image = Image(25, 6, pixels)

    desired_layer = None
    num_zeros = 25 * 6
    for layer in image.layers:
        if layer.pixel_counts[0] < num_zeros:
            num_zeros = layer.pixel_counts[0]
            desired_layer = layer
    
    print (desired_layer.pixel_counts[1] * desired_layer.pixel_counts[2])

    #decode the image
    real_pixels = [ ]
    for pixel in range(25 * 6):
        p = -1
        for layer in image.layers:
            p = layer.get_pixel(pixel)
            if p != 2:
                break

        assert p != -1
        real_pixels.append(p)

    line_count = 0
    for num, pixel in enumerate(real_pixels):
        if pixel == 1:
            print ('.', end = '')
        elif pixel == 0:
            print (' ', end = '')

        line_count += 1
        if line_count == 25:
            line_count = 0
            print ('')



    