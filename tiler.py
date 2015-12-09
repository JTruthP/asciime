"""
 *****************************************************************************
   FILE: tiler.py

   AUTHOR: Jack Pierce

   ASSIGNMENT: Lab number 5

   DATE: 11/1/13

   DESCRIPTION: replace the pixels of one large image with the closest average
   pixel rgb value of another pixel

 *****************************************************************************
"""
from cs110graphics import*
import math

def resizeCrop(image, width, height):
    pwidth, pheight = image.size()

    cropTB = 0
    cropSides = 0

    #ratio is the amount the image needs to be multiplied by
    ratio = (float(width) / height) * (float(pheight) / pwidth)

    #Decide which sides to crop from, and by how much
    if ratio > 1:
        cropTB = int(((pheight / width) - (float(pwidth) / height)) / 2)
    else:
        cropSides = int((float((pwidth / height)) -\
                             (float(pheight) / width)) / 2)

    #Actually crop image
    image.crop(cropTB, cropTB, cropSides, cropSides)
    image.resize(width, height)

    return image

def averagePixel(image):
    #find the average pixel of a given image and return it in (r, g, b) form
    pixelList = image.getPixels()
    redPixel = 0
    bluePixel = 0
    greenPixel = 0

    #add up all the r's, g's and b's
    for i in range(len(pixelList)):
        redPixel += pixelList[i][0]
        greenPixel += pixelList[i][1]
        bluePixel += pixelList[i][2]

    return (redPixel/len(pixelList), greenPixel/len(pixelList),
            bluePixel/len(pixelList), 255)

def makeTiles(files, tileSize):
    #create a list of tiles that is ((average pixel). [list of pixels])
    tiles = []
    for i in range(len(files)):
        tile = files[i]
        resizeCrop(tile, tileSize, tileSize)
        tiles.append((averagePixel(tile), tile.getPixels()))
    return tiles

def closestTile(pixel, tiles):

    closest = tiles[0]

    closestDistance = pixelDistance(pixel, tiles[0])

    #find the average distance in 3d space between the pixel and each tile's
    #average pixel
    for i in range(len(tiles)):
        distance = pixelDistance(pixel, tiles[i])
        if distance < closestDistance:
            closest = tiles[i]
            closestDistance = distance

    return closest

def pixelDistance(pixel, tile):
    distance = ((abs(pixel[0] - tile[0][0]) ** 2) +\
                (abs(pixel[1] - tile[0][1]) ** 2) +\
                (abs(pixel[2] - tile[0][2]) ** 2)) ** (.5)

    return distance

def unflatten(lst, width):
    #turn a list of pixels into lists of lists so that the larger lists are rows
    answer = []
    numSublists = len(lst) / width
    for i in range(numSublists):
        answer.append(lst[i * width:(i + 1) * width])
    return answer

def flatten(lstlst):
    #turn a list of lists (rows and colums) into just a list
    answer = []
    for lst in lstlst:
        for item in lst:
            answer.append(item)
    return answer

def placeTile(pixels, row, col, tile):
    tilesize = int(len(tile[1]) ** (.5))
    for k in range(tilesize):
        # replace each row in the blank list of pixels...
        for c in range(tilesize):
            # replace each column in that row with an individual pixel
            uftile = unflatten(tile[1], tilesize)
            pixels[row * tilesize + k][col * tilesize + c] = uftile[k][c]

    return pixels

def buildTiledImage(subjectImage, imagewidth, imageheight, tilesize):
    #crop the target(subject) image
    subjectImage = (resizeCrop(subjectImage, imagewidth/tilesize,
                                  imageheight/tilesize))

    #create all the tiles to replace subjectImage's pixels

    tiles = []
    for i in range(841):
        tiles.append(Image("tileImages%d.jpg" % (i)))
    tiles = makeTiles(tiles, tilesize)

    #tiles = []
    #for i in range(0, 13) + range(13, 25) + range(26, 170):
    #    tiles.append(Image("/home/acampbel/images/image%d.jpg" % (i)))
    #tiles = makeTiles(tiles, tilesize)

    #create a giant blank list of rows and columns, imagewidth by imageheight
    pixels = []
    for i in range(imageheight * imagewidth):
        pixels.append((0, 0, 0, 255))
    ufpixels = unflatten(pixels, imagewidth)

    #unflatten te subject image so i can index certain rows and columns
    ufSubImage = unflatten(subjectImage.getPixels(), imagewidth/tilesize)

    # replace each row in subject image...
    for i in range(imageheight/tilesize):

        # and for each column in that row...
        for j in range(imagewidth/tilesize):

            #choose the right tile to occupy that space
            rightTile = closestTile(ufSubImage[i][j], tiles)
            ufpixels = placeTile(ufpixels, i, j, rightTile)

    #create a new image, and set its pixels to the pixels of the now not blank
    #list of pixels
    newImage = Image(imagewidth, imageheight)
    newImage.setPixels(flatten(ufpixels))

    return newImage

def main():

    imagewidth = 1000
    imageheight = 800
    tilesize = 3


    win = Window(imagewidth, imageheight)



    #prompt the name of the photo to tile
    toTile = str(raw_input("What is the name of the photo to tile?: "))

    #Tile the image that the user specified. Call it newImage.
    newImage = (buildTiledImage((Image(toTile)), imagewidth, imageheight,
                                tilesize))

    win.add(newImage)
    newImage.moveTo(Point(imagewidth / 2, imageheight / 2))

    #Prompt a filename to save the tiled image as
    filename = str(raw_input("What would you like to name your new image? "))


    #save the image
    newImage.save(str(filename))

if __name__ == "__main__":
    # Use one of:
    #main()
    StartGraphicsSystem(main)
