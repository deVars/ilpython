# import idc
# import idautils
from idautils import Functions
from idc import GetFunctionName, GetFunctionAttr, GetManyBytes
from idc import FindBinary, PatchByte
from idc import FUNCATTR_START, FUNCATTR_END
from idc import SEARCH_DOWN, SEARCH_NOSHOW, BADADDR

class PatchRule:
    def __init__(self, name):
        self.name = name
        self.ea = None
        self.endEa = None

    def findFuncBinary(self, funcName, funcBinary):
        for funcAddr in Functions():
            if GetFunctionName(funcAddr) == funcName:
                self.ea = funcAddr
                break
        if self.ea is None:
            return self
        self.endEa = GetFunctionAttr(self.ea, FUNCATTR_END)
        if len(funcBinary) > 0:
            self.ea = FindBinary(self.ea, SEARCH_DOWN | SEARCH_NOSHOW,
                funcBinary, 16)
        # print('{:x} {:x} {:x}'.format(self.ea, binaryEA, self.ea + binaryEA))
        if self.ea > self.endEa:
            self.ea = None
        return self

    def patch(self, offset, patchHex):
        patch(self.ea, offset, self.name, patchHex)
        return self

    def patchFromEnd(self, offset, patchHex):
        patch(self.endEa, offset, self.name, patchHex)
        return self

    def getEA(self):
        if self.ea is not None:
            print '0x{:x}'.format(self.ea)
        return self


def patchList(patchesList):
    print('started patchList')
    for patch in patchesList:
        PatchRule(patch[0]) \
            .findFuncBinary(patch[1], patch[2]) \
            .getEA() \
            .patch(patch[3], patch[4])
    print('done!')


def findPatchString(config):
    patchStringByteArray = []
    for funcAddr in Functions():
        if GetFunctionName(funcAddr) == config['srcFnName']:
            print('found ea for ' + config['name'])
            break
    for byteIndex in xrange(0, config['patchLength']):
        func_byte_char = GetManyBytes(funcAddr + config['offset'] + byteIndex, 1)
        if func_byte_char is not None:
            patchStringByteArray.append('{:02x}'.format(ord(func_byte_char)))
    PATCH_STRING = ' '.join(patchStringByteArray)
    print('patch found for ' + config['name'] + ' >> ' + PATCH_STRING)
    return PATCH_STRING


def get_ea_from_binary(binary):
    return FindBinary(0, SEARCH_DOWN | SEARCH_NOSHOW, binary, 16)


def get_start_ea_from_binary(binary):
    ea = get_ea_from_binary(binary)
    if ea != BADADDR:
            return GetFunctionAttr(ea, FUNCATTR_START)
    return None


def zero_ex(hex_string, extend_bits):
    """
    takes in a hex_string to zero extend with extend_bits length
    :param hex_string:
    :param extend_bits:
    :return:
    """
    binary = '{:b}'.format(int(hex_string, 16) << extend_bits)[::-1]
    byte_chunks = [binary[x:x+8][::-1] for x in xrange(0, len(binary), 8)]
    return ' '.join(['{:02x}'.format(int(x, 2)) for x in byte_chunks])


def get_hex_bytes_from_ea(ea, length):
    """
    returns a list of hex bytes from an address
    :param ea:
    :param length:
    :return:
    """
    return ['{:02x}'.format(ord(x)) for x in GetManyBytes(ea, length)]


def patch(ea, offset, patch_name, patch_hex):
    if ea is None:
        print("Couldn't find address for {}! Skipping.".format(patch_name))
        return None
    for index, val in enumerate(patch_hex.strip().split(' ')):
        if val != '*':
            PatchByte(ea + offset + index, int(val, 16))
    print('patching {} on 0x{:x}'.format(patch_name, ea + offset))
    return None


def getFuncEA(funcName):
    for ea in Functions():
        iterFuncName = GetFunctionName(ea)
        if iterFuncName == funcName:
            return ea
    print('{} not found'.format(funcName))


def getFuncEALike(funcName):
    found = False
    for ea in Functions():
        iterFuncName = GetFunctionName(ea)
        if iterFuncName.find(funcName) != -1:
            print('0x{:x}'.format(ea), iterFuncName)
            found = True
    if not found:
        print('not found')


def rshift(val, n): return (val % 0x100000000) >> n


def getBLHexString(destEa, srcEa):
    offset = destEa - srcEa
    corrected_offset = (offset - 4) / 2  # align to THUMB 2 byte instructions
    unsigned_corrected_offset = rshift(corrected_offset, 0)
    is_signed = 1 if corrected_offset < 0 else 0
    binary_offset = '{:032b}'.format(unsigned_corrected_offset)[-21:]
    imm1 = binary_offset[:10]
    imm2 = binary_offset[10:]
    hiword_hibyte = '11110{}{}'.format(is_signed, imm1[:2])
    hiword_lobyte = '{}'.format(imm1[2:])
    loword_hibyte = '11111{}'.format(imm2[:3])
    loword_lobyte = '{}'.format(imm2[3:])
    return '{:02x} {:02x} {:02x} {:02x}'.format(int(hiword_lobyte, 2),
                                                int(hiword_hibyte, 2),
                                                int(loword_lobyte, 2),
                                                int(loword_hibyte, 2))


def getARMv8A64BLHexString(destEa, srcEa):
    # should be able to take imm26 now
    offset = destEa - srcEa
    corrected_offset = offset / 4  # v8A64
    unsigned_corrected_offset = rshift(corrected_offset, 0)
    is_signed = 1 if corrected_offset < 0 else 0
    binary_offset = '{:032b}'.format(unsigned_corrected_offset)
    imm_hi = binary_offset[:16]
    imm_lo = binary_offset[16:]
    hiword_hibyte = '100101{}'.format(imm_hi[6:8])
    hiword_lobyte = '{}'.format(imm_hi[8:])
    loword_hibyte = '{}'.format(imm_lo[:8])
    loword_lobyte = '{}'.format(imm_lo[8:])
    return '{:02x} {:02x} {:02x} {:02x}'.format(int(loword_lobyte, 2),
                                                int(loword_hibyte, 2),
                                                int(hiword_lobyte, 2),
                                                int(hiword_hibyte, 2))


def getARMBLHexString(destEa, srcEa):
    offset = destEa - srcEa
    corrected_offset = (offset - 8) / 4  # align to THUMB 2 byte instructions
    unsigned_corrected_offset = rshift(corrected_offset, 0)
    is_signed = 1 if corrected_offset < 0 else 0
    binary_offset = '{:032b}'.format(unsigned_corrected_offset)[-24:]
    imm_hi = binary_offset[:8]
    imm_lo = binary_offset[8:]
    hiword_hibyte = '11101011'
    hiword_lobyte = '{}'.format(imm_hi)
    loword_hibyte = '{}'.format(imm_lo[:8])
    loword_lobyte = '{}'.format(imm_lo[8:])
    return '{:02x} {:02x} {:02x} {:02x}'.format(int(loword_lobyte, 2),
                                                int(loword_hibyte, 2),
                                                int(hiword_lobyte, 2),
                                                int(hiword_hibyte, 2))


def getARMBHexString(destEa, srcEa):
    offset = destEa - srcEa
    corrected_offset = (offset - 8) / 4  # align to THUMB 2 byte instructions
    unsigned_corrected_offset = rshift(corrected_offset, 0)
    is_signed = 1 if corrected_offset < 0 else 0
    binary_offset = '{:032b}'.format(unsigned_corrected_offset)[-24:]
    imm_hi = binary_offset[:8]
    imm_lo = binary_offset[8:]
    hiword_hibyte = '11101010'
    hiword_lobyte = '{}'.format(imm_hi)
    loword_hibyte = '{}'.format(imm_lo[:8])
    loword_lobyte = '{}'.format(imm_lo[8:])
    return '{:02x} {:02x} {:02x} {:02x}'.format(int(loword_lobyte, 2),
                                                int(loword_hibyte, 2),
                                                int(hiword_lobyte, 2),
                                                int(hiword_hibyte, 2))
