from patchUtil import *
# used to get battleServantData:checkPlayer callvirt
CREATE_COMMAND_BATTLE_SIGNATURE = '11 0E 11 0F 94 13 0D 11 0D 11 04'
CHECK_PLAYER_OFFSET = int('3f', 16)
CHECK_PLAYER_LENGTH = 5
check_player_callvirt_bytes = get_hex_bytes_from_ea(
    get_ea_from_binary(CREATE_COMMAND_BATTLE_SIGNATURE) + CHECK_PLAYER_OFFSET,
    CHECK_PLAYER_LENGTH)

# used to get battleServantData::getAttri callvirt
BL_DEBUG_SORO_SIGNATURE = '13 05 11 05 13 07 16 13 08 38 74 00 00 00'
GET_ATTRI_OFFSET = int('4f', 16)
GET_ATTRI_LENGTH = 5
get_attri_callvirt_bytes = get_hex_bytes_from_ea(
    get_ea_from_binary(BL_DEBUG_SORO_SIGNATURE) + GET_ATTRI_OFFSET,
    GET_ATTRI_LENGTH
)

GET_CRITICAL_POINT_SIGNATURE = '8E 69 3C 0C 00 00 00 16 02'

GET_DAMAGE_LIST_SIGNATURE = '11 ? 11 ? 5A 13 ? 11 ? 03'

# not really signature since this is shared with class relation master
ATTRI_RELATION_MASTER_SIGNATURE = \
    '0A 06 3A 06 00 00 00 22 00 00 80 3F 2A 06 02 03'

print check_player_callvirt_bytes
print get_attri_callvirt_bytes
print '{:x}'.format(get_start_ea_from_binary(GET_CRITICAL_POINT_SIGNATURE))