#python ./tools/demo.py --cpu --model /home/ghazanfar/REPOS/Faster-RCNN_TF/VGGnet_fast_rcnn_iter_70000.ckpt

python ./tools/train_net.py --device "cpu" --iters 10000 --imdb "colorcard_train" --network "VGGnet_train" --cfg '/home/ahmer/ColorCardTraining/Faster-RCNN_TF/experiments/cfgs/colorcard.yml' --weights "/home/ahmer/ColorCardTraining/Faster-RCNN_TF/data/pretrain_model/VGG_imagenet.npy"

#python ./tools/train_net.py --device "gpu" --device_id 0 --iters 10000 --imdb "colorcard_train" --network "VGGnet_train" --cfg '/home/ahmer/ColorCardTraining/Faster-RCNN_TF/experiments/cfgs/colorcard.yml' --weights "/home/ahmer/ColorCardTraining/Faster-RCNN_TF/data/pretrain_model/VGG_imagenet.npy"
