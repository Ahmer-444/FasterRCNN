clc
clear all
warning off

% load Annotations.mat
% datapath = 'Faster-RCNN_TF/data/ColorCard/JPEGImages/';
% write_path = 'Faster-RCNN_TF/data/ColorCard/AnnotatedImages/';
% ROIdata = dir(datapath);
% 
% for i=size(Annotations,1)+3:length(ROIdata)
%     i
%     image = strcat(datapath,ROIdata(i).name)
%     I = imread(image);
%     [X,Y,P] = impixel(I);
%     
%     xx = ROIdata(i).name;
%     xx = strsplit(xx,'.');
%     xx = xx(1);
%     temp = [str2num(cell2mat(xx)) size(I,2) size(I,1) X(1) Y(1) X(2) Y(2)];
%     Annotations = [Annotations;temp]
%     save 'Annotations.mat' Annotations
%     wr_image = I(Y(1):Y(2),X(1):X(2),:);
%     wr_path = [ write_path  ROIdata(i).name]
%     imwrite(wr_image,wr_path);
% end



% Annotations = [];
% save 'Annotations.mat' Annotations
 write_path = 'Faster-RCNN_TF/data/ColorCard/AnnotatedImages/';
 

Annotations = [];
load Annotations_ROI.mat
for i=1:size(Annotated_ROI,1)
    i
    image_path = Annotated_ROI.imageFilename{i};
    a =  strsplit(image_path,'/');
    a = cell2mat(a(length(a)));
    b = strsplit(a,'.');
    b = b(1);
    image_num = str2num(cell2mat(b));
    
    rect = Annotated_ROI.card(i,:);
    I = imread(image_path);
    temp = [image_num size(I,2) size(I,1) rect(1) rect(2) rect(1)+rect(3) rect(2)+rect(4)];
    Annotations = [Annotations;temp];
    save 'Annotations.mat' Annotations
    
    wr_image = I(rect(2):rect(2)+rect(4) ,rect(1):rect(1)+rect(3),:);
    wr_path = [ write_path  a]
    imwrite(wr_image,wr_path);
end


% i = imread('/home/ahmer/Color_Calibration/ColorCardTraining/Faster-RCNN_TF/data/ColorCard/JPEGImages/10.jpg');
% figure;
% imshow(i)

