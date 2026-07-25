"""
PlatinumWarpMapInfo.py

Pokemon Platinum warp randomizer rules

Copyright (c) 2023 AtSign, XLuma, Turtleisaac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
class WT:
    def __init__(self, warp_id, flag):
        if isinstance(warp_id, int) and isinstance(flag, int):
            self.warp_id = warp_id
            self.flag = flag
        else:
            raise ValueError("Invalid Warp Tuple")


# Event/HM Dependencies
# Any Warp/Connection that has an Event/HM Dependency will have a corresponding blocker flag
# Based off bits set in flag, we will know what dependencies are required to traverse
TRAINERSCHOOL_FLAG = 0
ROCKSMASH_FLAG = 1
WINDWORKS_FLAG = 2
FLASH_FLAG = 3
CUT_FLAG = 4
BIKE_FLAG = 5
CONTESTHALL_FLAG = 6
HEARTHOMEGYM_FLAG = 7
DEFOG_FLAG = 8
FLY_FLAG = 9
PSYDUCK_FLAG = 10
SURF_FLAG = 11
STRENGTH_FLAG = 12
LAKES_FLAG = 13
VALOR_FLAG = 14
VERITY_FLAG = 15
ROCKCLIMB_FLAG = 16
GALACTICKEY_FLAG = 17
LIGHTHOUSE_FLAG = 18
WATERFALL_FLAG = 19
MEADOW_FLAG = 20
SPEECH_FLAG = 21
GUARDIANSFREE_FLAG = 22
VEILSTONEGYM_FLAG = 23
ROARK_FLAG = 24

END_FLAG = ROARK_FLAG

def fl(flag):
    return 1 << flag

# reminder - move deleter is in Map_Canalave_City_Room03_00

trainerschool_event = ['Map_Jubilife_Trainer_School_00']
rocksmash_event = ['Map_Oreburgh_Gate_00:0', 'Map_Oreburgh_Gym_00']
windworks_event = ['Map_ValleyWindworks_Interior_00']
cut_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Eterna_City_01']
flash_event = ['Map_Oreburgh_Gate_Floor01_00']
bike_event = ['Map_Eterna_Galactic_Building_Floor03_00:1', 'Map_Eterna_Cycle_Shop_00']
constesthall_event = ['Map_Hearthome_Contest_00']
hearthomegym_event = ['Map_Hearthome_Gym_00']
defog_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Solaceon_Ruins_Room10_00']
fly_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Veilstone_Warehouse_00',
             'Map_Veilstone_Gym_00']
psyduck_event = ['Map_Pastoria_Gym_00', 'Map_Pastoria_City_00', 'Map_Route_213_00', 'Map_Valor_Lakefront_01']
surf_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Veilstone_Gym_00',
              'Map_Pastoria_Gym_00', 'Map_Valor_Lakefront_01', 'Map_Pastoria_City_00',
              'Map_Route_213_00', 'Map_Celestic_Town_00', 'Map_Celestic_Shrine_00']
strength_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Veilstone_Gym_00',
                  'Map_Pastoria_Gym_00', 'Map_Canalave_Gym_00', 'Map_Canalave_City_00']
lakes_event = ['Map_Iron_Island_00', 'Map_Canalave_Gym_00', 'Map_Canalave_Library_02']
valor_event = ['Map_Valor_Cavern_00']
verity_event = ['Map_Lake_Verity_00']
rockclimb_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Veilstone_Gym_00',
                   'Map_Pastoria_Gym_00', 'Map_Canalave_Gym_00', 'Map_Route_217_00', 'Map_Snowpoint_Gym_00']
galactickey_event = ['Map_Galactic_HQ_Floor04_00:1']
lighthouse_event = ['Map_Lighthouse_00']
waterfall_event = ['Map_Oreburgh_Gym_00', 'Map_Eterna_Gym_00', 'Map_Hearthome_Gym_00', 'Map_Veilstone_Gym_00',
                   'Map_Pastoria_Gym_00', 'Map_Canalave_Gym_00', 'Map_Snowpoint_Gym_00', 'Map_Sunyshore_Gym_00']
meadow_event = ['Map_Floaroma_Meadow_00']
speech_event = ['Map_Galactic_HQ_Floor06_00:0']
guardiansfree_event = ['Map_Galactic_HQ_SS1_Room01_00']
veilstonegym_event = ['Map_Veilstone_Gym_00']
roark_event = ['Map_Oreburgh_Mine_Room02_00']

FORCED_FLAG_ORDER = [ROCKSMASH_FLAG, CUT_FLAG, FLASH_FLAG, HEARTHOMEGYM_FLAG, DEFOG_FLAG, VEILSTONEGYM_FLAG, FLY_FLAG,
                     PSYDUCK_FLAG, SURF_FLAG, LAKES_FLAG, STRENGTH_FLAG, ROCKCLIMB_FLAG, WATERFALL_FLAG]
FLAG_EVENT_LIST = [trainerschool_event, rocksmash_event, windworks_event, flash_event, cut_event, bike_event,
                   constesthall_event, hearthomegym_event, defog_event, fly_event, psyduck_event, surf_event,
                   strength_event, lakes_event, valor_event, verity_event, rockclimb_event, galactickey_event,
                   lighthouse_event, waterfall_event, meadow_event, speech_event, guardiansfree_event,
                   veilstonegym_event, roark_event]  # incomplete

no_event_allowed = []  # incomplete
map_chain_breaks = []  # incomplete

# Event Based Warps and Warp Connections
# If map not specified, assume that all warps are accessible
map_warp_accessibility = {
    'Map_Jubilife_City_00': {
        0: [WT(1, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(4, 0), WT(5, 0)],
        2: [],
        3: [],
        4: [WT(0, 0), WT(1, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(4, 0)]
    },
    'Map_Jubilife_City_01': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Jubilife_City_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_City_03': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Verity_Lakefront_03': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(3, 0)],
        2: [WT(0, 0), WT(3, 0)],
        3: [WT(1, 0), WT(2, 0)]
    },
    'Map_Route_221_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Twinleaf_Town_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Sandgem_Town_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Oreburgh_City_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, fl(ROARK_FLAG)), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, fl(ROARK_FLAG)), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, fl(ROARK_FLAG)), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, fl(ROARK_FLAG)), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, fl(ROARK_FLAG)), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Oreburgh_City_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Oreburgh_City_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Route_206_00': {
        0: [WT(1, 0), WT(6, 0), WT(7, 0), WT(8, 0), WT(9, 0), WT(10, 0), WT(11, 0)],  # path
        1: [WT(0, 0), WT(6, 0), WT(7, 0), WT(8, 0), WT(9, 0), WT(10, 0), WT(11, 0)],  # path
        2: [WT(3, 0), WT(4, fl(CUT_FLAG)), WT(5, fl(CUT_FLAG)), WT(12, fl(CUT_FLAG)), WT(13, fl(CUT_FLAG))],  # underside

        3: [WT(2, 0), WT(4, fl(CUT_FLAG)), WT(5, fl(CUT_FLAG)), WT(12, fl(CUT_FLAG)), WT(13, fl(CUT_FLAG))],  # underside

        4: [WT(5, 0), WT(12, 0), WT(13, 0), WT(2, fl(CUT_FLAG)), WT(3, fl(CUT_FLAG))],  # exterior
        5: [WT(4, 0), WT(12, 0), WT(13, 0), WT(2, fl(CUT_FLAG)), WT(3, fl(CUT_FLAG))],  # exterior
        6: [WT(0, 0), WT(1, 0), WT(7, 0), WT(8, 0), WT(9, 0), WT(10, 0), WT(11, 0)],  # path
        7: [WT(0, 0), WT(1, 0), WT(6, 0), WT(8, 0), WT(9, 0), WT(10, 0), WT(11, 0)],  # path
        8: [WT(0, 0), WT(1, 0), WT(6, 0), WT(7, 0), WT(9, 0), WT(10, 0), WT(11, 0)],  # path
        9: [WT(0, 0), WT(1, 0), WT(6, 0), WT(7, 0), WT(8, 0), WT(10, 0), WT(11, 0)],  # path
        10: [WT(0, 0), WT(1, 0), WT(6, 0), WT(7, 0), WT(8, 0), WT(9, 0), WT(11, 0)],  # path
        11: [WT(0, 0), WT(1, 0), WT(6, 0), WT(7, 0), WT(8, 0), WT(9, 0), WT(10, 0)],  # path
        12: [WT(4, 0), WT(5, 0), WT(13, 0), WT(2, fl(CUT_FLAG)), WT(3, fl(CUT_FLAG))],  # exterior
        13: [WT(4, 0), WT(5, 0), WT(12, 0), WT(2, fl(CUT_FLAG)), WT(3, fl(CUT_FLAG))]  # exterior
    },
    'Map_Route_207_01': {
        0: [],
        1: []
    },
    'Map_Eterna_City_00': {
        0: [WT(1, 0), WT(3, 0), WT(4, 0), WT(2, fl(CUT_FLAG))],
        1: [WT(0, 0), WT(3, 0), WT(4, 0), WT(2, fl(CUT_FLAG))],
        2: [WT(0, fl(CUT_FLAG)), WT(1, fl(CUT_FLAG)), WT(3, fl(CUT_FLAG)), WT(4, fl(CUT_FLAG))],
        3: [WT(0, 0), WT(1, 0), WT(4, 0), WT(2, fl(CUT_FLAG))],
        4: [WT(0, 0), WT(1, 0), WT(3, 0), WT(2, fl(CUT_FLAG))]
    },
    'Map_Eterna_City_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Fuego_Ironworks_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_205_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_205_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Floaroma_Town_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Floaroma_Town_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0), WT(6, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0), WT(6, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0), WT(6, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0), WT(6, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0), WT(6, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(6, 0)],
        6: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)]
    },
    'Map_Hearthome_City_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Hearthome_City_01': {
        0: [WT(1, 0), WT(2, fl(CONTESTHALL_FLAG)), WT(3, 0)],
        1: [WT(0, 0), WT(2, fl(CONTESTHALL_FLAG)), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, fl(CONTESTHALL_FLAG))]
    },
    'Map_Hearthome_City_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)],
        3: [WT(4, 0), WT(5, 0), WT(6, 0)],
        4: [WT(3, 0), WT(5, 0), WT(6, 0)],
        5: [WT(3, 0), WT(4, 0), WT(6, 0)],
        6: [WT(3, 0), WT(4, 0), WT(5, 0)]
    },
    'Map_Hearthome_City_03': {
        0: [WT(1, 0), WT(2, fl(HEARTHOMEGYM_FLAG)), WT(3, fl(HEARTHOMEGYM_FLAG))],
        1: [WT(0, 0), WT(2, fl(HEARTHOMEGYM_FLAG)), WT(3, fl(HEARTHOMEGYM_FLAG))],
        2: [WT(0, 0), WT(1, 0), WT(3, fl(HEARTHOMEGYM_FLAG))],
        3: [WT(0, 0), WT(1, 0), WT(2, fl(HEARTHOMEGYM_FLAG))]
    },
    'Map_Route_208_01': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_209_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_215_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Solaceon_Town_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Solaceon_Town_01': {
        0: [],
        1: [],
        2: [],
        3: []
    },
    'Map_Celestic_Town_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Veilstone_City_00': {
        0: [WT(1, 0), WT(3, fl(VEILSTONEGYM_FLAG))],
        1: [WT(0, 0), WT(3, fl(VEILSTONEGYM_FLAG))],
        2: [WT(0, 0), WT(1, 0), WT(3, fl(VEILSTONEGYM_FLAG))],
        3: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_City_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Veilstone_City_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_City_03': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Pastoria_City_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, fl(VEILSTONEGYM_FLAG)), WT(2, 0)],
        2: [WT(0, fl(VEILSTONEGYM_FLAG)), WT(1, 0)]
    },
    'Map_Pastoria_City_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Pastoria_City_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_212_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Sunyshore_City_00': {
        0: [WT(3, fl(LIGHTHOUSE_FLAG)), WT(4, 0)],
        1: [],
        2: [],
        3: [WT(0, 0), WT(4, 0)],
        4: [WT(0, 0), WT(3, fl(LIGHTHOUSE_FLAG))]
    },
    'Map_Sunyshore_City_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Sunyshore_City_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Sunyshore_City_03': {
        0: [WT(1, fl(ROCKCLIMB_FLAG))],
        1: [WT(0, fl(ROCKCLIMB_FLAG))]
    },
    'Map_Pokemon_League_01': {
        0: [WT(1, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(3, 0), WT(4, 0)],
        2: [WT(5, 0), WT(6, 0)],
        3: [WT(0, 0), WT(1, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(3, 0)],
        5: [WT(2, 0), WT(6, 0)],
        6: [WT(2, 0), WT(5, 0)]
    },
    'Map_Snowpoint_City_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Snowpoint_City_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Acuity_Lakefront_02': {
        0: [WT(1, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(2, 0)]
    },
    'Map_Canalave_City_00': {
        0: [WT(1, 0), WT(2, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Canalave_City_01': {
        0: [WT(1, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(3, 0), WT(4, 0)],
        2: [WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(3, 0)],
        5: [WT(2, 0)]
    },
    'Map_Fullmoon_Island_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Iron_Island_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Newmoon_Island_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_218_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_218_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_225_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Survival_Area_00': {
        0: [WT(1, 0), WT(3, 0), WT(4, 0)],
        1: [WT(3, 0), WT(4, 0)],
        2: [],
        3: [WT(1, 0), WT(4, 0)],
        4: [WT(1, 0), WT(3, 0)]
    },
    'Map_Route_226_02': {
        0: [WT(1, fl(SURF_FLAG)), WT(2, fl(SURF_FLAG))],
        1: [WT(2, 0), WT(0, fl(SURF_FLAG))],
        2: [WT(1, 0), WT(0, fl(SURF_FLAG))]
    },
    'Map_Valor_Lakefront_01': {
        0: [WT(1, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(2, 0)]
    },
    'Map_Valor_Lakefront_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Spring_Path_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_213_00': {
        # top left
        0: [WT(1, 0), WT(3, 0), WT(7, 0)],  # outside
        1: [WT(0, 0), WT(3, 0), WT(7, 0)],  # outside

        # top middle
        2: [WT(4, 0), WT(5, 0), WT(6, fl(ROCKCLIMB_FLAG))],  # inside

        # top right
        3: [WT(0, 0), WT(1, 0), WT(7, 0)],  # outside
        4: [WT(2, 0), WT(5, 0), WT(6, fl(ROCKCLIMB_FLAG))],  # inside
        5: [WT(2, 0), WT(4, 0), WT(6, fl(ROCKCLIMB_FLAG))],  # inside
        6: [WT(2, fl(ROCKCLIMB_FLAG)), WT(4, fl(ROCKCLIMB_FLAG)), WT(5, fl(ROCKCLIMB_FLAG))],  # inside

        # bottom left
        7: [WT(0, 0), WT(1, 0), WT(3, 0)]  # outside
    },
    'Map_Route_214_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0)],
        3: [WT(0, 0), WT(1, 0)],
        4: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_222_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Fight_Area_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Fight_Area_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Route_228_00': {
        0: [WT(1, 0), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG))],
        1: [WT(0, 0), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG))],
        2: [WT(0, fl(BIKE_FLAG)), WT(1, fl(BIKE_FLAG))],
        3: [WT(0, fl(BIKE_FLAG)), WT(1, fl(BIKE_FLAG))]
    },
    'Map_Resort_Area_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Oreburgh_Gate_00': {
        0: [WT(1, 0), WT(2, fl(ROCKSMASH_FLAG))],
        1: [WT(0, 0), WT(2, fl(ROCKSMASH_FLAG))],
        2: [WT(0, fl(ROCKSMASH_FLAG)), WT(1, fl(ROCKSMASH_FLAG))]
    },
    'Map_Oreburgh_Mine_Room01_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Eterna_Forest_Interior_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Forest_Interior_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Mount_Coronet_Floor00_00': {
        0: [WT(1, 0), WT(2, fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG))],
        1: [WT(0, 0), WT(2, fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG))],
        2: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, fl(ROCKCLIMB_FLAG))]
    },
    'Map_Mount_Coronet_Floor01_00': {
        0: [],
        1: [WT(2, 0)],
        2: [WT(1, 0)],
        3: []
    },
    'Map_Mount_Coronet_Floor01_01': {
        0: [WT(1, fl(STRENGTH_FLAG))],
        1: [WT(0, fl(STRENGTH_FLAG))]
    },
    'Map_Mount_Coronet_Floor02_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Mount_Coronet_Floor03_00': {
        0: [WT(4, fl(ROCKCLIMB_FLAG))],
        1: [WT(2, fl(SURF_FLAG) | fl(WATERFALL_FLAG))],

        2: [WT(1, fl(SURF_FLAG) | fl(WATERFALL_FLAG))],
        3: [],
        4: [WT(0, fl(ROCKCLIMB_FLAG))]
    },
    'Map_Mount_Coronet_Floor04_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Mount_Coronet_Floor05_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Mount_Coronet_Floor06_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0)],
        2: [WT(0, 0)],
        3: [WT(0, 0)],
        4: [WT(0, 0)]
    },
    'Map_Mount_Coronet_Floor08_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0)],
        3: [WT(0, 0), WT(1, 0)]
    },
    'Map_Mount_Coronet_Floor09_01': {
        0: [WT(1, fl(STRENGTH_FLAG)), WT(2, fl(STRENGTH_FLAG))],
        1: [WT(2, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))],
        2: [WT(1, fl(STRENGTH_FLAG))]
    },
    'Map_Solaceon_Ruins_Room01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Solaceon_Ruins_Room02_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Solaceon_Ruins_Room03_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Solaceon_Ruins_Room05_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Solaceon_Ruins_Room05_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Solaceon_Ruins_Room07_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Solaceon_Ruins_Room08_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Victory_Road_Floor01_00': {
        # (0,0)
        0: [WT(1, fl(ROCKCLIMB_FLAG)), WT(2, fl(ROCKCLIMB_FLAG)), WT(3, fl(ROCKCLIMB_FLAG)), WT(4, fl(ROCKCLIMB_FLAG)), WT(5, fl(ROCKCLIMB_FLAG)), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, fl(ROCKCLIMB_FLAG)), WT(9, fl(ROCKCLIMB_FLAG)), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w5 - top left stairs

        # (1,0)
        1: [WT(0, fl(ROCKCLIMB_FLAG)), WT(2, fl(ROCKCLIMB_FLAG)), WT(3, fl(ROCKCLIMB_FLAG)), WT(4, fl(ROCKCLIMB_FLAG)), WT(5, 0), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, 0), WT(9, 0), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w4 - right stair exit
        2: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, fl(ROCKCLIMB_FLAG)), WT(3, 0), WT(4, 0), WT(5, fl(ROCKCLIMB_FLAG)), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, fl(ROCKCLIMB_FLAG)), WT(9, fl(ROCKCLIMB_FLAG)), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w8 - top entrance
        3: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, fl(ROCKCLIMB_FLAG)), WT(2, 0), WT(4, 0), WT(5, fl(ROCKCLIMB_FLAG)), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, fl(ROCKCLIMB_FLAG)), WT(9, fl(ROCKCLIMB_FLAG)), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w11 - top entrance
        4: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, fl(ROCKCLIMB_FLAG)), WT(2, 0), WT(3, 0), WT(5, fl(ROCKCLIMB_FLAG)), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, fl(ROCKCLIMB_FLAG)), WT(9, fl(ROCKCLIMB_FLAG)), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w12 - top entrance

        # (0,1)
        5: [WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w0 - up stair entrance
        6: [WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG)), WT(5, fl(ROCKCLIMB_FLAG)), WT(7, fl(ROCKCLIMB_FLAG))],  # w1 - up stair exit

        # (1,1)
        7: [WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG)), WT(5, 0), WT(6, fl(ROCKCLIMB_FLAG))],  # w2 - right stair entrance
        8: [],  # w3 - item spot
        9: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, 0), WT(2, fl(ROCKCLIMB_FLAG)), WT(3, fl(ROCKCLIMB_FLAG)), WT(4, fl(ROCKCLIMB_FLAG)), WT(5, 0), WT(6, fl(ROCKCLIMB_FLAG)), WT(7, 0), WT(10, fl(ROCKCLIMB_FLAG)), WT(11, fl(ROCKCLIMB_FLAG)), WT(12, fl(ROCKCLIMB_FLAG))],  # w6 - postgame door

        # (0,2)
        10: [WT(11, 0), WT(12, 0), WT(5, fl(ROCKCLIMB_FLAG))],  # w7 - bottom entrance
        11: [WT(10, 0), WT(12, 0), WT(5, fl(ROCKCLIMB_FLAG))],  # w9 - bottom entrance
        12: [WT(10, 0), WT(11, 0), WT(5, fl(ROCKCLIMB_FLAG))]  # w10 - bottom entrance
    },
    'Map_Victory_Road_Floor02_00': {
        0: [WT(1, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))],
        1: [WT(0, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))],
        2: []
    },
    'Map_Victory_Road_Floor03_01': {
        0: [],
        1: []
    },
    'Map_Victory_Road_Floor05_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Victory_Road_Floor06_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pal_Park_00': {
        0: [],
        1: []
    },
    'Map_Amity_Square_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Amity_Square_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Ravaged_Path_00': {
        0: [WT(1, fl(ROCKSMASH_FLAG))],
        1: [WT(0, fl(ROCKSMASH_FLAG))]
    },
    'Map_Floaroma_Meadow_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],  # top
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],  # top

        2: [WT(3, 0), WT(4, 0)],  # house

        3: [WT(4, 0), WT(2, 0)],  # bottom
        4: [WT(3, 0), WT(2, 0)]  # bottom
    },
    'Map_Fullmoon_Island_Interior_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Stark_Mountain_Room01_00': {
        0: [],
        1: []
    },
    'Map_Sendoff_Springs_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Turnback_Cave_Room01_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Turnback_Cave_Room02_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room03_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_03': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_04': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room04_05': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_03': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_04': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room05_05': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_03': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_04': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Turnback_Cave_Room06_05': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Snowpoint_Temple_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Snowpoint_Temple_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Snowpoint_Temple_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Snowpoint_Temple_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Snowpoint_Temple_04': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Wayward_Cave_Room01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Wayward_Cave_Room01_01': {
        0: [],
        1: []
    },
    'Map_Trophy_Garden_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Iron_Island_Room01_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Iron_Island_Room03_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Iron_Island_Room06_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0)],
        3: [WT(0, 0), WT(1, 0)]
    },
    'Map_Old_Chateau_Room01_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Old_Chateau_Room03_00': {
        0: [],
        1: []
    },
    'Map_Old_Chateau_Room04_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Galactic_HQ_Floor00_00': {
        0: [WT(1, 0), WT(3, fl(GALACTICKEY_FLAG))],
        1: [WT(0, 0), WT(3, fl(GALACTICKEY_FLAG))],
        2: [WT(6, 0)],
        3: [WT(0, fl(GALACTICKEY_FLAG)), WT(1, fl(GALACTICKEY_FLAG))],
        4: [WT(5, 0)],
        5: [WT(4, 0)],
        6: [WT(2, 0)]
    },
    'Map_Galactic_HQ_Floor00_01': {
        0: [],
        1: [WT(3, 0), WT(4, 0)],
        2: [],
        3: [WT(1, 0), WT(4, 0)],
        4: [WT(1, 0), WT(3, 0)],
        5: [WT(6, 0)],
        6: [WT(5, 0)],
        7: [WT(0, 0)]
    },
    'Map_Galactic_HQ_Floor01_00': {
        0: [WT(3, 0), WT(4, 0)],  # top left room
        1: [WT(5, 0)],  # mid left room
        2: [WT(11, 0), WT(14, 0), WT(7, 0)],  # center hallway
        3: [WT(0, 0), WT(4, 0)],  # top left room
        4: [WT(0, 0), WT(3, 0)],  # top left room
        5: [WT(1, 0)],  # mid left room
        6: [],  # left wall room
        7: [WT(11, 0), WT(14, 0), WT(2, 0)],  # center room
        8: [WT(9, 0)],  # bottom hall
        9: [WT(8, 0)],  # bottom hall

        10: [WT(12, 0)],  # bed room
        11: [WT(14, 0), WT(2, 0), WT(7, 0)],  # center hallway
        12: [WT(10, 0)],  # bed room
        13: [],  # right wall room
        14: [WT(11, 0), WT(2, 0), WT(7, 0)]  # center hallway
    },
    'Map_Galactic_HQ_Floor02_00': {
        0: [],
        1: [WT(2, 0)],
        2: [WT(1, 0)],
        3: [WT(4, 0), WT(5, 0)],
        4: [WT(3, 0), WT(5, 0)],
        5: [WT(3, 0), WT(4, 0)]
    },
    'Map_Galactic_HQ_Floor02_01': {
        0: [],
        1: [],
        2: []
    },
    'Map_Galactic_HQ_Floor03_00': {
        0: [WT(1, fl(GALACTICKEY_FLAG)), WT(2, fl(GALACTICKEY_FLAG)), WT(3, fl(GALACTICKEY_FLAG) | fl(GUARDIANSFREE_FLAG))],
        1: [WT(0, fl(GALACTICKEY_FLAG)), WT(2, fl(GUARDIANSFREE_FLAG)), WT(3, 0)],
        2: [WT(0, fl(GALACTICKEY_FLAG) | fl(GUARDIANSFREE_FLAG)), WT(1, fl(GUARDIANSFREE_FLAG)), WT(3, fl(GUARDIANSFREE_FLAG))],
        3: [WT(0, fl(GALACTICKEY_FLAG)), WT(1, 0), WT(2, fl(GUARDIANSFREE_FLAG))]
    },
    'Map_Galactic_HQ_Floor05_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Lake_Verity_Dummy_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Lake_Verity_00': {
        0: [WT(1, fl(SURF_FLAG)), WT(2, fl(SURF_FLAG))],
        1: [WT(2, 0), WT(0, fl(SURF_FLAG))],
        2: [WT(1, 0), WT(0, fl(SURF_FLAG))]
    },
    'Map_Lake_Valor_Bombed_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Lake_Valor_Normal_00': {
        0: [],
        1: [],
        2: [WT(3, 0), WT(4, fl(SURF_FLAG))],
        3: [WT(2, 0), WT(4, fl(SURF_FLAG))],

        4: [WT(2, fl(SURF_FLAG)), WT(3, fl(SURF_FLAG))]
    },
    'Map_Valor_Cavern_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Lake_Acuity_NoCave_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Lake_Acuity_WithCave_00': {
        0: [],
        1: [],
        2: [WT(3, 0), WT(4, fl(SURF_FLAG))],
        3: [WT(2, 0), WT(4, fl(SURF_FLAG))],

        4: [WT(2, fl(SURF_FLAG)), WT(3, fl(SURF_FLAG))]
    },
    'Map_Newmoon_Island_Interior_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, fl(ROCKSMASH_FLAG))],
        1: [WT(0, 0), WT(2, fl(ROCKSMASH_FLAG))],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Canalave_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Oreburgh_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, fl(ROCKSMASH_FLAG))],
        1: [WT(0, 0), WT(2, fl(ROCKSMASH_FLAG))],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Eterna_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Hearthome_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Pastoria_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Sunyshore_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Snowpoint_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Pokemon_League_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Fight_Area_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Sandgem_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, fl(ROCKSMASH_FLAG))],
        1: [WT(0, 0), WT(2, fl(ROCKSMASH_FLAG))],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Floaroma_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Solaceon_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Celestic_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Survival_Area_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Resort_Area_PokemonCenter_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Jubilife_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Canalave_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Oreburgh_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Eterna_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Hearthome_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Pastoria_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Veilstone_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Sunyshore_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Snowpoint_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Pokemon_League_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Fight_Area_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Sandgem_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Floaroma_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Solaceon_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Celestic_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Survival_Area_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Resort_Area_PokemonCenter_01': {
        0: [],
        1: []
    },
    'Map_Pokemon_League_PokemonCenter02_01': {
        0: [],
        1: []
    },
    'Map_Twinleaf_Rival_House_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Twinleaf_Your_House_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Sandgem_House01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_Building01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_Building02_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_Building03_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building02_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building03_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Building01_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Building01_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building_Unused_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building_Unused_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_Poketch_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Jubilife_Poketch_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Interior_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Grand_Lake_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_TV_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Jubilife_TV_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Jubilife_TV_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0)]
    },
    'Map_Jubilife_TV_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Hearthome_Amity_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Hearthome_Amity_Gate_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Gate_Unused_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Galactic_Building_Floor01_00': {
        0: [],
        1: [WT(2, 0), WT(3, 0)],
        2: [WT(1, 0), WT(3, 0)],
        3: [WT(1, 0), WT(2, 0)]
    },
    'Map_Eterna_Galactic_Building_Floor02_00': {
        0: [],
        1: [WT(2, 0), WT(3, 0)],
        2: [WT(1, 0), WT(3, 0)],
        3: [WT(1, 0), WT(2, 0)]
    },
    'Map_Eterna_Galactic_Building_Floor03_00': {
        0: [],
        1: []
    },
    'Map_Hearthome_Contest_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Veilstone_Mall_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Veilstone_Mall_01': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_Mall_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_Mall_03': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Veilstone_Mall_04': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Veilstone_Warehouse_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_Mansion_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Pokemon_Mansion_01': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Pokemon_Mansion_Room01_00': {
        0: [],
        1: [],
        2: []
    },
    'Map_Pastoria_Marsh_Entrance_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    # NOTE: The Elite Four / Champion rooms (Aaron, Bertha, Flint, Lucian,
    # Cynthia) are intentionally NOT listed here. Their two warps are merged into
    # a single logical door via forced_warp_pairs, which makes any internal
    # warp-to-warp routing rules redundant (and would conflict, since only warp 1
    # was keyed while the paired representative is warp 0).
    'Map_Pokemon_League_Interior_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Interior_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Interior_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Interior_04': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Interior_05': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_League_Cynthia_Room_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Hall_Of_Fame_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Battle_Tower_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Ribbon_Syndicate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pal_Park_Interior_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Global_Terminal_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Jubilife_Building01_02': {
        0: [],
        1: []
    },
    'Map_Jubilife_Building01_Unused_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Jubilife_Building02_01': {
        0: [],
        1: []
    },
    'Map_Jubilife_Building02_Unused_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Oreburgh_Building01_01': {
        0: [],
        1: []
    },
    'Map_Oreburgh_Building02_01': {
        0: [],
        1: []
    },
    'Map_Oreburgh_Building03_01': {
        0: [],
        1: []
    },
    'Map_Eterna_Building01_02': {
        0: [],
        1: []
    },
    'Map_Hearthome_House02_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Hearthome_House03_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_Tower_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_Tower_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_Tower_02': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Pokemon_Tower_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Canalave_Library_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Canalave_Library_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Gym_00': {
        0: [],
        1: []
    },
    'Map_Hearthome_Gym_00': {
        0: [],
        1: [WT(3, 0), WT(4, 0)],
        2: [],
        3: [WT(1, 0), WT(4, 0)],
        4: [WT(1, 0), WT(3, 0)]
    },
    'Map_Hearthome_Gym_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Hearthome_Gym_02': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Hearthome_Gym_Unused_06': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Hearthome_Gym_Unused_07': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Hearthome_Gym_03': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)],
        3: [WT(4, 0)],
        4: [WT(3, 0)]
    },
    'Map_Sunyshore_Gym_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Sunyshore_Gym_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Battle_Park_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Battle_Park_Interior_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Great_Marsh_05': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Veilstone_Mall_05': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Battle_Frontier_Interior_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Battle_Factory_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Battle_Hall_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Battle_Castle_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Battle_Arcade_00': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Battle_Frontier_03': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Battle_Frontier_02': {
        0: [WT(1, 0), WT(2, 0)],
        1: [WT(0, 0), WT(2, 0)],
        2: [WT(0, 0), WT(1, 0)]
    },
    'Map_Battle_Frontier_01': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(5, 0)],
        5: [WT(0, 0), WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0)]
    },
    'Map_Battle_Frontier_00': {
        0: [WT(1, 0), WT(4, 0)],
        1: [WT(0, 0), WT(4, 0)],
        2: [WT(3, 0)],
        3: [WT(2, 0)],
        4: [WT(0, 0), WT(1, 0)]
    },
    'Map_Route_212_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_225_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_214_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_208_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_209_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_215_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_213_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_218_Gate_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_218_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_222_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_228_Gate_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Route_206_Gate_01': {
        0: [WT(1, fl(BIKE_FLAG)), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(4, 0), WT(5, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, 0), WT(1, fl(BIKE_FLAG)), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(5, 0)],
        5: [WT(0, 0), WT(1, fl(BIKE_FLAG)), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(4, 0)]
    },
    'Map_Route_206_Gate_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        1: [WT(0, fl(BIKE_FLAG)), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(4, 0), WT(5, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0), WT(4, 0), WT(5, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0), WT(4, 0), WT(5, 0)],
        4: [WT(0, fl(BIKE_FLAG)), WT(1, 0), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(5, 0)],
        5: [WT(0, fl(BIKE_FLAG)), WT(1, 0), WT(2, fl(BIKE_FLAG)), WT(3, fl(BIKE_FLAG)), WT(4, 0)]
    },
    'Map_Galactic_HQ_Floor06_00': {
        0: [WT(1, 0)],
        1: [WT(0, fl(SPEECH_FLAG))],
        2: []
    },
    'Map_Global_Terminal_01': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Global_Terminal_00': {
        0: [WT(1, 0)],
        1: [WT(0, 0)]
    },
    'Map_Eterna_Galactic_Building_Floor00_00': {
        0: [WT(1, 0), WT(2, 0), WT(3, 0)],
        1: [WT(0, 0), WT(2, 0), WT(3, 0)],
        2: [WT(0, 0), WT(1, 0), WT(3, 0)],
        3: [WT(0, 0), WT(1, 0), WT(2, 0)]
    },
    'Map_Mount_Coronet_Exterior_00': {
        0: [WT(1, fl(ROCKCLIMB_FLAG)), WT(2, fl(ROCKCLIMB_FLAG))],
        1: [WT(0, fl(ROCKCLIMB_FLAG)), WT(2, 0)],
        2: [WT(0, fl(ROCKCLIMB_FLAG)), WT(1, 0)]
    },
    'Map_Mount_Coronet_Exterior_03': {
        0: [WT(1, fl(SURF_FLAG)), WT(2, fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG))],
        1: [WT(0, fl(SURF_FLAG)), WT(2, fl(ROCKCLIMB_FLAG))],
        2: [WT(0, fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG)), WT(1, fl(ROCKCLIMB_FLAG))]
    },
    'Map_Galactic_HQ_Floor04_00': {
        0: [WT(1, fl(GALACTICKEY_FLAG)), WT(2, 0)],

        1: [WT(0, 0)],

        2: [WT(0, 0)]
    }
}

map_to_map_warp_accessibility = {
    'Map_Pokemon_League_01': {
        'Map_Pokemon_League_00': WT(2, 0),
        'Map_Route_223_00': WT(0, fl(WATERFALL_FLAG))
    },
    'Map_Jubilife_City_02': {
        'Map_Jubilife_City_00': WT(0, fl(ROCKSMASH_FLAG)),
        'Map_Jubilife_City_03': WT(0, fl(ROCKSMASH_FLAG))
    },
    # Pretty sure this should be a connection_to_connection_rules scenario, but also not sure this check is even needed?
    'Map_Jubilife_City_01': {
        'Map_Route_203_00': WT(0, fl(TRAINERSCHOOL_FLAG))
    },
    'Map_ValleyWindworks_00': {
        'Map_Route_205_02': WT(0, fl(MEADOW_FLAG))
    },
    'Map_Fuego_Ironworks_00': {
        'Map_Floaroma_Town_00': WT(0, fl(SURF_FLAG)),
        'Map_Route_205_00': WT(0, fl(SURF_FLAG))
    },
    'Map_Eterna_Forest_Interior_00': {
        'Map_Eterna_Forest_Interior_01': WT(0, fl(CUT_FLAG))
    },
    'Map_Eterna_Forest_Interior_01': {
        'Map_Eterna_Forest_Interior_00': WT(0, fl(CUT_FLAG))
    },
    'Map_Victory_Road_Floor04_00': {
        'Map_Victory_Road_Floor04_01': WT(0, fl(SURF_FLAG))
    },
    'Map_Victory_Road_Floor04_01': {
        'Map_Victory_Road_Floor04_00': WT(0, fl(SURF_FLAG))
    },
    'Map_Stark_Mountain_Room02_00': {
        'Map_Stark_Mountain_Room02_01': WT(0, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))
    },
    'Map_Stark_Mountain_Room02_01': {
        'Map_Stark_Mountain_Room02_00': WT(0, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))
    },
    'Map_Route_213_00': {
        'Map_Valor_Lakefront_03': WT(4, 0)
    },
    'Map_Route_206_00': {
        'Map_Route_207_00': WT(12, 0)
    },
    'Map_Galactic_HQ_Floor02_00': {
        'Map_Galactic_HQ_Floor02_01': WT(3, 0)
    },
    'Map_Mount_Coronet_Floor07_00': {
        'Map_Mount_Coronet_Floor07_01': WT(0, fl(ROCKSMASH_FLAG) | fl(ROCKCLIMB_FLAG))
    },
    'Map_Mount_Coronet_Floor07_01': {
        'Map_Mount_Coronet_Floor07_00': WT(0, fl(ROCKSMASH_FLAG) | fl(ROCKCLIMB_FLAG))
    },
    'Map_Route_210_01': {
        'Map_Route_210_05': WT(0, fl(PSYDUCK_FLAG))
    },
    'Map_Route_210_05': {
        'Map_Route_210_01': WT(0, fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG))
    },
    'Map_Mount_Coronet_Floor09_00': {
        'Map_Mount_Coronet_Floor09_01': WT(2, fl(STRENGTH_FLAG))
    },
    'Map_Route_228_01': {
        'Map_Route_228_02': WT(0, fl(BIKE_FLAG))
    },
    'Map_Route_229_00': {
        'Map_Route_228_02': WT(0, fl(BIKE_FLAG))
    },
    'Map_Route_227_00': {
        'Map_Stark_Mountain_00': WT(0, fl(BIKE_FLAG))
    },
    'Map_Stark_Mountain_00': {
        'Map_Route_227_00': WT(0, fl(BIKE_FLAG))
    },
    'Map_Survival_Area_00': {
        'Map_Route_226_00': WT(0, fl(ROCKCLIMB_FLAG))
    },
    'Map_Route_226_00': {
        'Map_Survival_Area_00': WT(0, fl(ROCKCLIMB_FLAG)),
        'Map_Route_226_01': WT(0, fl(ROCKCLIMB_FLAG))
    },
    'Map_Route_226_01': {
        'Map_Route_226_00': WT(0, fl(ROCKCLIMB_FLAG)),
        'Map_Route_226_02': WT(0, fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG)),
    },
    'Map_Route_226_02': {
        'Map_Route_226_01': WT(0, fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG))
    },
    'Map_Route_227_01': {
        'Map_Route_226_02': WT(1, 0)
    },
    'Map_Oreburgh_City_01': {
        'Map_Oreburgh_City_00': WT(1, 0)
    },
    'Map_Sunyshore_City_01': {
        'Map_Sunyshore_City_03': WT(1, 0)
    },
    'Map_Sunyshore_City_02': {
        'Map_Sunyshore_City_03': WT(1, 0)
    },
    'Map_Canalave_City_00': {
        'Map_Iron_Island_00': WT(0, 0),
        'Map_Canalave_City_01': WT(4, 0),
    }
}

potential_softlock_warps = {
    'Map_Pokemon_League_Aaron_Room_00': [1],
    'Map_Pokemon_League_Bertha_Room_00': [1],
    'Map_Pokemon_League_Flint_Room_00': [1],
    'Map_Pokemon_League_Lucian_Room_00': [1],
    'Map_Pokemon_League_Cynthia_Room_00': [1],
    'Map_Hall_Of_Fame_01': [1],
    'Map_Hall_Of_Fame_00': [0],
    'Map_Canalave_City_00': [3],
    'Map_Survival_Area_00': [0],
    'Map_Galactic_HQ_Floor00_01': [7],
}

final_rooms = [
    'Map_Pokemon_League_Aaron_Room_00',
    'Map_Pokemon_League_Bertha_Room_00', 
    'Map_Pokemon_League_Flint_Room_00',
    'Map_Pokemon_League_Lucian_Room_00', 
    'Map_Pokemon_League_Cynthia_Room_00',
]

# ---------------------------------------------------------------------------
# Forced warp pairs (custom "treat these warps as one door" flagging)
#
# The randomizer normally groups two warps into a single logical door only when
# their tiles are physically adjacent (see compute_pairs_for_map). Some maps have
# an entrance and an exit that are NOT next to each other but should still be
# treated as one warp so that randomization never routes THROUGH the room.
#
# Format: { map_name: [ [warp_id, warp_id, ...], ... ] }
# Each inner list is one group of warp ids on that map that will be merged into a
# single warp (the first id in the group is kept as the representative).
# ---------------------------------------------------------------------------
forced_warp_pairs = {
    # Elite Four + Champion rooms: warp 0 (top / *_top) and warp 1 (bottom /
    # *_bot) are on opposite ends of the room. Pair them so both ends act as one
    # door and the randomizer can't route the player through the room.
    'Map_Pokemon_League_Aaron_Room_00': [[0, 1]],
    'Map_Pokemon_League_Bertha_Room_00': [[0, 1]],
    'Map_Pokemon_League_Flint_Room_00': [[0, 1]],
    'Map_Pokemon_League_Lucian_Room_00': [[0, 1]],
}

# Handles Connection Requirements
rocksmash_needed = [  # TODO make work for Plat

]
cut_needed = [  # TODO make work for Plat
    'Map_Eterna_Forest_00', 'Map_Eterna_Forest_01', 'Map_Eterna_Forest_02', 'Map_Eterna_Forest_03'
]
surf_needed = [  # TODO make work for Plat
    'Map_Route_220_00', 'Map_Route_220_01', 'Map_Route_219_00', 'Map_Route_218_00', 'Map_Route_230_00',
    'Map_Route_230_01', 'Map_Route_230_02', 'Map_Route_226_02', 'Map_Route_223_00', 'Map_Route_223_01',
    'Map_Route_223_02', 'Map_Route_223_03'
]
strength_needed = [  # TODO make work for Plat
    
]
rockclimb_needed = [  # TODO make work for Plat
    'Map_Route_210_05', 'Map_Route_226_00', 'Map_Route_226_01'
]
bike_needed = ['Map_Route_207_01', 'Map_Route_227_00']

# ---------------------------------------------------------------------------
# Per-map flag requirements
#
# A single lookup (map -> required flag bitmask) derived from the per-map
# requirement lists above. The bitmask uses the same 1<<FLAG encoding as the
# WT.flag values in map_warp_accessibility / map_to_map_warp_accessibility, so
# BOTH the randomizer's is_map_progressable AND the route/tracker reachability
# engine (reachable_room_warps) can gate on the exact same data via check_flags.
# Add a list here to have it honored by both engines automatically.
# ---------------------------------------------------------------------------
_per_map_flag_requirement_lists = [
    (SURF_FLAG, surf_needed),
    (ROCKSMASH_FLAG, rocksmash_needed),
    (CUT_FLAG, cut_needed),
    (BIKE_FLAG, bike_needed),
    (STRENGTH_FLAG, strength_needed),
    (ROCKCLIMB_FLAG, rockclimb_needed),
]

map_flag_requirements = {}
for _req_flag, _req_maps in _per_map_flag_requirement_lists:
    for _req_map in _req_maps:
        map_flag_requirements[_req_map] = map_flag_requirements.get(_req_map, 0) | (1 << _req_flag)

# TODO finish work for Plat
dont_randomize = [
    'Map_Twinleaf_Town_00', 'Map_Eterna_Gym_Unused_00', 'Map_Veilstone_Mall_Elevator_00', 'Map_Hearthome_Gym_Unused_06',
    'Map_Hearthome_Gym_Unused_01', 'Map_Hearthome_Gym_Unused_07', 'Map_Hearthome_Gym_Unused_02',
    'Map_Jubilife_TV_Elevator_00', 'Map_Hearthome_Elevator_00', 'Map_Hearthome_Gym_Unused_00',
    'Map_Union_Room', 'Map_Sandgem_Prof_Lab_00', 'Map_Pastoria_Marsh_Entrance_01', 'Map_Hearthome_Gym_Unused_03',
    'Map_Great_Marsh_05', 'Map_Pastoria_Marsh_Entrance_00', 'Map_Pastoria_Marsh_Entrance_01', 'Map_Hall_Of_Fame_01',
    'Map_Hall_Of_Fame_00', 'Map_Hearthome_Gym_Unused_05', 'Map_Hearthome_Gym_Unused_08',
    'Map_Jubilife_Unused_02', 'Map_Oreburgh_Building_Unused_00', 'Map_Oreburgh_Building_Unused_02',
    'Map_Oreburgh_Building_Unused_01', 'Map_Oreburgh_Building_Unused_03', 'Map_Hearthome_Gym_Unused_04',
    'Map_Oreburgh_Building_Unused_04', 'Map_Eterna_Building01_Unused_00', 'Map_Sunyshore_House04_00',
    'Map_Sunyshore_House05_00', 'Map_Hearthome_Gym_01', 'Map_Hearthome_Gym_02', 'Map_Hearthome_Gym_03',
    'Map_Battle_Park_00', 'Map_Battle_Park_Interior_00', 'Map_Sunyshore_Gym_01', 'Map_Sunyshore_Gym_02',
    'Map_Twinleaf_Rival_House', 'Map_Twinleaf_Your_House', 'Map_Jubilife_Trainer_School_00',
    'Map_Turnback_Cave_Room02_00', 'Map_Turnback_Cave_Room03_00', 'Map_Eterna_Gate_Unused_00',
    'Map_Turnback_Cave_Room04_00', 'Map_Turnback_Cave_Room04_01', 'Map_Turnback_Cave_Room04_02',
    'Map_Turnback_Cave_Room04_03', 'Map_Turnback_Cave_Room04_04', 'Map_Turnback_Cave_Room04_05',
    'Map_Turnback_Cave_Room05_00', 'Map_Turnback_Cave_Room05_01', 'Map_Turnback_Cave_Room05_02',
    'Map_Turnback_Cave_Room05_03', 'Map_Turnback_Cave_Room05_04', 'Map_Turnback_Cave_Room05_05',
    'Map_Turnback_Cave_Room06_00', 'Map_Turnback_Cave_Room06_01', 'Map_Turnback_Cave_Room06_02',
    'Map_Turnback_Cave_Room06_03', 'Map_Turnback_Cave_Room06_04', 'Map_Turnback_Cave_Room06_05'
]

dont_randomize_warp = {  # TODO finish work for Plat
    'Map_Turnback_Cave_Room01_00': [0, 1, 2, 3],
    'Map_Jubilife_Building01_02': [1],
    'Map_Spring_Path_02': [0, 1],
    'Map_Jubilife_Building02_01': [1],
    'Map_Jubilife_City_00': [2, 3],
    'Map_Lake_Acuity_WithCave_00': [1, 0],
    'Map_Lake_Valor_Normal_00': [1, 0]
}

not_needed = [  # TODO finish work for Plat
    'Map_Canalave_City_Room02_00', 'Map_Oreburgh_City_Room03_00', 'Map_Oreburgh_City_Room05_00',
    'Map_Oreburgh_City_Room07_00', 'Map_Pastoria_City_Room02_00', 'Map_Pastoria_City_Room03_00',
    'Map_Pastoria_City_Room05_00', 'Map_Pastoria_City_Room06_00', 'Map_Veilstone_City_Room08_00',
    'Map_Snowpoint_City_Room01_00', 'Map_Fight_Area_Room03_00', 'Map_Fight_Area_Room04_00',
    'Map_Floaroma_Meadow_Room01_00', 'Map_Route_222_Room01_00', 'Map_Route_222_Room02_00',
    'Map_Twinleaf_Town_Room03_00', 'Map_Twinleaf_Town_Room04_00', 'Map_Sandgem_Town_Room03_00',
    'Map_Floaroma_Town_Room02_00', 'Map_Floaroma_Town_Room03_00', 'Map_Solaceon_Town_Room02_00',
    'Map_Solaceon_Town_Room04_00', 'Map_Solaceon_Town_Room05_00', 'Map_Resort_Area_Room03_00',
    'Map_Route_225_Room01_00', 'Map_Jubilife_PokemonCenter_01', 'Map_Sandgem_PokemonCenter_01',
    'Map_Oreburgh_PokemonCenter_01', 'Map_Floaroma_PokemonCenter_01', 'Map_Eterna_PokemonCenter_01',
    'Map_Hearthome_PokemonCenter_01', 'Map_Pastoria_PokemonCenter_01', 'Map_Veilstone_PokemonCenter_01',
    'Map_Sunyshore_PokemonCenter_01', 'Map_Snowpoint_PokemonCenter_01', 'Map_Pokemon_League_PokemonCenter_01',
    'Map_Fight_Area_PokemonCenter_01', 'Map_Solaceon_PokemonCenter_01', 'Map_Celestic_PokemonCenter_01',
    'Map_Survival_Area_PokemonCenter_01', 'Map_Resort_Area_PokemonCenter_01', 'Map_Pokemon_League_PokemonCenter02_01',
    'Map_Jubilife_Shop_00', 'Map_Canalave_Shop_00', 'Map_Eterna_Shop_00', 'Map_Hearthome_Shop_00',
    'Map_Sunyshore_Shop_00', 'Map_Snowpoint_Shop_00', 'Map_Fight_Area_Shop_00', 'Map_Sandgem_Shop_00',
    'Map_Floaroma_Shop_00', 'Map_Solaceon_Shop_00', 'Map_Survival_Area_Shop_00',
    'Map_Union_Room', 'Map_Ruin_Maniac_Cave_00', 'Map_Ruin_Maniac_Cave_01', 'Map_Jubilife_Gym_00',
    'Map_Jubilife_Building01_Unused_00', 'Map_Jubilife_Unused_00', 'Map_Jubilife_Building02_Unused_00',
    'Map_Jubilife_Building02_Unused_02', 'Map_Jubilife_Unused_01', 'Map_Ribbon_Syndicate_Elevator_00',
    'Map_Ribbon_Syndicate_Unused_00', 'Map_Lighthouse_Elevator_00', 'Map_Hearthome_House02_01',
    'Map_Hearthome_Elevator_00', 'Map_Hearthome_House03_01', 'Map_Hearthome_Elevator_01', 'Map_Hearthome_House03_00',
    'Map_Pokemon_League_Interior_01', 'Map_Pokemon_League_Interior_02', 'Map_Pokemon_League_Interior_03',
    'Map_Pokemon_League_Interior_04', 'Map_Pokemon_League_Interior_05', 'Map_Lake_Acuity_NoCave_00',
    'Map_Lake_Verity_Dummy_00', 'Map_Jubilife_PokemonCenter_02', 'Map_Sandgem_PokemonCenter_02',
    'Map_Oreburgh_PokemonCenter_02', 'Map_Floaroma_PokemonCenter_02', 'Map_Eterna_PokemonCenter_02',
    'Map_Hearthome_PokemonCenter_02', 'Map_Pastoria_PokemonCenter_02', 'Map_Veilstone_PokemonCenter_02',
    'Map_Sunyshore_PokemonCenter_02', 'Map_Snowpoint_PokemonCenter_02', 'Map_Pokemon_League_PokemonCenter_02',
    'Map_Fight_Area_PokemonCenter_02', 'Map_Solaceon_PokemonCenter_02', 'Map_Celestic_PokemonCenter_02',
    'Map_Survival_Area_PokemonCenter_02', 'Map_Resort_Area_PokemonCenter_02', 'Map_Pokemon_League_PokemonCenter02_02',
    'Map_Resort_Area_Shop_00', 'Map_Fullmoon_Island_00', 'Map_Newmoon_Island_00', 'Map_Lake_Valor_Bombed_00',
    'Map_Spear_Pillar_Normal_00', 'Map_Spear_Pillar_DistoEvent_00', 'Map_Spear_Pillar_DP_Leftover02',
    'Map_Lake_Valor_Bombed_01', 'Map_Pal_Park_Interior_00', 'Map_Pal_Park_00', 'Map_Distortion_World_00',
    'Map_Ribbon_Syndicate_00', 'Map_Villa_00', 'Map_Oreburgh_Shop_00'
]

non_navigable_connections = [  # TODO finish work for Plat
    ['Map_Canalave_City_01', 'Map_Route_218_00'], ['Map_Route_218_00', 'Map_Canalave_City_01'],
    ['Map_Mount_Coronet_Floor01_00', 'Map_Mount_Coronet_Floor01_01']
]

connection_to_connection_rules = {
    'Map_Route_205_02': {'Map_Route_205_01': 4},
    'Map_Route_205_01': {'Map_Route_205_02': 4},
    'Map_Eterna_Forest_02': {'Map_Route_205_00': 16, 'Map_Eterna_Forest_03': 16},
    'Map_Eterna_Forest_01': {'Map_Route_205_03': 16, 'Map_Eterna_Forest_03': 16},
    'Map_Route_205_00': {'Map_Fuego_Ironworks_00': 2048},
    'Map_Route_218_00': {'Map_Route_218_01': 2048},
    'Map_Route_218_01': {'Map_Route_218_00': 2048},
    'Map_Mount_Coronet_Floor01_01': {'Map_Mount_Coronet_Floor01_00': 2048}
}

grouped_warps = {
    # "Lake Verity": {
    #     'warps': {
    #         "Map_Lake_Verity_Dummy_00": [0, 1],
    #         "Map_Lake_Verity_00": [1, 2]
    #     },
    #     'header_dummy': 0x5,
    #     'resource_folder': 'verity',
    # },

    # "Lake Valor": {
    #     'warps': {
    #         "Map_Lake_Valor_Normal_00": [0, 1, 2, 3]
    #     },
    # },
    #
    # "Lake Acuity": {
    #     'warps': {
    #         "Map_Lake_Acuity_WithCave_00": [1, 2, 3, 4]
    #     },
    # },

    # "Tornworld": {
    #     'warps': {
    #         "Map_Distortion_World_00": [0],
    #     },
    #     'header_dummy': 0x1B,
    #     'resource_folder': 'tornworld'
    # },
}

other_overwrites = {
    "Tornworld_return": {
        'header_dummy': 0x1F,
        'resource_folder': 'tornworld_return',
        'script_overwrite': 380,
    },
    "Aaron E4": {
        'resource_folder': 'league_aaron',
        'script_overwrite': 188,
    },
    "Bertha E4": {
        'resource_folder': 'league_bertha',
        'script_overwrite': 190,
    },
    "Flint E4": {
        'resource_folder': 'league_flint',
        'script_overwrite': 192,
    },
    "Lucian E4": {
        'resource_folder': 'league_lucian',
        'script_overwrite': 194,
    },
    "Player House": {
        'resource_folder': 'player_house',
        'script_overwrite': 1056,
    },
    "Veilstone Warehouse": {
        'resource_folder': 'veilstone_warehouse',
        'script_overwrite': 149,
    },
    "Spear Pillar": {
        'warps': {
            "Map_Spear_Pillar_Leftover01": [0],
        },
        'resource_folder': 'pillar',
        'script_overwrite': 239,
        'event_overwrite': 525,
        'map_overwrite': 635,
        'text_overwrite': 237
    },
    "Spear Pillar 2": {
        'resource_folder': 'pillar',
        'map_overwrite': 636
    },
    "Coronet 2F": {
        'resource_folder': 'coronet_2f',
        'event_overwrite': 205
    },
    "Cyrus Office": {
        'resource_folder': 'cyrus_office',
        'event_overwrite': 296
    },
    "Valor Lakefront": {
        'resource_folder': 'valor_lakefront',
        'event_overwrite': 322
    },
    "Iron Ruins": {
        'resource_folder': 'registeel_chamber',
        'script_overwrite': 392
    },
    "Iceberg Ruins": {
        'resource_folder': 'regice_chamber',
        'script_overwrite': 394
    },
    "Rock Peak Ruins": {
        'resource_folder': 'regirock_chamber',
        'script_overwrite': 396
    },
    "Route 216": {
        'resource_folder': 'route_216',
        'event_overwrite': 371
    },
    "Fight Area": {
        'resource_folder': 'fight_area',
        'event_overwrite': 187
    },
    "Eterna City": {
        'resource_folder': 'eterna_city',
        'event_overwrite': 64,
        'script_overwrite': 71,
    },
    "Galactic Eterna 1F": {
        'resource_folder': 'galactic_eterna',
        'event_overwrite': 71
    },
    "Route 221": {
        'resource_folder': 'route_221',
        'event_overwrite': 378
    },
    "Newmoon Island": {
        'resource_folder': 'newmoon_island',
        'script_overwrite': 363
    },
    "Victory Road 1F": {
        'resource_folder': 'victory_1f',
        'event_overwrite': 238
    },
    "Sandgem Center": {
        'resource_folder': 'sandgem_center',
        'event_overwrite': 399
    },
    "Jubilife Center": {
        'resource_folder': 'jubilife_center',
        'event_overwrite': 5
    },
    "Route 218": {
        'resource_folder': 'route_218',
        'event_overwrite': 374
    },
    "Snowpoint City": {
        'resource_folder': 'snowpoint_city',
        'event_overwrite': 164
    },
    "Contest Hall": {
        'resource_folder': 'contest_hall',
        'script_overwrite': 119
    },
    "Coronet 1F 2": {
        'resource_folder': 'coronet_1f',
        'event_overwrite': 213
    },
    "Jubilife City": {
        'resource_folder': 'jubilife',
        'event_overwrite': 2,
        'script_overwrite': 2
    },
    "Pastoria City": {
        'resource_folder': 'pastoria',
        'event_overwrite': 119,
        'script_overwrite': 123
    },
    "Route 230": {
        'resource_folder': 'route_230',
        'event_overwrite': 449
    },
    "Stark Mountain": {
        'resource_folder': 'stark_mountain',
        'event_overwrite': 255,
        'script_overwrite': 283,
        'text_overwrite': 261
    },
    "Eterna Forest": {
        'resource_folder': 'eterna_forest',
        'event_overwrite': 201
    },
    "Coronet 1F": {
        'resource_folder': 'coronet_1f_2',
        'event_overwrite': 215
    },
    "Floaroma Town": {
        'resource_folder': 'floaroma',
        'event_overwrite': 405
    },
    "Veilstone City": {
        'resource_folder': 'veilstone',
        'event_overwrite': 131,
        'script_overwrite': 136
    },
    "Pokemon League Lobby": {
        'resource_folder': 'league_lobby',
        'script_overwrite': 186
    }
}

override_maps = [
    'Map_Jubilife_Building01_Unused_00', 'Map_Jubilife_Unused_00', 'Map_Jubilife_Building02_Unused_00',
    'Map_Jubilife_Building02_Unused_02', 'Map_Jubilife_Unused_01'
]


def search_for_needed_maps(event_maps, accesible_maps):
    ret = True
    for req in event_maps:
        map_name = req
        warp_parts = []
        if ':' in req:
            map_name = req.split(':')[0]
            warp_parts = req.split(':')
        if map_name not in accesible_maps:
            ret = False
            break
        if len(warp_parts) != 0:
            original_length = len(warp_parts)
            for warp in accesible_maps[map_name]:
                if str(warp) in warp_parts:
                    warp_parts.remove(str(warp))
            if len(warp_parts) == original_length:
                ret = False
                break
    return ret


def check_progession_blockers(flag, accesible_maps):  # TODO make work for Plat
    if flag == TRAINERSCHOOL_FLAG:
        return search_for_needed_maps(trainerschool_event, accesible_maps)
    elif flag == ROCKSMASH_FLAG:
        return search_for_needed_maps(rocksmash_event, accesible_maps)
    elif flag == WINDWORKS_FLAG:
        return search_for_needed_maps(windworks_event, accesible_maps)
    elif flag == FLASH_FLAG:
        return search_for_needed_maps(flash_event, accesible_maps)
    elif flag == CUT_FLAG:
        return search_for_needed_maps(cut_event, accesible_maps)
    elif flag == BIKE_FLAG:
        return search_for_needed_maps(bike_event, accesible_maps)
    elif flag == CONTESTHALL_FLAG:
        return search_for_needed_maps(constesthall_event, accesible_maps)
    elif flag == HEARTHOMEGYM_FLAG:
        return search_for_needed_maps(hearthomegym_event, accesible_maps)
    elif flag == DEFOG_FLAG:
        return search_for_needed_maps(defog_event, accesible_maps)
    elif flag == FLY_FLAG:
        return search_for_needed_maps(fly_event, accesible_maps)
    elif flag == PSYDUCK_FLAG:
        return search_for_needed_maps(psyduck_event, accesible_maps)
    elif flag == SURF_FLAG:
        return search_for_needed_maps(surf_event, accesible_maps)
    elif flag == STRENGTH_FLAG:
        return search_for_needed_maps(strength_event, accesible_maps)
    elif flag == LAKES_FLAG:
        return search_for_needed_maps(lakes_event, accesible_maps)
    elif flag == VALOR_FLAG:
        return search_for_needed_maps(valor_event, accesible_maps)
    elif flag == VERITY_FLAG:
        return search_for_needed_maps(verity_event, accesible_maps)
    elif flag == ROCKCLIMB_FLAG:
        return search_for_needed_maps(rockclimb_event, accesible_maps)
    elif flag == GALACTICKEY_FLAG:
        return search_for_needed_maps(galactickey_event, accesible_maps)
    elif flag == LIGHTHOUSE_FLAG:
        return search_for_needed_maps(lighthouse_event, accesible_maps)
    elif flag == WATERFALL_FLAG:
        return search_for_needed_maps(waterfall_event, accesible_maps)
    elif flag == MEADOW_FLAG:
        return search_for_needed_maps(meadow_event, accesible_maps)
    elif flag == SPEECH_FLAG:
        return search_for_needed_maps(speech_event, accesible_maps)
    elif flag == GUARDIANSFREE_FLAG:
        return search_for_needed_maps(guardiansfree_event, accesible_maps)
    elif flag == VEILSTONEGYM_FLAG:
        return search_for_needed_maps(veilstonegym_event, accesible_maps)
    elif flag == ROARK_FLAG:
        return search_for_needed_maps(roark_event, accesible_maps)
    else:
        return False
    # for flag_num in range(len(FLAG_EVENT_LIST)):
    #     if flag_num == flag:
    #         return search_for_needed_maps(FLAG_EVENT_LIST[flag], accesible_maps)
    # return False


# If warp_id = -1 we check connection, otherwise we check if there is an accessible warp from warp id
# noinspection DuplicatedCode
def is_map_progressable(map, accesible_maps, warp_id, ignore=False):  # TODO make work for Plat
    # Per-map flag/HM gate. Driven by map_flag_requirements so the route/tracker
    # reachability engine (reachable_room_warps) enforces the exact same rules.
    required_flags = map_flag_requirements.get(map, 0)
    if required_flags:
        index = 0
        bits = required_flags
        while bits:
            if (bits & 1) and not check_progession_blockers(index, accesible_maps):
                return False
            bits >>= 1
            index += 1
    if warp_id == -1 and not ignore:
        if map not in map_warp_accessibility:
            return True
        map_warps = map_warp_accessibility[map].keys()
        for map_warp in map_warps:
            if is_map_progressable(map, accesible_maps, map_warp):
                return True
        return False
    if warp_id != -1:
        if map not in map_warp_accessibility:
            return True
        if warp_id not in map_warp_accessibility[map]:
            return True
        potential_warps = map_warp_accessibility[map][warp_id]
        if len(potential_warps) == 0:
            return True
        for potential_warp in potential_warps:
            bits = bin(potential_warp.flag)
            index = 0
            warp_pass = True
            for bit in reversed(bits):
                if bit == '1':
                    if not check_progession_blockers(index, accesible_maps):
                        warp_pass = False
                        break
                index = index + 1
            if warp_pass:
                return True
        return False
    else:
        return True


def is_warp_to_warp_valid(map, accesible_maps, from_warp_id, to_warp_id):
    if map not in map_warp_accessibility:
        return True  # If map doesn't specify warp routing all warps are accessible
    if from_warp_id not in map_warp_accessibility[map]:
        return False  # If warp id isnt in map specifications, warp is not meant to be randomized
    potential_warps = map_warp_accessibility[map][from_warp_id]
    for potential_warp in potential_warps:
        if potential_warp.warp_id != to_warp_id:
            continue
        bits = bin(potential_warp.flag)
        index = 0
        warp_pass = True
        for bit in reversed(bits):
            if bit == '1':
                if not check_progession_blockers(index, accesible_maps):
                    warp_pass = False
                    break
            index = index + 1
        if warp_pass:
            return True
    return False


def is_warp_ready(warp_tuple: WT, accesible_maps):
    bits = bin(warp_tuple.flag)
    index = 0
    warp_pass = True
    for bit in reversed(bits):
        if bit == '1':
            if not check_progession_blockers(index, accesible_maps):
                warp_pass = False
                break
        index = index + 1
    return warp_pass
