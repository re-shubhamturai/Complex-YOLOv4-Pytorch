#!/bin/sh

cd src
# run echo $DISPLAY in your local machine after loging into the hulk and copy the resultant port number below
export DISPLAY=localhost:12.0
echo $DISPLAY

# python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client test.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth --cfgfile /home/src/config/cfg/complex_yolov4.cfg --working_dir /home --show_image

# python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client evaluate.py --gpu_idx 0 --pretrained_path /home/checkpoints/complex_yolov4/complex_yolov4_mse_loss.pth

# python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client train.py --gpu_idx 0 --batch_size 16 --num_workers 20 --mosaic --multiscale_training
python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client train.py --gpu_idx 0 --batch_size 2 --num_workers 4 --resume_path /home/checkpoints/complexer_yolo/Model_complexer_yolo_epoch_5.pth --num_epochs 100
