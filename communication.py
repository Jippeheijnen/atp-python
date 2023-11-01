from datetime import datetime
from typing import Union
from functools import wraps
from util import Pins
from ctypes import cdll


def log_method_calls(f):
    '''
    Deze decorator is vrij vanzelfsprekend, een simpele log functie.
    :param f:
    :return:
    '''
    def wrapper(*args, **kw):
        t = datetime.now()
        printstr = f"{t.hour}:{t.minute}:{t.second} : " + \
                 f"Calling {f.__name__} with args: {args} and kwargs: {kw}"
        result = f(*args, **kw)
        print(printstr)
        print(f"{f.__name__} returned: {result}")
        return result

    return wrapper


"""
Het idee bij deze decorators is dat elke (soort) sensor een eigen c++ programma wordt,
deze moeten elk apart aangeroepen worden vanuit python, maar de signatuur (d.w.z. alleen een byte
waarde hoeft verstuurd te worden) van de send_command() verandert daar niet mee. Nu zijn
de UART en I2C functies nog vrij karig, maar deze gaan nog invulling krijgen zodra ik de 
koppeling tussen Python en C++ geïmplementeerd heb.
"""


def uart(f):
    '''
    Bij de UART decorator komt een implementatie die interact met de TMC2209 simulator.
    :param f: De send_command() functie waarover de decorator staat.
    :return:
    '''

    @wraps(f)
    def wrapper(self, *args, **kw):
        # self is the TMC2209
        self.serial.send(args, kw)
        f(self, *args, **kw)
        # ^ pass on self here

    return wrapper


def i2c_send_receive(f):
    '''
    Bij de I2C decorator komt een implementatie die interact met de VEML6075 simulator.
    :param f: De send_command() functie waarover de decorator staat.
    :return:
    '''

    @wraps(f)
    def wrapper(self, *args, **kw):
        # self is the UVSensor
        self.serial.send(args, kw)
        f(self, *args, **kw)
        # ^ pass on self here

    return wrapper


class Serial:
    def __init__(self,
                 tx: Union[Pins, None],
                 rx: Union[Pins, None]):
        self.tx = tx
        self.rx = rx
        pass

    def __repr__(self):
        return 'Serial'

    @log_method_calls
    def send(self, data: bytes, d_len: int):
        pass
