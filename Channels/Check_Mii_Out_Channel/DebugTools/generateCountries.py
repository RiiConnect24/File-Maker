from cmoc import Prepare
from struct import pack

# automatically generates all country codes for /first. sloppy code because it only needs to be ran once

# codes = [1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 128, 136, 144, 145, 152, 153, 154, 155, 156, 160, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177]
# codes = [201, 202, 203, 204, 205, 206]
codes = [100]
p = Prepare()


def u32(data):
    if not 0 <= data <= 4294967295:
        log("u32 out of range: %s" % data, "INFO")
        data = 0
    return pack(">I", data)


for i in codes:
    with open(("addition/" + str(i) + ".ces"), "wb") as file:
        # data = bytes.fromhex('46440000') + u32(i) + bytes.fromhex('00000000000000000000000000000000FFFFFFFFFFFFFFFF4644000C0000000196000003')
        data = (
            bytes.fromhex("4144000000000000")
            + u32(i)
            + bytes.fromhex("000000000000009600000096FFFFFFFFFFFFFFFF")
        )
        file.write(p.prepare(data))
