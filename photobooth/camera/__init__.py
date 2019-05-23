import picamera

class Camera(picamera.PiCamera):
    def __init__(self, resolution):
        picamera.PiCamera.__init__(self)

        self.resolution = resolution
        self.rotation              = 0
        self.hflip                 = True
        self.vflip                 = False
        self.brightness            = 50
        self.preview_alpha = 120
        self.preview_fullscreen = True
        #self.framerate             = 24
        #self.sharpness             = 0
        #self.contrast              = 8
        #self.saturation            = 0
        #self.ISO                   = 0
        #self.video_stabilization   = False
        #self.exposure_compensation = 0
        #self.exposure_mode         = 'auto'
        #self.meter_mode            = 'average'
        #self.awb_mode              = 'auto'
        #self.image_effect          = 'none'
        #self.color_effects         = None
        #self.crop                  = (0.0, 0.0, 1.0, 1.0)

    def start(self):
        print("Starting Camera Feed...")
        print("Camera Resolution at ",self.resolution)
        self.start_preview()

    def stop(self):
        print("Stoping Camera Feed...")
        self.stop_preview()

