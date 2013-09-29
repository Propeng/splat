from display.framebuffer import Framebuffer
import random, time

class Display:
    def __init__(self, config):
        self.config = config
        self.fb = Framebuffer(self.config.fb_device)
        self.fb.configure()
        lmao = 0
        self.maxBatt = int(open('/sys/class/power_supply/battery/voltage_max_design', 'r').read().strip('\n'))
        self.minBatt = int(open('/sys/class/power_supply/battery/voltage_min_design', 'r').read().strip('\n'))
        while True:
           lmao += 4
           if lmao > 250:
           	lmao = 0
           #ts = time.time()
           self.fb.reset()
           #print(1/(time.time()-ts))
           #print("drawing square")
           #self.fb.rect(x=2, y=1, w=25, h=2, rgba=[random.randrange(0,255),random.randrange(0, 255),random.randrange(0, 255)])
           #self.fb.rect(x=lmao, y=25+lmao, w=400, h=400, rgba=[random.randrange(0,255),random.randrange(0, 255),random.randrange(0, 255)])
           self.fb.rect(x=0, y=0, w=self.config.width, h=self.config.height, rgba=[255, 255, 255])
           self.fb.rect(x=0, y=0, w=self.config.width, h=50, rgba=[150, 150, 150])
           if open('/sys/class/power_supply/battery/status', 'r').read().strip('\n') == 'Charging':
           	batterycolor = [255, 0, 0]
           elif open('/sys/class/power_supply/battery/status', 'r').read().strip('\n') == 'Full':
           	batterycolor = [0, 255, 0]
           else:
           	batterycolor = [100, 200, 255]
           max = self.maxBatt
           batt = int(open('/sys/class/power_supply/battery/voltage_now', 'r').read().strip('\n'))
           percentage = (batt / max)
           print('Battery is %d full, %s %s' % ((int(percentage*100)), str(percentage), str(batt - max)))
           self.fb.rect(x=self.config.width-20, y=10, w=10, h=30, rgba=batterycolor)
           #self.fb.rect(x=255+lmao, y=295, w=90, h=90, rgba=[random.randrange(0,255),random.randrange(0, 255),random.randrange(0, 255)])
           #print(1/(time.time()-ts))
           #print("updating screen")
           self.fb.update()
           time.sleep(1/60.0)
           #print("updating screen done")
        