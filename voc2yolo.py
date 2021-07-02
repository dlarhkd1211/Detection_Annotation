import xml.etree.ElementTree as ET
from glob import glob
import argparse

def voc2yolo(path):
  path = glob(path +'/*.xml') 
  for i in path:
    doc = ET.parse(i)
    root = doc.getroot()
    f = open(i.replace('xml','txt'), 'w')
    for object in root.iter("size"):
      width = int(object.findtext("width"))
      height = int(object.findtext("height"))

    for object in root.iter("object"):
      xmin = int(object.find("bndbox").findtext("xmin"))
      xmax = int(object.find("bndbox").findtext("xmax"))
      ymin = int(object.find("bndbox").findtext("ymin"))
      ymax = int(object.find("bndbox").findtext("ymax"))

      class2idx = {'dog':1, 'person':2, 'cat':3}
      classes =''
      f.write(str(classes))
      f.write(' ')
      f.write(str(((xmin + xmax)//2)/width))
      f.write(' ')
      f.write(str(((ymin + ymax)//2)/height))
      f.write(' ')
      f.write(str((xmax - xmin)/width))
      f.write(' ')
      f.write(str((ymax - ymin)/height))
      f.write('\n')
    f.close()

def main():
  parser = argparse.ArgumentParser(description="This script support converting voc format xml to yolo format")
  parser.add_argument('--path', type=str, default=None, help = 'path to image of yolo format')
  args = parser.parse_args()
  voc2yolo(args.path)

if __name__ == '__main__':
  main()