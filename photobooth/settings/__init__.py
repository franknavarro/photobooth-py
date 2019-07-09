import configparser
import json
import os


class MyConfigParser(configparser.SafeConfigParser):
    def __init__(self):
        configparser.SafeConfigParser.__init__(self)

        self.filename = 'config.ini';
    
        # Set the default Apperance values
        self['Apperance'] = {
            'mainColor':'#F2AFB0',
            'secondaryColor':'#AFF2F1',
            'fontColor': '#FFFFFF',
            'font': '["Droid", 65, "bold"]
        }

        # Set the default Interaction values
        self['Interactions'] = {
            'imageCountdown': 5,
            'stripCountdown': 15
        }

        # Set the default Photostrip values
        self['Photostrip'] = {
            'folderPath': os.path.expanduser('~/Pictures/Photobooth'),
            'type': 'vertical',
        }

        # Set the default StripVertical values
        self['StripVertical'] = {
            'hasLogo': 'yes',
            'photoCount': 3,
            'paperSize': '[4,6]',
            'border': 0.125
        }

        self.readFromFile()

    def getlist(self, section, subsection):
        return json.loads(self.get(section, subsection))

    def saveToFile(self):
        with open(self.filename, 'w') as configfile:
            self.write(configfile)

    def readFromFile(self):
        self.read(self.filename)



config = MyConfigParser()
config.readFromFile()
