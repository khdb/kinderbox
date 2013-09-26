import sys, os, time
import string
import logging
import RPi.GPIO as GPIO ## Import GPIO library
import config
import SensorModule
import PlayerModule
import LCDModule
import LoggerModule

sys.path.append("/home/pi/db")
import DBModule

PREV = config.PREV
NEXT = config.NEXT
VOLUP = config.VOLUP
VOLDOWN = config.VOLDOWN
TOGGLE = config.TOGGLE

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(PREV, GPIO.IN)
GPIO.setup(NEXT, GPIO.IN)
GPIO.setup(VOLUP, GPIO.IN)
GPIO.setup(VOLDOWN, GPIO.IN)
GPIO.setup(TOGGLE, GPIO.IN)



class Kinderbox4Kids:

    def __init__(self):
        self.playlist_dir =  config.playlist_dir

        self.sensor = SensorModule.Sensor()
        self.player = PlayerModule.Player()
        self.lcd = LCDModule.LCD()
        self.logger = LoggerModule.Logger()
        self.db = DBModule.DBUtils()


    def kill_reading_rfid(self):
        cmd = "sudo pkill -9 -f enableScanRFID.py"
        os.system(cmd)
        cmd = "sudo pkill -9 -f readingRFID.py"
        os.system(cmd)

    def update_lcd_now(self):
        info = self.player.get_play_status()
        #Pause
        if info[0] == 1:
            self.lcd.display_pause()
        #Playing
        elif info[0] == 2:
            self.lcd.message(info[1], info[2], True)
        #Not active
        else:
            self.lcd.display_ready()



    def run(self):
        self.kill_reading_rfid()
        self.sensor.open()
        current_barcode = ""
        prev_input = None
        self.lcd.hello()
        get_status_ms = time.time()
        display_lcd_ms = time.time()
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
                    if input == "VOLDOWN" or input == "VOLUP":
                        message = self.player.get_volume()
                        self.lcd.display_volume(message)
                    else:
                        self.update_lcd_now()
                prev_input = input
                #Read rfid card
                rfid = self.sensor.get_rfid_code()
                if (rfid != None):
                    info = self.db.get_item_by_rfid(rfid)
                    if info is not None:
                        barcode = info[1]
                        album = info[2]
                        if barcode != None:
                            if current_barcode != barcode:
                                print "barcode id = %s" %barcode
                                current_barcode = barcode
                                self.player.set_album(album)
                                self.player.load_playlist(barcode)
                time.sleep(0.1)
                current_ms = time.time()

                #Update display each  0.5ms:
                if (current_ms - get_status_ms) > 3:
                    get_status_ms = current_ms
                    info = self.player.get_play_status()
                    #Pause
                    if info[0] == 1:
                        self.lcd.display_pause()
                    #Playing
                    elif info[0] == 2:
                        self.lcd.message(info[1], info[2])
                    #Not active
                    else:
                        self.lcd.display_ready()

                if (current_ms - display_lcd_ms) > 1:
                    display_lcd_ms = current_ms
                    self.lcd.scroll_to_left()
        except IOError:
            self.logger.error('An error occured trying to read the file.')
            os.system("mpc stop")
        except Exception, err:
            self.logger.exception("An exception occured: %s" %err)
        finally:
            self.sensor.close()
            self.lcd.turn_off()
            os.system("mpc stop")

def main(argv):
    kinderbox = Kinderbox4Kids()
    kinderbox.run()

if __name__ == "__main__":
    main(sys.argv[1:])



