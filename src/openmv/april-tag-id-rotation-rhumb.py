# This source is capabale of detecting apriltags and returns Id, Angle of rotation and Rhumb.
# The output

import sensor, image, time, math, pyb

# Init serial over USB
usb_vcp = pyb.USB_VCP()
usb_vcp.setinterrupt(-1)

sensor.reset()
# Color
sensor.set_pixformat(sensor.RGB565)
# Highest possible res for the current memory
sensor.set_framesize(sensor.VGA)
# Zoom in on a center part of the image
sensor.set_windowing((160, 120))
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()

rhumbs = [
    (0,"N"),
    (45,"NE"),
    (90,"E"),
    (135,"SE"),
    (180,"S"),
    (225,"SW"),
    (270,"W"),
    (315,"NW"),
    (360,"N")
    ]

# Checks if a given number is within a 45 units range of a matching number
def IsInRange(rotation, angle):
    if(angle < rotation+22.5 and angle > rotation-22.5):
        return True
    else:
        return False

# Retrieves a rhumb based on rotation angle
def GetRhumb(rotation):
    for key, value in rhumbs:
        if(IsInRange(rotation, key)):
            return value



while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(): # default settings finds only TAG36H11 types
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

        correction = 180
        rotation = (correction * tag.rotation()) / math.pi
        rhumb = GetRhumb(rotation)
        output_args = (tag.id(),rotation, rhumb)

        # Print can be used for development purpose
        #print("%d, %f, %s" % output_args)
        usb_vcp.send("%d, %f, %s\n" % output_args, timeout=0)




