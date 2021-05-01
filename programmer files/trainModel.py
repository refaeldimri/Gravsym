from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="hololens")# dataSet path on drive
trainer.setTrainConfig(object_names_array=["hololens"],# Symbol name
 batch_size=4,
 num_experiments=100,
 train_from_pretrained_model="pretrained-yolov3.h5")

trainer.trainModel()
