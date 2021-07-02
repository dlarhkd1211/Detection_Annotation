#Code for Scaled YoloV4 , YoloV5 descripted by pytorch

import shutil
from tqdm import tqdm
from glob import glob
from sklearn.model_selection import train_test_split

path = glob('path of image')
train, test = train_test_split(path, random_state = 123)
for i in tqdm(train):
    shutil.copy(i,'/v5image/image/train')
    shutil.copy(i.replace('jpg','txt'),'/v5image/label/train')
for i in tqdm(test):
    shutil.copy(i,'/v5image/image/test')
    shutil.copy(i.replace('jpg','txt'),'/v5image/label/test')