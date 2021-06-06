def draw_boxes(image, boxes, labels):
    image_h, image_w, _ = image.shape
 
    for box in boxes:
        xmin = int(box.xmin*image_w)
        ymin = int(box.ymin*image_h)
        xmax = int(box.xmax*image_w)
        ymax = int(box.ymax*image_h)
 
        cv2.rectangle(image, (xmin,ymin), (xmax,ymax), (0,255,0), 3)
        cv2.putText(image, 
                    labels[box.get_label()] + ' ' + str(box.get_score()), 
                    (xmin, ymin - 13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1e-3 * image_h, 
                    (0,255,0), 2)
        
    return image  


mejores_pesos = "pesos-primer-entrenamiento"
image_path = "mate1.png"
 
mi_yolo = YOLO(input_size          = tamanio, 
            labels              = labels, 
            max_box_per_image   = 5,
            anchors             = anchors)
 
mi_yolo.load_weights(mejores_pesos)
 
image = cv2.imread(image_path)
boxes = mi_yolo.predict(image)
image = draw_boxes(image, boxes, labels)
 
print('Detectados', len(boxes))
 
cv2.imwrite(image_path[:-4] + '_detected' + image_path[-4:], image)