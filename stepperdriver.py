from communication import Serial, uart, log_method_calls
from util import Pins
from functools import wraps


class TMC2209:
    '''
    Dit is de controller klasse foor de TMC2209 chip.
    '''

    def __init__(self, id: int, serial: Serial):
        '''

        :param serial:
        '''
        self.serial = serial

    def __repr__(self):
        return 'TMC2209'

    def setup(self):
        '''
        setup the chip.
        '''

    def move(self, steps: float):
        self.send_command(bytes([0b10000000]), 8)
        self.send_command(bytes([0b01111111]), 8)
        self.send_command(bytes([0b01111110]), 8)
        self.send_command(bytes([0b01111101]), 8)
        return

    @log_method_calls
    @uart
    def send_command(self, data: bytes, d_len: int):

        return
