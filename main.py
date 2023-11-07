import asyncio
import time
from asyncio import Task
from typing import List, Any, Coroutine, Tuple
from concurrent.futures import ProcessPoolExecutor

from atp_cplusplus import VEML6075, TMC2209

from util import LOADCELL, log_method_calls, log_data, VEML_REG


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

    # setting up the UV sensors
    i: int = 0
    for i in range(4):
        uv_sensors[i] << [VEML_REG.UV_CONF, i, 0x0]  # sending command

    # The main eventloop
    async def main_loop():
        # for sensor in uv_sensors:
        #     print("\n\n")
        #     print(f"sensor config is                : {bin(sensor >> VEML_REG.UV_CONF)}")
        #     print(f"sensor UVA data is              : {hex(sensor >> VEML_REG.UVA_Data)}")
        #     print(f"current weight on the panel is  : {loadcell.get_weight()}grams")
        # await asyncio.sleep(0.05)

        uv_values: List[int] = [sensor >> VEML_REG.UVA_Data for sensor in uv_sensors]
        avg_uv_value = sum(uv_values) / len(uv_values)
        correction: Tuple[float, float] = calcMotorCorrection(uv_values)
        print(f"[{uv_values[0]},{uv_values[1]}]\n"
              f"[{uv_values[2]},{uv_values[3]}]\n"
              f"weight: {loadcell.get_weight()}\n"
              f"motor correction: {correction}\n\n")

        # checking motors to see if they are not overheating
        h_response = horizontal << []
        v_response = vertical << []

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

    # def move_stepper_to_target(self, target_position):
    #     if self.current_position == target_position:
    #         # If the current position matches the target, no adjustment needed
    #         return
    #     elif self.current_position < target_position:
    #         # If lesser than target, increment position
    #         self.current_position += 1  # arbitrary value for now, change in the future
    #     else:
    #         # If greater than target, decrement position
    #         self.current_position -= 1  # arbitrary value for now, change in the future
    #
    #     print(f"Current position: {self.current_position}")
    #
    #     # Recursively call adjust_position until the target is reached
    #     self.move_stepper_to_target(target_position)
    #
    #
    # # Function to track the sun
    # @log_data

    #

    # if __name__ == "__main__":
    #     # Define example UV data as 2x2 matrices
    #     # Normally this data would come from the UV sensors
    #     uv_data_point_1 = [[0.8, 0.6], [0.5, 0.7]]
    #     uv_data_point_2 = [[0.7, 0.9], [0.4, 0.6]]
    #     uv_data_point_3 = [[0.6, 0.8], [0.7, 0.5]]
    #     uv_data_point_4 = [[0.9, 0.7], [0.6, 0.8]]
    #
    #     # simulate a list that is managed first-in first-out
    #     uv_data_fifo_list = [uv_data_point_1,
    #                          uv_data_point_2,
    #                          uv_data_point_3,
    #                          uv_data_point_4]
    #
    #     # Example usage of the map func on the UV data:
    #
    #     movement_orders = map(calcMotorCorrection, uv_data_fifo_list)
    #
    #     print(movement_orders)
    #
    #     # Example usage of the calcMotorCorrection func:
    #
    #     sensor_data_matrix = [[0.2, 0.3],
    #                           [0.5, 0.4]]
    #
    #     movement = calcMotorCorrection(sensor_data_matrix)
    #     print("Horizontal Movement value:", movement[0])
    #     print("Vertical Movement value:", movement[1])
    #
    #     track_sun()
