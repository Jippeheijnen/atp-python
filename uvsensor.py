from communication import Serial, i2c_send_receive, log_method_calls


class VEML6075:
    def __init__(self, id: int, serial: Serial):
        '''

        :param serial: The serial object
        '''
        self.serial = serial
        pass

    def __repr__(self):
        return 'VEML6075'

    def setup(self):
        '''

        :return:
        '''

    @log_method_calls
    @i2c_send_receive
    def send_command(self, data: bytes, d_len: int):
        '''

        :param data: Data to be sent in bytes() format.
        :param d_len: Data length in int amt of bits.
        :return: None for now
        '''
        pass

    def read_uv(self):
        self.send_command(bytes([0b00000001]), 8)
        self.send_command(bytes([0b00000010]), 8)
        self.send_command(bytes([0b00000011]), 8)
        self.send_command(bytes([0b00000100]), 8)

        # return uv values in the future
        return
