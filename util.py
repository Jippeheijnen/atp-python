from enum import Enum


class VEML_REG:
    UV_CONF: int = 0x0
    UVA_Data: int = 0x7
    UVB_Data: int = 0x9
    UVCOMP1_Data: int = 0xA
    UVCOMP2_Data: int = 0xB
    ID: int = 0xC
