import os
import xml.etree.ElementTree as ET
import math

xml_dir = "../../repo-imagenes/robots-repo-imagenes/labels/mates/"
img_dir = "../../repo-imagenes/robots-repo-imagenes/images/mates/"
labels = ["mate","calabaza","metal","madera","plastico"] #TODO: estaria bueno unificar con los que son Mate, Madera, Plastico, Calabaza, Metal
tamanio = 416
mejores_pesos = "red_lego.h5"

#ejemplo de json generado
#{'object': [{'name': 'mate', 'xmin': 194, 'ymin': 33, 'xmax': 556, 'ymax': 845}, {'name': 'madera', 'xmin': 197, 'ymin': 337, 'xmax': 547, 'ymax': 837}], 'filename': '../../mate-detection/images/mates/mamarkosich-13.jpeg', 'width': 828, 'height': 868}
def generate_file(img,filename):
    outF = open(filename, "w")
    image_width = img['width']
    image_height = img['height']
    for obj in img['object']:
        if obj['name'] == "mate":
            image_class = "0"
        elif obj['name'] == "calabaza":
            image_class = "1"
        elif obj['name'] == "metal":
            image_class = "2"
        elif obj['name'] == "madera":
            image_class = "3"
        elif obj['name'] == "plastico":
            image_class = "4"

        xmin = obj['xmin']
        xmax = obj['xmax']
        x_center = ((xmax - xmin)/2)/image_width
        width = ((xmax - xmin))/image_width

        ymin = obj['ymin']
        ymax = obj['ymax']
        y_center = ((ymax - ymin)/2)/image_height
        height = ((ymax - ymin))/image_height

        file_line = image_class + " " + str(x_center) + " " + str(y_center) + " " + str(width) + str(height)

        outF.write(file_line)
        outF.write("\n")
    
    outF.close()
 
def leer_annotations(ann_dir, img_dir, labels=[]):
    all_imgs = []
    seen_labels = {}
    
    count = 0
    for ann in sorted(os.listdir(ann_dir)):
        img = {'object':[]}
 
        tree = ET.parse(ann_dir + ann)
        
        for elem in tree.iter():
            if 'filename' in elem.tag:
                img['filename'] = img_dir + elem.text
            if 'width' in elem.tag:
                img['width'] = int(elem.text)
            if 'height' in elem.tag:
                img['height'] = int(elem.text)
            if 'object' in elem.tag or 'part' in elem.tag:
                obj = {}
                
                for attr in list(elem):
                    if 'name' in attr.tag:
                        obj['name'] = attr.text
 
                        if obj['name'] in seen_labels:
                            seen_labels[obj['name']] += 1
                        else:
                            seen_labels[obj['name']] = 1
                        
                        if len(labels) > 0 and obj['name'] not in labels:
                            break
                        else:
                            img['object'] += [obj]
                            
                    if 'bndbox' in attr.tag:
                        for dim in list(attr):
                            if 'xmin' in dim.tag:
                                obj['xmin'] = int(round(float(dim.text)))
                            if 'ymin' in dim.tag:
                                obj['ymin'] = int(round(float(dim.text)))
                            if 'xmax' in dim.tag:
                                obj['xmax'] = int(round(float(dim.text)))
                            if 'ymax' in dim.tag:
                                obj['ymax'] = int(round(float(dim.text)))
 
        if len(img['object']) > 0:
            dir_txt_name = os.path.splitext(img['filename'])[0] + '.txt'
            dir_list = dir_txt_name.split('/')
            last_element = len(dir_list) - 1 
            file_name = dir_list[last_element]

            generate_file(img,file_name)
            all_imgs += [img]
            count += 1
                        
    return all_imgs, seen_labels
 
train_imgs, train_labels = leer_annotations(xml_dir, img_dir, labels)
print('imagenes',len(train_imgs), 'labels',len(train_labels))
print(train_labels)








