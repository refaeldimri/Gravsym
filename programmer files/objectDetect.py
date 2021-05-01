from imageai.Detection.Custom import CustomObjectDetection

# put a photo in same folder

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("model") # model name
detector.setJsonPath("detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image="photo.jpg",#photo name
 output_image_path="holo3-detected.jpg")
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
