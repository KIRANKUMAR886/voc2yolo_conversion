import xml.etree.ElementTree as ET
import pickle
import os,sys
from os import listdir, getcwd
from os.path import join

classes=["08901725101053","08901030664205","08901030662010","04902430772877","08901030612381","08901512540102"]


def convert(size,box):
	# Conversion from VOC to YOLO format
	dw = 1./(size[0])
	dh = 1./(size[1])
	x = (box[0] + box[1])/2.0 - 1
	y = (box[2] + box[3])/2.0 - 1
	w = box[1] - box[0]
	h = box[3] - box[2]
	x = x*dw
	w = w*dw
	y = y*dh
	h = h*dh
	return (x,y,w,h)

#print ann_file
def converting_annotation(ann_file):
	for ann in ann_file:
		txt_file= ann.split('.')[0]+'.txt'
		in_file=open(ann_dir+ann)
		out_file =open(ann_dir+txt_file, 'w')
		tree=ET.parse(in_file)
		root = tree.getroot()
		size = root.find('size')
		w = int(size.find('width').text)
		h = int(size.find('height').text)

		print w,h
		for obj in root.iter('object'):
			cls=obj.find('name').text
			if cls not in classes:
				continue
			cls_id=classes.index(cls)
			xmlbox = obj.find('bndbox')
			b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
			data = convert((w,h), b)
			out_file.write(str(cls_id) + " " + " ".join([str(a) for a in data]) + '\n')


if __name__ == '__main__': 
	ann_dir=sys.argv[1]
	ann_file=os.listdir(ann_dir)
	ann_file.sort()
	print(ann_file)
	converting_annotation(ann_file)
