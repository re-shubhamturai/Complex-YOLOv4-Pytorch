all: build

build:
	# docker build --tag complex-yolov4:latest --target debug -f Dockerfile .
	docker build --tag complex-yolov4:latest -f Dockerfile .

debug-build:
	docker build --tag complex-yolov4:latest --target debug -f Dockerfile .
	# docker build --tag complex-yolov4:latest -f Dockerfile .

run:
	docker stop $(docker ps --filter="name=mfund-complex-yolov4" --format '{{.Names}}') || true
	docker rm mfund-complex-yolov4 || true
	docker run --runtime=nvidia --name mfund-complex-yolov4 -v ${PWD}:/home -p 5678:5678 -v /disk/mfund/kitti/training/:/home/dataset/kitti/training:ro -v /disk/mfund/kitti/testing/:/home/dataset/kitti/testing:ro complex-yolov4:latest
	