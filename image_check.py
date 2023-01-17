import numpy as np
import cv2
import os
from skimage import metrics

# detect QR and add white border
def pre_processing(im):
    # Convert image to grayscale
    #1-
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #2-
    im = cv2.GaussianBlur(im, (5, 5), 0)
    #3-
    #im = cv2.medianBlur(im, 3)

    # Convert image to black and white
    # 128,255, you can change
    _, im = cv2.threshold(im,100,255,cv2.THRESH_BINARY)
    # Get the indexes of the black pixels
    black_pixels = np.where(im == 0)
    # Get the min and max points of the QR code
    min_x = np.min(black_pixels[1])
    max_x = np.max(black_pixels[1])
    min_y = np.min(black_pixels[0])
    max_y = np.max(black_pixels[0])
    # Get the QR code image
    qr_code = im[min_y:max_y,min_x:max_x]
    # Get the shape of the QR code
    height, width  = qr_code.shape
    # constant value for white border
    constant = 2
    # check diff from height and width
    border = max(height, width) - min(height, width)
    #check even or odd:
    if border % 2 != 0:
        # do even
        border +=1
        # add white border
        if height < width:
            qr_code = cv2.copyMakeBorder(qr_code, (border)//2 + constant, (border)//2 + constant, constant+1, constant, cv2.BORDER_CONSTANT, value=255)
        else:
            qr_code = cv2.copyMakeBorder(qr_code, constant+1, constant, (border)//2 + constant, (border)//2 + constant, cv2.BORDER_CONSTANT, value=255)
    # even
    else:
        # add white border
        if height < width:
            qr_code = cv2.copyMakeBorder(qr_code, (border)//2 + constant, (border)//2 + constant, constant, constant, cv2.BORDER_CONSTANT, value=255)
        else:
            qr_code = cv2.copyMakeBorder(qr_code, constant, constant, (border)//2 + constant, (border)//2 + constant, cv2.BORDER_CONSTANT, value=255)
    return qr_code

def qr_resize(im, im1):
    # take shape
    width = im.shape[1]
    height = im.shape[0]    
    dim = (width, height)
    # resize image
    resized = cv2.resize(im1, dim, interpolation = cv2.INTER_AREA)
    return resized


# add white border to small shape image
def equals_shape(im, im1):
    # take shape
    height, _ = im.shape
    height1, _ = im1.shape
    # find max shape
    find_max = max(height, height1)
    # find diff
    diff =  abs(height - height1)
    # odd
    if diff % 2 != 0:
        diff +=1
        # decide
        if find_max == height:
            im = cv2.copyMakeBorder(im, 1 , 0, 1, 0, cv2.BORDER_CONSTANT, value=255)
            im1 = cv2.copyMakeBorder(im1, diff//2 , diff//2, diff//2, diff//2, cv2.BORDER_CONSTANT, value=255)
        else:
            im = cv2.copyMakeBorder(im, diff//2 , diff//2, diff//2, diff//2, cv2.BORDER_CONSTANT, value=255)
            im1 = cv2.copyMakeBorder(im1, 1 , 0, 1, 0, cv2.BORDER_CONSTANT, value=255)
    # even
    else:
        # decide
        if find_max == height:
            im1 = cv2.copyMakeBorder(im1, diff//2 , diff//2, diff//2, diff//2, cv2.BORDER_CONSTANT, value=255)
        else:
            im = cv2.copyMakeBorder(im, diff//2 , diff//2, diff//2, diff//2, cv2.BORDER_CONSTANT, value=255)

    return im, im1

def compare(real, snap, threshold = 0.60):
    # check 0 to 360 degrees
    for degree in range(0,360,15):
        # Get rotation matrix for the current angle
        rot_mat = cv2.getRotationMatrix2D((snap.shape[1] / 2, snap.shape[0] / 2), degree, 1)
        # Perform the rotation
        im_qr = cv2.warpAffine(snap, rot_mat, (snap.shape[1], snap.shape[0]))
        # 1-
        #diff = abs(real - im_qr)
        #mean_diff = np.mean(diff)
        #mean_diff = (100-mean_diff)/100
        #print(ssim_ab)
        #2-
        #mean_diff = np.mean((real - im_qr) ** 2)
        #3-
        h, w = snap.shape[:2]
        window = min(h, w)
        if not window % 2 == 1:
            window -= 1
        ssim = metrics.structural_similarity(real, im_qr, win_size=window)
        if ssim > threshold:
            print(ssim)
            return True  
    return False

# run
def run(Snap):
    # real QR
    QR_path = 'Train/'
    # QR list
    QRs = os.listdir(QR_path)

    for QR in QRs:

        # Open real image
        Real = cv2.imread(f'Train/{QR}')
        Real1 = pre_processing(Real)
    
        Snap1 = pre_processing(Snap)

        Snap2 = qr_resize(Real1,Snap1)
        # Save the filtered image
        
        Real2, Snap3 = equals_shape(Real1, Snap2)
        #cv2.imwrite('QR.png', Snap2)

        result = compare(Real2,Snap3)
        if result:
            print(QR, 'is matched.')
            break
        else:
            print(QR, 'is not mached')