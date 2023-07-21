import json

class FakeInput:
    def __init__(self, data):
        self.TrackID = data["TrackID"]
        self.Confidence = data["Confidence"]
        self.ClassID = data["ClassID"]
        self.Left = data["Left"]
        self.Right = data["Right"]
        self.Top = data["Top"]
        self.Bottom = data["Bottom"]
        self.Center = data["Center"]

class Detection:
    def __init__(self, data):
        self.id = data["id"]
        self.frame = data["frame"]
        self.type = data["type"]
        self.center = data["center"]
        self.left = data["left"]
        self.right = data["right"]
        self.top = data["top"]
        self.bottom = data["bottom"]

        self.width = abs(1280-self.left-self.right)
        self.height = abs(720-self.top-self.bottom)
        self.area = abs(self.width * self.height)
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
        build += "\n\tWidth " + str(self.width)
        build += "\n\tHeight " + str(self.height)
        build += "\n\tArea " + str(self.area)
        build += "\n"
        return build