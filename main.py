import ctypes
import time
from ctypes import c_ubyte
from typing import List
from atp_cplusplus import VEML6075, TMC2209

from communication import log_method_calls
# from communication import Serial
from util import VEML_REG

# Decorator for logging
def log_data(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time} seconds")
        return result

    return wrapper


if __name__ == '__main__':
    # Constants for calibration and tracking
    TARGET_UV_THRESHOLD = 1000  # Adjust this threshold based on your calibration
    HORIZONTAL_SPEED = 0.5  # Adjust the speed as needed
    VERTICAL_SPEED = 0.3  # Adjust the speed as needed

    # UV sensors
    topLeft: VEML6075 = VEML6075()
    topRight: VEML6075 = VEML6075()
    bottomLeft: VEML6075 = VEML6075()
    bottomRight: VEML6075 = VEML6075()

    # Stepper motors
    horizontal: TMC2209 = TMC2209()
    vertical: TMC2209 = TMC2209()

    # Initialize UV sensors
    uv_sensors = [topLeft,
                  topRight,
                  bottomLeft,
                  bottomRight]

    # Initialize motors
    motors = [horizontal,
              vertical]

    i: int = 0
    for i in range(4):
        uv_sensors[i] << [VEML_REG.UV_CONF, i, 0x0] # sending command

    @log_data
    @log_method_calls
    def func(uv_sensors):
        for sensor in uv_sensors:
            print("\n\n")
            print(f"sensor config is    : {bin(sensor >> VEML_REG.UV_CONF)}")
            print(f"sensor UVA data is  : {hex(sensor >> VEML_REG.UVA_Data)}")
            time.sleep(0.125)

    for i in range(20):
        func(uv_sensors)


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
    # def track_sun():
    #     while True:
    #         # hieronder wat voorbeeld logica
    #         uv_values = [sensor>> for sensor in uv_sensors]
    #         # avg_uv_value = sum(uv_values) / len(uv_values)
    #
    #         # Check if the average UV value is above the threshold
    #         # if avg_uv_value > TARGET_UV_THRESHOLD:
    #         if True:
    #             # Calculate adjustments for horizontal and vertical motors
    #             horizontal_adjustment = 0  # Calculate based on sensor data
    #             vertical_adjustment = 0  # Calculate based on sensor data
    #
    #             # Move the motors to adjust the solar panel position
    #             # motors[0].move(HORIZONTAL_SPEED * horizontal_adjustment)
    #             # vertical_motor.move(VERTICAL_SPEED * vertical_adjustment)
    #             # # Move the motors to adjust the solar panel position
    #             # horizontal_motor.move(HORIZONTAL_SPEED * horizontal_adjustment)
    #             # vertical_motor.move(VERTICAL_SPEED * vertical_adjustment)
    #         time.sleep(1)  # Adjust the sleep duration as needed
    #
    #
    # def calcMotorCorrection(uv_data:
    # Tuple[
    #     Tuple[float, float],
    #     Tuple[float, float]
    # ]) -> Tuple[float, float]:
    #     """
    #     A (Pure) function for calculating the stepper movements.
    #     :param uv_data: A 2x2 matrix which contains the
    #     :return: A tuple containing the movement values for the stepper motors.
    #     """
    #
    #     # assuming the UV sensors are positioned as follows:
    #
    #     # UV1 | UV2
    #     # ---------
    #     # UV3 | UV4
    #
    #     horizontal_movement = (uv_data[1][0] - uv_data[0][1])  # UV3 - UV2
    #     vertical_movement = (uv_data[0][0] - uv_data[1][1])  # UV1 - UV4
    #
    #     return [horizontal_movement, vertical_movement]


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
