#-------------------------------------------------------------------------------
# Converts a photo (jpg, png, jpeg) into an ascii poster in a file called
# "poster"
#
# poster prints left column, then to the right. A few blank lines are printed
# to indicate the bottom of the image.
#
# Use text edit, font courier, font size = 8.2, line spaceing = 0.6
#
# resolution and filename must be manually changed in main()
#
# THINGS TO DO:
# - input filenames.
# - real dimensions of the poster given any photo.
# -
#-------------------------------------------------------------------------------
from PIL import Image
import numpy

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1[]?-_+~<>i!lI;:,\"^`'. "
class EditImage():
    def __init__(self, filename):
        img = Image.open(filename).convert('L')
        #not sure if this line is necessary. probably not.
        img.save('greyscale.png')
        self.width, self.height = img.size
        self.pixel_list = list(img.getdata())

class M():
    def __init__(self, resolution, filename):
        self.resolution = resolution
        self.filename = filename
        self.img = EditImage(filename)
        self.pixel_matrix = self.unflatten()
        self.density_matrix = self.get_density_matrix()
        self.index_matrix = []
        self.ascii_matrix = self.generate_ascii_matrix()


    def _calc_density(self, densities):
        #takes list of pixels, computes average color. returns number.
        avg = 0
        for pixel in densities:
            avg += pixel
        return avg/len(densities)

    def char_density(self, r, c):
        #takes coordinates. Calculates densites in area. Returns number.
        densities = []
        for i in range(self.resolution):
            for j in range(self.resolution):
                densities.append(self.pixel_matrix[i+r][j+c])
        return self._calc_density(densities)

    def get_density_matrix(self):
        density_matrix = []
        for i in range(0, self.img.height - self.resolution, self.resolution):
            row = []
            for j in range(0, self.img.width -self.resolution, self.resolution):
                row.append(self.char_density(i, j))
            density_matrix.append(row)
        return density_matrix

    def unflatten(self):
        pixels = []
        for i in range(0, self.img.width * self.img.height, self.img.width):
            rows = []
            for j in range(self.img.width):
                rows.append(self.img.pixel_list[i + j])
            pixels.append(rows)
        return pixels

    def flatten(self, m):
        ret = []
        for i in range(len(m)):
            for j in range(len(m[0])):
                ret.append(m[i][j])
        return ret

    def generate_ascii_matrix(self):
        mappings = {}
        all_values = self.flatten(self.density_matrix)
        all_values = sorted(list(set(all_values)))
        for i in range(len(all_values)):
            percentage_position = i/float(len(all_values))
            actual_position = int(percentage_position * len(chars))
            mappings[all_values[i]] = actual_position

        ret = []
        for i in range(len(self.density_matrix)):
            row = []
            index_matrix_row = []     #debug
            for j in range(len(self.density_matrix[0])):
                indx = mappings[self.density_matrix[i][j]]
                row.append(chars[indx])
                index_matrix_row.append(indx)
            self.index_matrix.append(index_matrix_row)
            ret.append(row)
        return ret

    def stdprint(self, matrix):
        print "NUM1",len(matrix)
        print "NUM2",len(matrix[0])

        for i in range(len(matrix)):
            rows = ""
            for j in range(len(matrix[0])):
                rows += str(matrix[i][j])
            print rows

    def posterit(self):
        num_rows = len(self.ascii_matrix)
        num_cols = len(self.ascii_matrix[0])
        width = 80
        f = open('poster', 'w+')
        print "NUMCOLS: ",num_cols
        print "NUMROWS: " ,num_rows
        for s in range(0, num_cols, width):
            for i in range(num_rows):
                string = ""
                if num_cols - s < width:
                    width = num_cols - s
                    print width
                for j in range(width):
                    string += str(self.ascii_matrix[i][j+s])
                f.write(string)
                f.write('\n')
            f.write('\n\n\n\n')

        f.close()

def main():
    resolution = 1
    filename = "images/2.jpg"
    matrix = M(resolution, filename)
    matrix.posterit()
main()
