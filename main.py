import asyncio
import struct
from typing import List, Any, Coroutine, Tuple
from crc import Calculator, Crc8

from atp_cplusplus import VEML6075, TMC2209

from util import LOADCELL, log_method_calls, log_data, VEML_REG


def split_32bits_lsb_msb(value: int) -> List[int]:
    return list(struct.unpack('4B', struct.pack('<I', value)))


def calc_crc(datagram):
    calculator = Calculator(Crc8.CCITT)
    return calculator.checksum(datagram)


def calcMotorCorrection(uv_data:
List[int]) -> Tuple[float, float]:
    """
    A (Pure) function for calculating the stepper movements.
    :param uv_data: A 2x2 matrix which contains the
    :return: A tuple containing the movement values for the stepper motors.
    """

    # assuming the UV sensors are positioned as follows:

    # UV1 | UV2
    # ---------
    # UV3 | UV4

    return (((uv_data[0] / 100 + uv_data[3] / 100) / 2 -
             (uv_data[1] / 100 + uv_data[2] / 100) / 2),  # left - right
            ((uv_data[0] / 100 + uv_data[1] / 100) / 2 -
             (uv_data[2] / 100 + uv_data[3] / 100) / 2))  # up - down


async def main():
    subtasks: List[Coroutine] = []

    # Constants for calibration and tracking
    W_THRS = 3  # weight threshold at which the panel starts clearing debris.
    X_THRS = 0.5  # horizontal correction threshold
    Y_THRS = 0.3  # vertical correction threshold

    # UV sensors
    topLeft: VEML6075 = VEML6075()
    topRight: VEML6075 = VEML6075()
    bottomLeft: VEML6075 = VEML6075()
    bottomRight: VEML6075 = VEML6075()

    # Stepper motors
    horizontal: TMC2209 = TMC2209(0)
    vertical: TMC2209 = TMC2209(1)

    # loadcell
    loadcell: LOADCELL = LOADCELL()

    # Initialize UV sensors
    uv_sensors = [topLeft,
                  topRight,
                  bottomLeft,
                  bottomRight]

    # Initialize motors
    motors = [horizontal,
              vertical]

    # configuring motors
    # datagram lsb -> msb =
    # sync + reserved, slave_addr, reg_addr, data[0], data[1], data[2], data[3], crc

    # writing GCONF
    data = 414170769
    datagram_h = [5, 0, 127, *[val for val in split_32bits_lsb_msb(data)],
                  calc_crc([5, 0, 0, *split_32bits_lsb_msb(data)])]
    h_response = [motor << datagram_h for motor in motors]  # simulating the bus, so all slaves receive a datagram
    datagram_v = [hex(5), hex(1), hex(127), hex(*split_32bits_lsb_msb(data)),
                  hex(calc_crc([5, 0, 0, *split_32bits_lsb_msb(data)]))]
    v_response = [motor << datagram_v for motor in motors]

    # reading GCONF to check if chip received.
    # h_response = [motor << [5, 0, 0, calc_crc([5, 0, 0b00000000])] for motor in motors]
    # v_response = [motor << [5, 1, 0, calc_crc([5, 0, 0b00000000])] for motor in motors]

    # setting up the UV sensors
    i: int = 0
    for i in range(4):
        uv_sensors[i] << [VEML_REG.UV_CONF, i, 0x0]  # sending command

    # The main eventloop
    async def main_loop():
        for sensor in uv_sensors:
            print("\n\n")
            print(f"sensor config is                : {bin(sensor >> VEML_REG.UV_CONF)}")
            print(f"sensor UVA data is              : {hex(sensor >> VEML_REG.UVA_Data)}")
            print(f"current weight on the panel is  : {loadcell.get_weight()}grams")
        await asyncio.sleep(0.05)

        uv_values: List[int] = [sensor >> VEML_REG.UVA_Data for sensor in uv_sensors]

        correction: Tuple[float, float] = calcMotorCorrection(uv_values)

        # print(f"[{uv_values[0]},{uv_values[1]}]\n"
        #      f"[{uv_values[2]},{uv_values[3]}]\n"
        #      f"weight: {loadcell.get_weight()}\n"
        #      f"motor correction: {correction}\n\n")

        # checking motors to see if they are not overheating
        # datagram lsb -> msb =
        # sync + reserved, slave_addr, reg_addr, data, crc

        # h_response = [motor << [5, 0, 0b10000000, ] for motor in motors]
        # v_response = [motor << [5, 1, 0b10000000, ] for motor in motors]

        # Check if the horizontal motor correction value is above the threshold of 0.1
        if correction[0] - .1 > 0 > correction[0] + .1:
            horizontal << []

        # Check if the vertical motor correction value is above the threshold of 0.1
        if correction[1] - .1 > 0 > correction[1] + .1:
            vertical << []

        await asyncio.sleep(0.5)  # Adjust the sleep duration as needed

    # running everything simultaneously (for the simulation of the loadcell)
    f2 = asyncio.create_task(loadcell.start_timer())

    while True:
        f1 = asyncio.create_task(loadcell.run())
        f3 = asyncio.create_task(main_loop())
        await asyncio.wait([f1, f3])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
