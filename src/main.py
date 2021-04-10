import os
import cv2
from scripts.data_utils import pad_images_black_border, downscale_image, process_all_images_to_fit, split_dataset
from model.conv_net import run_model

def main():
    # Get file path of dog pics dataset.
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, '../dog_pics/')

    # Pre-process these by making sure all photos will fit CNN with regards to image dimensions.
    # Comment out this function once pre-processing of dataset is complete.
    process_all_images_to_fit(filepath)
    split_dataset(0.8)

    # image = downscale_image(os.path.join(filepath, 'n02085620-Chihuahua/n02085620_199.jpg'))
    # image = pad_images_black_border(os.path.join(filepath, 'n02086079-Pekinese/n02086079_606.jpg'))
    # cv2.imshow('image', image)  
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 

    # run_model()


if __name__ == '__main__':
    main()
