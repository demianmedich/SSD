# coding=utf-8


DEFAULT_LOWER_BOUND = 0
DEFAULT_UPPER_BOUND = 99
DEFAULT_ERASE_MAX_SIZE = 10


def is_valid_address(
    address: int,
) -> bool:
    return DEFAULT_LOWER_BOUND <= address <= DEFAULT_UPPER_BOUND


def is_valid_address_and_size(
    address: int,
    size: int,
) -> bool:
    return (
        (0 < size <= DEFAULT_ERASE_MAX_SIZE)
        and (address + size <= DEFAULT_UPPER_BOUND + 1)
        and (DEFAULT_LOWER_BOUND <= address)
    )


def is_8digit_hex_string(value: str) -> bool:
    return (
        len(value) == 10
        and value.startswith("0x")
        and all(c in "0123456789ABCDEF" for c in value[2:])
    )
