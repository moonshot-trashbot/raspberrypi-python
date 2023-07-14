import json

class CustomizedTestingInput:
    def __init__(self, data):
        self.TrackID = data["TrackID"]
        self.Confidence = data["Confidence"]
        self.ClassID = data["ClassID"]
        self.Left = data["Left"]
        self.Right = data["Right"]
        self.Top = data["Top"]
        self.Bottom = data["Bottom"]
        self.Center = data["Center"]

class SendableDetection:
    def __init__(self, data):
        self.id = data["id"]
        self.frame = data["frame"]
        self.type = data["type"]
        self.left = data["left"]
        self.right = data["right"]
        self.top = data["top"]
        self.bottom = data["bottom"]
        self.center = data["center"]
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __str__(self):
        build = "SENDABLE DETECTION"
        build += "\n\tID: " + str(self.id)
        build += "\n\tFrame: " + str(self.frame)
        build += "\n\tType: " + str(self.type)
        build += "\n\tLeft: " + str(self.left)
        build += "\n\tRight: " + str(self.right)
        build += "\n\tTop: " + str(self.top)
        build += "\n\tBottom " + str(self.bottom)
        build += "\n\tCenter " + str(self.center)
        build += "\n"
        return build

class ReceivedDetection:
    def __init__(self, data):
        self.id = data["id"]
        self.frame = data["frame"]
        self.type = data["type"]
        self.left = data["left"]
        self.right = data["right"]
        self.top = data["top"]
        self.bottom = data["bottom"]
        self.center = data["center"]
    def __str__(self):
        build = "RECEIVED DETECTION"
        build += "\n\tID: " + str(self.id)
        build += "\n\tFrame: " + str(self.frame)
        build += "\n\tType: " + str(self.type)
        build += "\n\tLeft: " + str(self.left)
        build += "\n\tRight: " + str(self.right)
        build += "\n\tTop: " + str(self.top)
        build += "\n\tBottom " + str(self.bottom)
        build += "\n\tCenter " + str(self.center)
        build += "\n"
        return build