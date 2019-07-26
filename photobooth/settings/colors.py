# This file contains helper function for computing colors
# and converting them to different color spaces as well
# as a function to find the complimentary color of a hex color


# Find the complimenatry hex color of the hex color passed in
def hex_complimentary(startHex):
    #print("COMPUTING COMPLIMENTARY COLOR FROM HEX: ", startHex)
    # Convert hex to hsl
    hsl = hex_hsl(startHex)
    # Get complimentary color by moving the hue 180 degrees (1/2 of 360 degrees)
    newHue = hsl[0] + 0.5
    if( newHue > 1 ):
        newHue -= 1
    newHSL = (newHue, hsl[1], hsl[2])
    #print("COMPLIMENTARY HSL: ", newHSL)
    # Convert back to hex color
    newHex = hsl_hex(newHSL)
    #print("NEW HEX: ", newHex)
    # Set the new complimentary color
    return newHex

def hex_lighten(hexcolor, lightenAmount):
    # Convert the color to hsl to lighten or darken
    hsl = hex_hsl(hexcolor)
    # Adjust the lightness value
    newLight = hsl[2] + lightenAmount
    newHSL = (hsl[0], hsl[1], newLight)
    # Convert back to hex
    newHex = hsl_hex(newHSL)
    return newHex


# Helper function for hsl_rgb()
def hue_rgb(var1, var2, varHue):
    # Make sure that the hue is within 0 - 1
    if( varHue < 0 ):
        varHue += 1
    elif( varHue > 1 ):
        varHue -= 1

    # Convert Hue to RGB number represented as a decimal
    if( (6 * varHue) < 1 ):
        rgbDec = var1 + (var2 - var1) * 6 * varHue
    elif( (2 * varHue) < 1 ):
        rgbDec = var2
    elif( (3 * varHue) < 2 ):
        rgbDec = var1 + (var2 - var1) * ((2/3 - varHue) * 6)
    else:
        rgbDec = var1

    #print("VAR1: ", var1)
    #print("VAR2: ", var2)
    #print("VARHUE: ", varHue)
    #print("RGB DECIMAL: ", rgbDec)
    # Return the rgb value in range of 1 - 255
    return round(255 * rgbDec)


# Convert a color from HSL to RGB
def hsl_rgb(hslColor):
    # If the saturation is 0 then just set luminence as the rgb colors
    if( hslColor[1] == 0 ):
        redNum = int(hslColor[2] * 255)
        greenNum = int(hslColor[2] * 255)
        blueNum = int(hslColor[2] * 255)
    else:
        if( hslColor[2] < 0.5 ):
            var2 = hslColor[2] * (1 + hslColor[1])
        else:
            var2 = (hslColor[2] + hslColor[1]) - (hslColor[1] * hslColor[2])

        var1 = 2 * hslColor[2] - var2
        redNum = hue_rgb(var1, var2, hslColor[0]+1/3)
        greenNum = hue_rgb(var1, var2, hslColor[0])
        blueNum = hue_rgb(var1, var2, hslColor[0]-1/3)

    returnRGB = (redNum, greenNum, blueNum)
    #print("HSL -> RGB: ", hslColor, " -> ", returnRGB)
    return returnRGB


# Convert a color from RGB to Hexidecimal
def rgb_hex(rgbColor):
    # Get hexidecimal number for red
    redHex = hex(rgbColor[0])[2:]
    if( len(redHex) == 1 ):
        redHex = "0" + redHex
    # Get hexidecimal number for green
    greenHex = hex(rgbColor[1])[2:]
    if( len(greenHex) == 1 ):
        greenHex = "0" + greenHex
    # Get hexidecimal number for blue
    blueHex = hex(rgbColor[2])[2:]
    if( len(blueHex) == 1 ):
        blueHex = "0" + blueHex

    returnHex = ("#" + redHex + greenHex + blueHex).upper()
    #print("RGB -> HEX: ", rgbColor, " -> ", returnHex)
    return returnHex


# Convert a color from HSL to Hex
def hsl_hex(hslColor):
    newRGB = hsl_rgb(hslColor)
    newHex = rgb_hex(newRGB)
    return newHex


# Convert a color from Hex to RGB
def hex_rgb(hexColor):
    # Split the hex string into its color parts
    redHex = hexColor[1:3]
    greenHex = hexColor[3:5]
    blueHex = hexColor[5:7]
    # Convert the hex colors to rbg colors
    redNum = int(redHex, 16) 
    greenNum = int(greenHex, 16) 
    blueNum = int(blueHex, 16) 

    returnRGB = (redNum, greenNum, blueNum)
    #print("HEX -> RGB: ", hexColor, " -> ", returnRGB)
    return returnRGB


# Convert a color from RGB to HSL
def rgb_hsl(rgbColor):
    redFrac = rgbColor[0] / 255
    greenFrac = rgbColor[1] / 255
    blueFrac = rgbColor[2] / 255
    minNum = min(redFrac, greenFrac, blueFrac)
    maxNum = max(redFrac, greenFrac, blueFrac)
    diffNum = maxNum - minNum
    luminence = (maxNum + minNum) / 2
    if ( diffNum == 0 ):
        hue = 0
        saturation = 0
    else:
        # Change the formula used for saturation depending on if luminence
        # is less than 0.5
        if( luminence < 0.5 ):
            saturation = diffNum / (maxNum + minNum)
        else:
            saturation = diffNum / (2 - maxNum - minNum)
        # Formulas used in calculating the hue
        diffRed = (((maxNum - redFrac) / 6) + (diffNum / 2)) / diffNum
        diffGreen = (((maxNum - greenFrac) / 6) + (diffNum / 2)) / diffNum
        diffBlue = (((maxNum - blueFrac) / 6) + (diffNum / 2)) / diffNum
        # Depending on which rgb color is the max use a different formula
        if( redFrac == maxNum ):
            hue = diffBlue - diffGreen
        elif( greenFrac == maxNum):
            hue = (1/3) + diffRed - diffBlue
        elif( blueFrac == maxNum):
            hue = (2/3) + diffGreen - diffRed
        # When hue is less then zero or more than 1 rotate it 360 degrees
        if( hue < 0 ):
            hue += 1
        elif( hue > 1 ):
            hue -= 1

    returnHSL = (hue, saturation, luminence)
    #print("RGB -> HSL: ", rgbColor, " -> ", returnHSL)
    return returnHSL 


# Convert a color from hexidecimal to HSL
def hex_hsl(hexColor):
    rgb = hex_rgb(hexColor)
    return rgb_hsl(rgb)

