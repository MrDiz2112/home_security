import os


class FaceDetectionConfig:
    # cascade_path = r"C:\Users\diz20\Documents\_Programming\Projects\home_security\haarcascade_frontalface_default.xml"

    script_dir = os.path.dirname(os.path.realpath(__file__))
    cascade_path = os.path.join('haarcascade_frontalface_default.xml')

    cascade_path = os.path.abspath(cascade_path)
