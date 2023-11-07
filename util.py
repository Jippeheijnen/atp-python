from datetime import datetime
import time
import random
import asyncio


class LOADCELL:
    """
    This is the simulated class for the loadcell sensor, it returns random weight values.
    When a specific time is reached, ths class will simulate a weather event, such as snow.

    Attributes:
        weight          Actual current weight on the sensor (simulating noise)
        weight_offset   Gained weight due to weather
        timer_trigger   The weather event has commenced and weight is being gained.
        timer_time      The time in seconds after which a weather event occurs.
    """
    weight: float = 0
    weight_offset: float = 0
    time_trigger: bool = False
    timer_time: int = 10

    def __init__(self):
        self.weight = random.uniform(0.01, 0.1)
        # asyncio.create_task(asyncio.to_thread(self.run))
        return

    def get_weight(self) -> float:
        return self.weight

    async def start_timer(self):
        await asyncio.sleep(self.timer_time)
        self.time_trigger = True
        self.timer_time = 2

    async def run(self):
        if not self.time_trigger:
            self.weight = random.uniform(0.01, 0.1) + self.weight_offset
        else:
            self.weight_offset += random.uniform(0.1, 0.5)
            self.time_trigger = False
            asyncio.create_task(self.start_timer())


class VEML_REG:
    UV_CONF: int = 0x0
    UVA_Data: int = 0x7
    UVB_Data: int = 0x9
    UVCOMP1_Data: int = 0xA
    UVCOMP2_Data: int = 0xB
    ID: int = 0xC


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


# Decorator for logging
def log_data(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time} seconds")
        return result

    return wrapper
