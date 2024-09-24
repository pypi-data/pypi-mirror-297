from skimage.io import imread, imsave

def read_image(path, is_gray = False):
    image = imreaf(path, as_gray = is_gray)
    return image

def save_image(image,path):
    imsave(path, image)
    