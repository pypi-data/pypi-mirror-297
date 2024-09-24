# Represents the BinaExperts data model,
# which might include all the necessary fields and structures to handle the intermediate format.

class BinaImage:
    def __init__(self, id, width, height, image_name):
        self.id = id
        self.width = width
        self.height = height
        self.image_name = image_name

# Similar classes for categories, annotations, etc.
