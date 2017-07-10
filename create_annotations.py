from xml.dom import minidom;
import os
import scipy.io

os.chdir('/home/ahmer/Color_Calibration/ColorCardTraining')
mat = scipy.io.loadmat('Annotations.mat')
Annotations = mat['Annotations']

ann_dir = 'Faster-RCNN_TF/data/colorcard/Annotations/'
FolderName = "colorcard"
ClassName = "amazoncolorcard"
dim = '3'

for _i in Annotations:
    onlyname = str(_i[0])+'.jpg'
    _w = str(_i[1])
    _h = str(_i[2])
     
    _xmin = str(_i[3])
    _ymin = str(_i[4])
    _xmax = str(_i[5])
    _ymax = str(_i[6])
    
    doc = minidom.Document();
    declaration = doc.toxml()
    annotation = doc.createElement("annotation");

    folder = doc.createElement("folder");
    folder.appendChild(doc.createTextNode(FolderName))

    annotation.appendChild(folder);

    filename = doc.createElement("filename");
    filename.appendChild(doc.createTextNode(onlyname))

    size = doc.createElement("size");
		
    width = doc.createElement('width');
    height = doc.createElement('height');
    depth = doc.createElement('depth');

    width.appendChild(doc.createTextNode(_w));
    height.appendChild(doc.createTextNode(_h));
    depth.appendChild(doc.createTextNode(dim));

    size.appendChild(width);
    size.appendChild(height);
    size.appendChild(depth);

    annotation.appendChild(filename);
    annotation.appendChild(size);

    obj = doc.createElement("object");
    bndbox = doc.createElement("bndbox");
    
    class_name = doc.createElement("name");
    class_name.appendChild(doc.createTextNode(ClassName));



    xmin = doc.createElement("xmin");
    xmin.appendChild(doc.createTextNode(_xmin))
    ymin = doc.createElement("ymin");
    ymin.appendChild(doc.createTextNode(_ymin))
    xmax = doc.createElement("xmax");
    xmax.appendChild(doc.createTextNode(_xmax))
    ymax = doc.createElement("ymax");
    ymax.appendChild(doc.createTextNode(_ymax))

    bndbox.appendChild(xmin);
    bndbox.appendChild(ymin);
    bndbox.appendChild(xmax);
    bndbox.appendChild(ymax);

    obj.appendChild(class_name);
    obj.appendChild(bndbox);

    annotation.appendChild(obj);

    doc.appendChild(annotation);

    f = open(ann_dir + str(_i[0]) + '.xml', 'w');
    print ann_dir + str(_i[0]) + '.xml'
    x = annotation.toprettyxml()#[len(declaration) + 1:]
    f.write(x);
    
