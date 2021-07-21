from tqdm import tqdm
from PIL import Image
from glob import glob
import numpy as np
import argparse

def yolo2voc(path, img_format):
  path = glob(path +'/*.' + img_format) 
  for i in tqdm(path):
      image = Image.open(i)
      name = i.split('/')[-1]
      img = np.array(image)
      h, w = img.shape[0], img.shape[1]
      with open(i.replace('jpg','txt'), 'r') as f:
          lines = f.readlines()
          g = open(i.replace('jpg','xml'), 'w')
          g.write('<annotation>\n')
          g.write('	<folder>images</folder>\n')
          g.write('	<filename>{}</filename>\n'.format(name))
          g.write('	<path>{}</path>\n'.format(i))
          g.write('	<source>\n')
          g.write('		<database>Unknown</database>\n')
          g.write('	</source>\n')
          g.write('	<size>\n')
          g.write('		<width>{}</width>\n'.format(w))
          g.write('		<height>{}</height>\n'.format(h))
          g.write('		<depth>3</depth>\n')
          g.write('	</size>\n')
          g.write('	<segmented>0</segmented>\n')
          for line in lines:
              li = line.split()
              if li[0] == '0':
                  cate = 'dog'
              elif li[0] == '1':
                  cate = 'person'
              else:
                  cate = 'cat'
              xmin = int((float(li[1]) - float(li[3])/2) * w)
              ymin = int((float(li[2]) - float(li[4])/2) * h)
              xmax = int((float(li[1]) + float(li[3])/2) * w)
              ymax = int((float(li[2]) + float(li[4])/2) * h)
              if float(li[1]) * float(li[2]) < 1/(16*16):
                  continue
              g.write('	<object>\n')
              g.write('		<name>{}</name>\n'.format(cate))
              g.write('		<pose>Unspecified</pose>\n')
              g.write('		<truncated>0</truncated>\n')
              g.write('		<difficult>0</difficult>\n')
              g.write('		<bndbox>\n')
              g.write('			<xmin>{}</xmin>\n'.format(xmin))
              g.write('			<ymin>{}</ymin>\n'.format(ymin))
              g.write('			<xmax>{}</xmax>\n'.format(xmax))
              g.write('			<ymax>{}</ymax>\n'.format(ymax))
              g.write('		</bndbox>\n')
              g.write('	</object>\n')
          g.write('</annotation>')
      g.close()
      f.close()

def nametxt(path, img_format):
  path = glob(path +'/*.' + img_format) 
  trainval, test = train_test_split(path, train_size = 0.8, random_state = 123)
  train, val = train_test_split(trainval, test_size = 0.125, random_state = 123)
  # train : val : test = 7 : 2 : 1
  with open(path + '/train.txt','w') as f:
    for name in tqdm(train):
        f.write(name.split('/')[-1].replace('.' + img_format,''))
        f.write('\n')
  f.close()
  with open(path + '/test.txt','w') as f:
    for name in tqdm(test):
        f.write(name.split('/')[-1].replace('.' + img_format,''))
        f.write('\n')
  f.close()
  with open(path + '/val.txt','w') as f:
    for name in tqdm(val):
        f.write(name.split('/')[-1].replace('.' + img_format,''))
        f.write('\n')
  f.close()



def main():
  parser = argparse.ArgumentParser(description="This script support converting yolo format to voc format xml")
  parser.add_argument('--path', type=str, default=None, help = 'path to image of yolo format')
  parser.add_argument('--img-format', type=str, default='jpg', help = 'jpg or png')
  args = parser.parse_args()
  yolo2voc(args.path, args.img_format)
  nametxt(args.path, args.img_format)

if __name__ == '__main__':
  main()
