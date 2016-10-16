import serial
from time import sleep

SERIAL_PORT = '/dev/ttyAMA0'
HANDSHAKE_CODE = '0'
REQUEST_CODE = '1'
RESET_CODE = '2'
START_SENSOR_CODE = '3'


def convert_to_float(raw, divisor):
    return float(raw)/divisor


# Only Part1 of the class interfaces with the hardware access. Any change to the hardware tech stack should be contained
# inside Part1.

class Comm(object):
    msg_format = [('stps', 3),
                  ('head', 3),
                  ('prs', 6),
                  ('distLW', 3),
                  ('distRW', 3),
                  ('distLF', 3),
                  ('distRF', 3),
                  ('distLK', 3),
                  ('distRK', 3),
                  ('distRod', 3)]
    

    # Part 1: functions interfacing with the hardware

    def __init__(self):
        self.ser = serial.Serial(port=SERIAL_PORT,
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1)
        self.msg_raw = ''
        self.msg_decoded = {}
        sleep(2)
        '''
        # wait for the port to be ready,
        # TODO: remove the need for sleep after studying pySerial library in depth.
        '''
        while True:
            self.ser.write(HANDSHAKE_CODE)
            if self.ser.readline()[0:5] == 'ready':
                self.ser.flushInput()
                break

    def get_current_port(self):
        return self.ser.port

    def set_port(self, new_port):
        self.ser.port = new_port
        self.ser.open()

    def get_next_input(self):
        while True:
            try:
                result = int(self.ser.readline())
            except ValueError:
                pass
            else:
                break
        return result

    def start_sensing(self):
        self.ser.flushInput()
        self.ser.write(START_SENSOR_CODE)
        while self.ser.readline()[0:6] != 'ready2':
            pass
        self.ser.flushInput()

    def request_data(self):
        self.ser.flushInput()
        self.ser.write(REQUEST_CODE)
        self.msg_raw = self.ser.readline()
        self.process_raw()

    # reset step counter on Arduino
    def send_reset(self):
        self.ser.write(RESET_CODE)
        while self.ser.readline()[0:5] != 'reset':
            pass
        self.ser.flushInput()

    # Part 2: functions that do not interface with the hardware

    '''
    # This is a helper function. It is automatically called in request_data() function.
    # No need to be explicitly called.
    #
    # processing raw message into msg_decoded
    '''
    def process_raw(self):
        i = 0
        for (key, value) in self.msg_format:
            self.msg_decoded[key] = self.msg_raw[i:(value + i)]
            i += value

    def get_steps(self):
        return int(self.msg_decoded['stps'])

    def get_pressure(self):
        return float(int(self.msg_decoded['prs']))/100

    def get_heading(self):
        return int(self.msg_decoded['head'])

    def get_distanceLW(self):
        return int(self.msg_decoded['distLW'])
    
    def get_distanceRW(self):
        return int(self.msg_decoded['distRW'])
    
    def get_distanceLF(self):
        return int(self.msg_decoded['distLF'])
    
    def get_distanceRF(self):
        return int(self.msg_decoded['distRF'])
    
    def get_distanceLK(self):
        return int(self.msg_decoded['distLK'])
    def get_distanceRK(self):
        return int(self.msg_decoded['distRK'])
    
    def get_distanceRod(self):
        return int(self.msg_decoded['distRod'])
    


