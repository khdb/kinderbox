import sys, os, time
import string
import logging
import RPi.GPIO as GPIO ## Import GPIO library
import config
import SensorModule
import PlayerModule

PREV = config.PREV
NEXT = config.NEXT
VOLUP = config.VOLUP
VOLDOWN = config.VOLDOWN
TOGGLE = config.TOGGLE

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(PREV, GPIO.IN)
GPIO.setup(NEXT, GPIO.IN)
GPIO.setup(VOLUP, GPIO.IN)
GPIO.setup(VOLDOWN, GPIO.IN)
GPIO.setup(TOGGLE, GPIO.IN)



class Kinderbox4Kids:

    def __init__(self):
        self.playlist_dir =  config.playlist_dir
        self.rfid_map_file = config.rfid_map_file
        self.rfid_map = []

        self.sensor = SensorModule.Sensor()
        self.player = PlayerModule.Player()

        self.logger = logging.getLogger('kinderbox')
        hdlr = logging.FileHandler('/var/log/kinderbox/kinderbox.log')
        formatter = logging.Formatter ('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.WARNING)

    def load_rfid_map(self):
        print "loading %s" % self.rfid_map_file
        if not os.path.exists(self.rfid_map_file):
            print "could not open %s" % self.rfid_map_file
            return
        self.rfid_map = []
        for line in open(self.rfid_map_file, 'r'):
            data = line.strip()
            if len(data) > 0:
                index = data.find('=')
                if index > 0:
                    rfid = data[0:index]
                    barcode = data[index+1:]
                    self.rfid_map.append((rfid, barcode))

    def get_barcode_by_rfid(self, rfid):
        for (rf,bc) in self.rfid_map:
            if rfid == rf:
                return bc
        return


    def run(self):
        self.load_rfid_map()
        print "connect to serial ..."
        self.sensor.open()
        current_barcode = ""
        print "Huy Testing"
        prev_input = None
        last_ms = time.time()
        try:
            while 1:
                #Read button state
                input =  None
                if(GPIO.input(PREV)):
                    input = "PREV"
                if(GPIO.input(NEXT)):
                    input = "NEXT"
                if(GPIO.input(VOLUP)):
                    input = "VOLUP"
                if(GPIO.input(VOLDOWN)):
                    input = "VOLDOWN"
                if(GPIO.input(TOGGLE)):
                    input = "TOGGLE"
                if ((not prev_input) and input):
                    self.player.process_button(input)
                prev_input = input
                #Read rfid card
                rfid = self.sensor.get_rfid_code()
                if (rfid != None):
                    barcode = self.get_barcode_by_rfid(rfid)
                    if barcode != None:
                        if current_barcode != barcode:
                            current_barcode = barcode
                            self.player.load_playlist(barcode)
                time.sleep(0.1)
                current_ms = time.time()

                #Update display each  0.5ms:
                if (current_ms - last_ms) > 2:
                    last_ms = current_ms
                    self.player.get_play_status()
        except IOError:
            self.logger.error('An error occured trying to read the file.')
        except KeyboardInterrupt:
            self.sensor.close()
        except Exception, err:
            self.logger.exception("An exception occured: ")
        self.sensor.close()

def main(argv):
    kinderbox = Kinderbox4Kids()
    kinderbox.run()

if __name__ == "__main__":
    main(sys.argv[1:])


