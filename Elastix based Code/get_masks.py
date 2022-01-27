import cv2 as cv
import numpy as np

def find_luns_cv(im):
    '''Function to get the lung mask of a 2D image'''
    #Clipping the air values without considering the outside of the CT cylinder
    im[im<-1000] = 0
    clipped = im.clip(-1000, -300)
    clipped[clipped != -300] = 1
    clipped[clipped == -300] = 0

    #Get the binary mask of the clipped image and the contours
    ret,th1 = cv.threshold(np.uint8(clipped),0,255,cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(th1, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    final_contours = []
    for i,c in enumerate(contours):
        ar = cv.contourArea(c)
        per = cv.arcLength(c,True)
        #Ignore empty contours
        if per>0:
            #Basic condition on minimum area and area-to-perimeter ratio
            if (ar>1000) & ((ar/per)>3):
                hull = cv.convexHull(c)
                hull_area = cv.contourArea(hull)
                sol = float(ar)/hull_area
                #Avoid almost circular contours (body outer contour)
                if sol<0.985:
                    #Enclosing circle 
                    e = cv.fitEllipse(c)
                    #Moments analysis to check centroid and principal axes
                    M = cv.moments(c)
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    x1 = (cx + e[1][1] / 2 * np.cos((e[2] + 90) * np.pi / 180.0))
                    y1 = (cy + e[1][1] / 2 * np.sin((e[2] + 90) * np.pi / 180.0))
                    x2 = (cx + e[1][1] / 2 * np.cos((e[2] - 90) * np.pi / 180.0))
                    y2 = (cy + e[1][1] / 2 * np.sin((e[2] - 90) * np.pi / 180.0))
                    #If created to avoid the case where the principal axis is vertical 
                    #i.e. (x2 and x1 are the same)
                    if ((x2-x1)>=0):
                        #Remove contours whose centroid is next to the borders
                        if (abs((x2-x1))==0.0)&(120<cy<410)&(100<cx<410):
                            circle = cv.minEnclosingCircle(c)
                            circularity = 4*np.pi*(ar/(per*per))
                            #Remove contours related to the CT outer cylinder and small circular vessels
                            if (circle[1]<220)&(circularity<0.85):
                                final_contours.append(c)
                        elif (abs((y2-y1)/(x2-x1))>0.0001)&(120<cy<410)&(100<cx<410):
                            circle = cv.minEnclosingCircle(c)
                            circularity = 4*np.pi*(ar/(per*per))
                            if (circle[1]<220)&(circularity<0.85):
                                final_contours.append(c)
    #Create the mask with the selected contours
    mask = np.zeros(im.shape)
    cv.drawContours(mask, final_contours, -1, (255),-1,)
    return mask

def get_lungs_volume(vol):
    '''Function to get the lungs slice by slice, if 3 consecutive slices after the 20 initial ones
    contain no lungs, finish the segmentation of the volume. This is to avoid segmenting air in the intestine'''
    new_vol = np.zeros(vol.shape)
    c=0
    for i in range(vol.shape[0]):
        seg = find_luns_cv(vol[i,:,:])
        new_vol[i,:,:] = seg
        if (np.sum(seg)==0)&(i>20):
            c += 1
        else:
            c=0
        if c>2:
            break
    return new_vol

def get_crop_mask(vol, lm):
    '''Function to get the cropped mask given a volume and its landmark files'''
    lm = np.genfromtxt(lm, dtype = np.int64)
    new_vol = np.zeros(vol.shape)
    # Crop only where the landmarks are + 8 pixel margin
    crop_min = np.min(lm, axis = 0) - 8
    crop_max = np.max(lm, axis = 0) + 8
    crop_range = [slice(crop_min[2], crop_max[2]), slice(crop_min[1], crop_max[1]), slice(crop_min[0], crop_max[0])]
    new_vol[crop_range[0], crop_range[1], crop_range[2]] = 1
    return new_vol