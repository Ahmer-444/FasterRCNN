import sys;
PY_VER = sys.version_info[0];

import _init_paths
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2';
import tensorflow as tf
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import sys,shutil, cv2, natsort
import argparse, csv
from networks.factory import get_network
import cc_config


from transform import four_point_transform
import imutils
import scipy.io

CLASSES = cc_config.CLASSES;
input_dir = cc_config.INPUT_DIR
output_dir = cc_config.OUTPUT_DIR


bboxes = dict();

ground = cc_config.ground_truth;

miss_cls = 0;
miss_det = 0;


confusion_matrix = [ [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0] ] ;

csvfile = open('log.csv', "w");
fieldnames = ['Image Path', 'Ground Truth', 'Predicted'];
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()


class MyValidationError(Exception):
    pass

def calccolortransform(col):
    print os.getcwd()
    mat = scipy.io.loadmat('colact.mat')
    colact = mat['colact']
    colact.shape
    col.shape    
    #colactG = colact.reshape(4,6,3)
    #colG = col.reshape(4,6,3)
    
    if not colact.shape == col.shape:
        raise MyValidationError("test and reference data must be same size and shape")

    MactAll = colact.T
    MrawAll = col.T
    
    #Mcorrpseudo = (MactAll * MrawAll.T) / (MrawAll * MrawAll.T)
    t1 = np.dot(MactAll,MrawAll.T)
    t1 = t1.astype(float)
    t2 = np.dot(MrawAll,MrawAll.T)
    t2 = t2.astype(float)
    t2 = np.linalg.inv(t2)
    
    Mcorrpseudo = np.dot(t1,t2)
    return Mcorrpseudo





def filter_and_drawbboxes(im, class_name, dets, image_name, thresh=0.5):
    global bboxes;
    """Draw detected bounding boxes."""
    
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    # save_dir = os.path.join(output_dir, class_name)
    # if not os.path.isdir(save_dir):
    #     os.mkdir(save_dir)
    # save_path = os.path.join(save_dir, image_name)
    # shutil.copy(os.path.join(input_dir, image_name), save_path)
    cropped = [];
    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        score = round(score, 4);

        if PY_VER == 3:
	        if class_name not in bboxes:
	            bboxes[class_name] = (score, bbox);
	        else:
	            if bboxes[class_name][0] < score:
	                bboxes[class_name] = (score, bbox);
        else:
        	if not bboxes.has_key(class_name):
	            bboxes[class_name] = (score, bbox);
	        else:
	            if bboxes[class_name][0] < score:
	                bboxes[class_name] = (score, bbox);

        #print('Score = ' + str(score));
        #cropped = im[ int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2]) ].copy();

        #cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), ( int(bbox[2]), int(bbox[3])), (255,0,0), 2)
        #cv2.putText(im, class_name + ' : ' + str(score), (int(bbox[0]), int(bbox[1]-2)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))
        #cv2.putText(im, class_name + ' : ' + str(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0));

    #cv2.imwrite(os.path.join(output_dir + '/cropped/', image_name), cropped);
    #cv2.imwrite(os.path.join(output_dir, image_name), im)

def detect_objects(sess, net, image_name):
    global bboxes, ground, miss_cls, miss_det;
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(input_dir, image_name)
    #im_file = os.path.join('/home/corgi/Lab/label/pos_frame/ACCV/training/000001/',image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(sess, net, im)
    timer.toc()

    out = 'Detection took {:.3f}s for {:d} object proposals'.format(timer.total_time, boxes.shape[0]);
    print (out);

    # Visualize detections for each class
    #im = im[:, :, (2, 1, 0)]
    # fig, ax = plt.subplots(figsize=(12, 12))
    # ax.imshow(im, aspect='equal')

    CONF_THRESH = 0.3
    NMS_THRESH = 0.3
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        filter_and_drawbboxes(im, cls, dets, image_name, thresh=CONF_THRESH)

    sboxes = sorted(bboxes.items(), key=lambda x: x[1][0])
    
    if len(sboxes) == 0:
        miss_det += 1;
        bboxes = {};
        return;

    bbox = sboxes[-1][1][1];
    score = sboxes[-1][1][0];
    class_name = sboxes[-1][0];

    

    #img_name_i = 0;#int(image_name[:-4]);

    #actual_class_idx = 0;

    #for idx, i in enumerate(cc_config.ranges):
    #    if img_name_i in i:
    #        actual_class_idx = idx;

    #actual_class_name = cc_config.class_indices_inv[actual_class_idx];


    #predicted_class_idx = cc_config.class_indices[class_name];

    #confusion_matrix[actual_class_idx][predicted_class_idx] += 1;

    #writer.writerow({'Image Path': image_name, 'Ground Truth': actual_class_name, 'Predicted' : class_name});
    
    #if img_name_i not in ground[class_name]:
    #    miss_cls += 1;
        #cv2.putText(im, 'x', (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255));
    

    ##### ____ AHMER ____ ####
    BBOX = bbox	
    #cv2.rectangle(im, (int(bbox[0]), int(bbox[1])), ( int(bbox[2]), int(bbox[3])), (255,0,0), 2)
    #cv2.putText(im, class_name + ' : ' + str(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0));
    #cv2.imwrite(os.path.join(output_dir, image_name), im)
    bboxes = {};
    return BBOX

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        default='VGGnet_test')
    parser.add_argument('--model', dest='model', help='Model path',
                        default=' ')
    parser.add_argument('--image', dest='im_name', required=True, help="path to the input image")
    parser.add_argument('--output', dest='out', required=True, help='"path to the output image"')

    
    args = parser.parse_args()

    return args

    
if __name__ == '__main__':
    
    args = parse_args()

    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = parse_args()

    model = cc_config.MODEL
    if model == ' ':
        raise IOError(('Error: Model not found.\n'))
        
    # init session
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = get_network(cc_config.TESTING_NETWORK_NAME)


    # load model
    saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
    saver.restore(sess, model)


    #saver = tf.train.import_meta_graph(model+'.meta')
    #saver.restore(sess, model)


    print('\n\nLoaded network {:s}'.format(model));

    # Warmup on a dummy image
    im = 128 * np.ones((640, 480, 3), dtype=np.uint8)
    for i in range(2):
        _, _= im_detect(sess, net, im)


    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Demo for /{}'.format(args.im_name))
    bbox = detect_objects(sess, net, args.im_name)

    if bbox is None:
    	raise MyValidationError("No Amazon Card Found")
    else:
    	image = cv2.imread(args.im_name)
    	detected_card = image[int(bbox[1]):int(bbox[3]),int(bbox[0]) : int(bbox[2]), : ]

    	rm_width = 0.06
    	rm_height = 0.21
    	(h,w,d) = detected_card.shape
    	detected_card2 = detected_card[int(rm_width*w):int(h-(h*rm_height)),int(rm_width*w):int(w-rm_width*w),:]
    	(rr,cc,dd) = detected_card2.shape

    	XX = np.arange(0.125,1.0,0.25)
    	XX = np.tile(XX, 6)
    	XX = XX * cc
    	XX = XX.astype(int)

    	YY = np.arange(0.0833,1,0.1667)
    	YY = np.repeat(YY, 4)
    	YY = YY * rr
    	YY = YY.astype(int)

    	font = cv2.FONT_HERSHEY_SIMPLEX
    	BGR_VALUES = np.array([],dtype='int')

    	for i in range(0,24):
    		temp = detected_card2[YY[i],XX[i],:]
    		BGR_VALUES = np.concatenate((BGR_VALUES,temp))
    		#print BGR_VALUES
    		cv2.putText(detected_card2,'o',(XX[i],YY[i]), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    		#cv2.imshow('temp',detected_card2)
    		#cv2.waitKey(0)

    	RGB = BGR_VALUES.reshape(24,3)
    	RGB[:,[0, 2]] = RGB[:,[2, 0]]
    	Mcorrpseudo = calccolortransform(RGB)

    	A = image;
    	[rA,cA,dA] = A.shape
    	x = A.swapaxes(0,2).swapaxes(1,2)
    	x1 = x.reshape(dA,rA*cA,order='F')
    	x1 = x1.astype('float')

    	#Mcorrpseudo = np.array([[ 0.9725 ,0.0627 ,0.2296],[-0.0762,1.0738,0.0921],
    	#                       [-0.0486,-0.1488,1.2403 ]])
    	out = np.round(np.dot(Mcorrpseudo,x1))
    	out = out.T
    	out = out.astype('int')
    	corrected_image = out.reshape(rA,cA,dA,order='F')
    	print "calibrated Image has been written"
    	cv2.imwrite(args.out,corrected_image)

     	# Converts to grey for better reulsts

    	# gray = cv2.cvtColor(detected_card, cv2.COLOR_BGR2GRAY)

    	# # Converts to HSV
    	# hsv = cv2.cvtColor(detected_card, cv2.COLOR_BGR2HSV)

    	# # HSV values
    	# lower_skin = np.array([80,0,0])     ## 100 - 120
    	# upper_skin = np.array([140,255,255])

    	# mask = cv2.inRange(hsv, lower_skin, upper_skin)

    	# mask = cv2.erode(mask, None, iterations=2)
    	# mask = cv2.dilate(mask, None, iterations=2)

    	# # Finds contours
    	# im2, cnts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	# cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    	# # Draws contours
    	# for c in cnts:
    	#     if cv2.contourArea(c) < 3000:
    	#         continue
    	    
    	#     (x, y, w, h) = cv2.boundingRect(c)
    	#     #cv2.rectangle(image, (x,y), (x+w,y+h), (0, 255, 0), 2)
    	#      ## BEGIN - draw rotated rectangle
    	#     rect = cv2.minAreaRect(c)
    	#     box = cv2.boxPoints(rect)
    	#     box = np.int0(box)
    	#     cv2.drawContours(image,[box],0,(0,255,0),2)
    	#     ## END - draw rotated rectangle       
    	#     break


    
    	








    '''
    total_images = len(im_names);

    err_det = 100.0 * float(miss_det) / total_images;
    acc_det = 100.0 - err_det;

    print('Mis-detections = ' + str(miss_det) + ' / ' + str(total_images) + ' = ' + str(err_det) + '%');

    print('Detection Accuracy = ' + str(acc_det));

    detection_count = total_images - miss_det;

    err_cls = 100.0 * float(miss_cls) / total_images;

    print('Miss-classifications = ' + str(miss_cls) + ' / ' + str(total_images) + ' = ' + str(err_cls) + '%');

    acc_cls = 100 - err_cls;
    acc_cls = round(acc_cls, 4);
    
    print('Classification Accuracy = ' + str(acc_cls));

    confusion_matrix = np.array(confusion_matrix);

    print('\n\nConfusion Matrix:\n')
    print(confusion_matrix);
    ''' 

