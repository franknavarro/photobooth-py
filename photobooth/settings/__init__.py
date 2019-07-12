import configparser
import json
import os
from .constants import systemFonts


class MyConfigParser(configparser.SafeConfigParser):
    def __init__(self):
        configparser.SafeConfigParser.__init__(self)

        self.filename = 'config.ini';
    
        # Set the default Apperance values
        self['Apperance'] = {
            'mainColor':'#F2AFB0',
            'mainFontFamily': systemFonts[0],
            'mainFontSize': 65,
            'mainFontSettings': 'bold',
            'mainFontColor': '#FFFFFF',

            'secondaryColor':'#AFF2F1',
            'secondaryFontFamily': systemFonts[0],
            'secondaryFontSize': 45,
            'secondaryFontSettings': 'bold',
            'secondaryFontColor': '#FFFFFF'
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

    def getFont(self, typeF):
        fontTuple = (
            self.get('Apperance', typeF+'FontFamily'),
            self.get('Apperance', typeF+'FontSize'),
            self.get('Apperance', typeF+'FontSettings')
        )
        fontColor = self.get('Apperance', typeF+'FontColor')
        return (fontTuple, fontColor)

    def getlist(self, section, subsection):
        return json.loads(self.get(section, subsection))

    def saveToFile(self):
        with open(self.filename, 'w') as configfile:
            self.write(configfile)

    def readFromFile(self):
        self.read(self.filename)



config = MyConfigParser()
config.readFromFile()
