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


class ZT:
    def __init__(self, zone_id, flag):
        if isinstance(zone_id, int) and isinstance(flag, int):
            self.zone_id = zone_id
            self.flag = flag
        else:
            raise ValueError("Invalid Zone Tuple")


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


def permutate(zone_ids, flag):
    return {
        source: [ZT(target, flag) for target in zone_ids if target != source]
        for source in zone_ids
    }


def merge_rules(*rule_maps):
    merged = {}
    for rule_map in rule_maps:
        for source, rules in rule_map.items():
            source_rules = merged.setdefault(source, [])
            target_indices = {rule.zone_id: index for index, rule in enumerate(source_rules)}
            for rule in rules:
                if rule.zone_id in target_indices:
                    source_rules[target_indices[rule.zone_id]] = rule
                else:
                    target_indices[rule.zone_id] = len(source_rules)
                    source_rules.append(rule)
    return merged

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

final_rooms = ['Map_Pokemon_League_Aaron_Room_00',
 'Map_Pokemon_League_Bertha_Room_00',
 'Map_Pokemon_League_Flint_Room_00',
 'Map_Pokemon_League_Lucian_Room_00',
 'Map_Pokemon_League_Cynthia_Room_00']

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
forced_warp_pairs = {'Map_Pokemon_League_Aaron_Room_00': [[0, 1]],
 'Map_Pokemon_League_Bertha_Room_00': [[0, 1]],
 'Map_Pokemon_League_Flint_Room_00': [[0, 1]],
 'Map_Pokemon_League_Lucian_Room_00': [[0, 1]]}

# ---------------------------------------------------------------------------
# Zone-based accessibility
#
# SOURCES:
#   * The game data (every map, its warps, and its seamless connections) lives in
#     the JSON file Resources/gen4/PlatinumMapResources.json. That JSON is the
#     source of truth for WHAT warps/connections exist.
#   * The zone_accessibility table below, in this .py file
#     (nds/gen4/PlatinumWarpMapInfo.py), is the source of truth for HOW those
#     warps/connections reach each other. "Referenced" always means "referenced
#     by the zone_accessibility table in this .py file", and "warp"/"connection"
#     always means an entry that exists in the .json file.
#
# A referenced map may define:
#   * 'zones': list of zones. Zone members are warp ids (int) or connection map
#     names (str), both drawn from that map's entry in the .json file. Everything
#     in one zone is mutually reachable.
#   * 'rules': one-way zone-to-zone movement, as {from_zone: [ZT(to_zone, flag)]}.
#
# Zone rules are intentionally NON-TRANSITIVE. A rule means "from this zone,
# these target zones are directly reachable". This preserves modeling freedom for maps
# whose direct reachability is intentionally not transitive; maps that should be
# fully connected should state that explicitly with helpers such as permutate().
#
# Members that exist in the .json file but are left unreferenced on a map that
# IS referenced by the .py zone_accessibility table (i.e. the map appears in the
# table but does not list that member in any of its zones) are handled by MEMBER
# TYPE:
#
#   * Warp id (int) omitted from every zone -> that warp is intentionally OUTSIDE
#     the zone graph. It is not "defined for randomization"
#     (is_member_defined_for_randomization returns False), has no accessible exit,
#     and cannot be routed to or from by zone reachability. Use this to freeze a
#     warp out of the shuffle. To keep a warp in the graph but isolated, give it
#     its own single-member zone with no rules instead of omitting it.
#
#   * Connection string (str) omitted from every zone -> that connection stays an
#     implicit FREE connection, entering the map through warp 0's zone (or zone 0
#     if warp 0 is not zoned). It remains freely usable with no gating. Add the
#     connection string to a zone only when it needs explicit routing, gating, or
#     isolation.
#
# This literal table is the single source of Platinum zone definitions (the .py
# side); it references the map/warp/connection data defined in the .json file.
#
# A map from the .json file that is not referenced by the zone_accessibility
# table in this .py file is treated as one big zone: every warp and every
# seamless connection on that map can reach every other warp/connection.
# ---------------------------------------------------------------------------
USES_ZONE_ACCESSIBILITY = True


zone_accessibility = {
    'Map_Acuity_Lakefront_02': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Amity_Square_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Amity_Square_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Battle_Arcade_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Battle_Castle_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Battle_Factory_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Battle_Frontier_00': {
        'zones': [
            [0, 1, 4],
            [2, 3],
        ],
    },
    'Map_Battle_Frontier_01': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Battle_Frontier_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Battle_Frontier_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Battle_Frontier_Interior_00': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Battle_Hall_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Battle_Park_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Battle_Park_Interior_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Battle_Tower_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Canalave_City_00': {
        'zones': [
            [0, 1, 2, 4, 'Map_Canalave_City_01', 'Map_Iron_Island_00'],
            [3],
        ],
        'rules': {
            1: [ZT(0, 0)],
        },
    },
    'Map_Canalave_City_01': {
        'zones': [
            [0, 1, 3, 4],
            [2, 5],
            # Non-navigable connection to Route_218_00 (blocked): isolated zone
            # with no rules so it can never be traversed to.
            ['Map_Route_218_00'],
        ],
    },
    'Map_Canalave_Library_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Canalave_Library_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Canalave_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Canalave_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Celestic_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Celestic_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Celestic_Town_00': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Eterna_Building01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Eterna_Building01_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Eterna_Building01_02': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Eterna_City_00': {
        'zones': [
            [0, 1, 3, 4],
            [2],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
    },
    'Map_Eterna_City_02': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Eterna_Forest_00': {
        'zones': [
            ['Map_Eterna_Forest_01'],
            ['Map_Eterna_Forest_02'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Eterna_Forest_01': {
        'zones': [
            ['Map_Route_205_03'],
            ['Map_Eterna_Forest_03'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Eterna_Forest_02': {
        'zones': [
            ['Map_Eterna_Forest_03'],
            ['Map_Route_205_00'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Eterna_Forest_03': {
        'zones': [
            ['Map_Eterna_Forest_01'],
            ['Map_Eterna_Forest_02'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Eterna_Forest_Interior_00': {
        'zones': [
            [0],
            ['Map_Eterna_Forest_Interior_01'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
    },
    'Map_Eterna_Forest_Interior_01': {
        'zones': [
            [0, 1],
            ['Map_Eterna_Forest_Interior_00'],
        ],
        'rules': permutate([0, 1], fl(CUT_FLAG)),
    },
    'Map_Eterna_Forest_Interior_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Eterna_Galactic_Building_Floor00_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Eterna_Galactic_Building_Floor01_00': {
        'zones': [
            [0],
            [1, 2, 3],
        ],
    },
    'Map_Eterna_Galactic_Building_Floor02_00': {
        'zones': [
            [0],
            [1, 2, 3],
        ],
    },
    'Map_Eterna_Galactic_Building_Floor03_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Eterna_Gate_Unused_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Eterna_Gym_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Eterna_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Eterna_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Fight_Area_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Fight_Area_01': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Fight_Area_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Fight_Area_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Floaroma_Meadow_00': {
        'zones': [
            [0, 1],
            [2, 3, 4],
        ],
        'rules': {
            0: [ZT(1, 0)],
        },
    },
    'Map_Floaroma_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Floaroma_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Floaroma_Town_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Floaroma_Town_01': {
        'zones': [
            [0, 1, 2, 3, 4, 5, 6],
        ],
    },
    'Map_Fuego_Ironworks_00': {
        'zones': [
            [0, 1, 2],
            ['Map_Floaroma_Town_00'],
            ['Map_Route_205_00'],
        ],
        # On main, map_to_map_warp_accessibility routes all connections through
        # warp 0, so connection<->connection traversal is gated the same way as
        # warp<->connection (SURF). The zone model needs explicit conn<->conn
        # rules to match this.
        'rules': merge_rules(
            permutate([0, 1], fl(SURF_FLAG)),
            permutate([0, 2], fl(SURF_FLAG)),
            permutate([1, 2], fl(SURF_FLAG)),
        ),
    },
    'Map_Fullmoon_Island_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Fullmoon_Island_Interior_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Galactic_HQ_Floor00_00': {
        'zones': [
            [0, 1],
            [2, 6],
            [3],
            [4, 5],
        ],
        'rules': permutate([0, 2], fl(GALACTICKEY_FLAG)),
    },
    'Map_Galactic_HQ_Floor00_01': {
        'zones': [
            [0],
            [1, 3, 4],
            [2],
            [5, 6],
            [7],
        ],
        'rules': {
            4: [ZT(0, 0)],
        },
    },
    'Map_Galactic_HQ_Floor01_00': {
        'zones': [
            [0, 3, 4],
            [1, 5],
            [2, 7, 11, 14],
            [6],
            [8, 9],
            [10, 12],
            [13],
        ],
    },
    'Map_Galactic_HQ_Floor02_00': {
        'zones': [
            [0],
            [1, 2],
            [3, 4, 5, 'Map_Galactic_HQ_Floor02_01'],
        ],
    },
    'Map_Galactic_HQ_Floor02_01': {
        'zones': [
            [0],
            [1],
            [2],
        ],
    },
    'Map_Galactic_HQ_Floor03_00': {
        'zones': [
            [0],
            [1],
            [2],
            [3],
        ],
        'rules': {
            0: [ZT(1, fl(GALACTICKEY_FLAG)), ZT(2, fl(GALACTICKEY_FLAG)),
                ZT(3, fl(GALACTICKEY_FLAG) | fl(GUARDIANSFREE_FLAG))],
            1: [ZT(0, fl(GALACTICKEY_FLAG)), ZT(2, fl(GUARDIANSFREE_FLAG)), ZT(3, 0)],
            2: [ZT(0, fl(GALACTICKEY_FLAG) | fl(GUARDIANSFREE_FLAG)),
                ZT(1, fl(GUARDIANSFREE_FLAG)), ZT(3, fl(GUARDIANSFREE_FLAG))],
            3: [ZT(0, fl(GALACTICKEY_FLAG)), ZT(1, 0), ZT(2, fl(GUARDIANSFREE_FLAG))],
        },
    },
    'Map_Galactic_HQ_Floor04_00': {
        'zones': [
            [0],
            [1],
            [2],
        ],
        'rules': merge_rules({
            0: [ZT(1, fl(GALACTICKEY_FLAG))],
            1: [ZT(0, 0)],
        }, permutate([0, 2], 0)),
    },
    'Map_Galactic_HQ_Floor05_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Galactic_HQ_Floor06_00': {
        'zones': [
            [0],
            [1],
            [2],
        ],
        'rules': {
            0: [ZT(1, 0)],
            1: [ZT(0, fl(SPEECH_FLAG))],
        },
    },
    'Map_Global_Terminal_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Global_Terminal_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Global_Terminal_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Grand_Lake_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Great_Marsh_05': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hall_Of_Fame_00': {
        'zones': [
            [0],
        ],
    },
    'Map_Hall_Of_Fame_01': {
        'zones': [
            [0],
            [1],
        ],
        'rules': {
            0: [ZT(1, 0)],
        },
    },
    'Map_Hearthome_Amity_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hearthome_Amity_Gate_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hearthome_City_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Hearthome_City_01': {
        'zones': [
            [0, 1, 3],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(CONTESTHALL_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Hearthome_City_02': {
        'zones': [
            [0, 1, 2],
            [3, 4, 5, 6],
        ],
    },
    'Map_Hearthome_City_03': {
        'zones': [
            [0, 1],
            [2],
            [3],
        ],
        'rules': merge_rules({
            0: [ZT(1, fl(HEARTHOMEGYM_FLAG)), ZT(2, fl(HEARTHOMEGYM_FLAG))],
            1: [ZT(0, 0)],
            2: [ZT(0, 0)],
        }, permutate([1, 2], fl(HEARTHOMEGYM_FLAG))),
    },
    'Map_Hearthome_Contest_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hearthome_Gym_00': {
        'zones': [
            [0],
            [1, 3, 4],
            [2],
        ],
    },
    'Map_Hearthome_Gym_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Hearthome_Gym_02': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Hearthome_Gym_03': {
        'zones': [
            [0, 1, 2],
            [3, 4],
        ],
    },
    'Map_Hearthome_Gym_Unused_06': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Hearthome_Gym_Unused_07': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Hearthome_House02_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hearthome_House03_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Hearthome_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Hearthome_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Iron_Island_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': {
            1: [ZT(0, 0)],
        },
    },
    'Map_Iron_Island_Room01_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Iron_Island_Room03_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Iron_Island_Room06_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Jubilife_Building01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_Building01_02': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Jubilife_Building01_Unused_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_Building02_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_Building02_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Jubilife_Building02_Unused_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_Building03_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_City_00': {
        'zones': [
            [0, 1, 4, 5],
            [2],
            [3],
        ],
    },
    'Map_Jubilife_City_01': {
        'zones': [
            [0, 1, 2],
            ['Map_Route_203_00'],
        ],
        'rules': permutate([0, 1], fl(TRAINERSCHOOL_FLAG)),
    },
    'Map_Jubilife_City_02': {
        'zones': [
            [0, 1],
            ['Map_Jubilife_City_00'],
            ['Map_Jubilife_City_03'],
        ],
        'rules': merge_rules(
            permutate([0, 1], fl(ROCKSMASH_FLAG)),
            permutate([0, 2], fl(ROCKSMASH_FLAG)),
        ),
    },
    'Map_Jubilife_City_03': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Jubilife_PokemonCenter_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(ROCKSMASH_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Jubilife_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Jubilife_Poketch_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Jubilife_Poketch_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Jubilife_TV_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Jubilife_TV_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Jubilife_TV_02': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Jubilife_TV_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Lake_Acuity_NoCave_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Lake_Acuity_WithCave_00': {
        'zones': [
            [0],
            [1],
            [2, 3],
            [4],
        ],
        'rules': permutate([2, 3], fl(SURF_FLAG)),
    },
    'Map_Lake_Valor_Bombed_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Lake_Valor_Normal_00': {
        'zones': [
            [0],
            [1],
            [2, 3],
            [4],
        ],
        'rules': permutate([2, 3], fl(SURF_FLAG)),
    },
    'Map_Lake_Verity_00': {
        'zones': [
            [0],
            [1, 2],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Lake_Verity_Dummy_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Mount_Coronet_Exterior_00': {
        'zones': [
            [0],
            [1, 2],
        ],
        'rules': permutate([0, 1], fl(ROCKCLIMB_FLAG)),
    },
    'Map_Mount_Coronet_Exterior_03': {
        'zones': [
            [0],
            [1],
            [2],
        ],
        'rules': merge_rules(
            permutate([0, 1], fl(SURF_FLAG)),
            permutate([0, 2], fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG)),
            permutate([1, 2], fl(ROCKCLIMB_FLAG)),
        ),
    },
    'Map_Mount_Coronet_Floor00_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG))],
            1: [ZT(0, fl(ROCKCLIMB_FLAG))],
        },
    },
    'Map_Mount_Coronet_Floor01_00': {
        # On main, Floor01_00 -> Floor01_01 is non-navigable (blocked), but
        # Floor01_01 -> Floor01_00 is NOT blocked; it requires SURF via
        # connection_to_connection_rules on Floor01_01 and enters at warp 0
        # (starting_warp defaults to 0 since no map_to_map_warp_accessibility).
        'zones': [
            [0],
            [1, 2],
            [3],
            ['Map_Mount_Coronet_Floor01_01'],
        ],
        # One-way: entering from Floor01_01 can reach warp 0 for free.
        # No reverse rule keeps the non-navigable Floor01_00 -> Floor01_01 block.
        'rules': {
            3: [ZT(0, 0)],
        },
    },
    'Map_Mount_Coronet_Floor01_01': {
        'zones': [
            [0],
            [1],
            ['Map_Mount_Coronet_Floor01_00'],
        ],
        # Warps 0<->1 require STRENGTH. The Floor01_01 -> Floor01_00 connection
        # requires SURF (matching main's connection_to_connection_rules).
        'rules': merge_rules(
            permutate([0, 1], fl(STRENGTH_FLAG)),
            {0: [ZT(2, fl(SURF_FLAG))], 1: [ZT(2, fl(SURF_FLAG))]},
        ),
    },
    'Map_Mount_Coronet_Floor02_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Mount_Coronet_Floor03_00': {
        'zones': [
            [0],
            [1],
            [2],
            [3],
            [4],
        ],
        'rules': merge_rules(
            permutate([0, 4], fl(ROCKCLIMB_FLAG)),
            permutate([1, 2], fl(SURF_FLAG) | fl(WATERFALL_FLAG)),
        ),
    },
    'Map_Mount_Coronet_Floor04_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Mount_Coronet_Floor05_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Mount_Coronet_Floor06_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Mount_Coronet_Floor07_00': {
        'zones': [
            [0],
            ['Map_Mount_Coronet_Floor07_01'],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG) | fl(ROCKCLIMB_FLAG)),
    },
    'Map_Mount_Coronet_Floor07_01': {
        'zones': [
            [0],
            ['Map_Mount_Coronet_Floor07_00'],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG) | fl(ROCKCLIMB_FLAG)),
    },
    'Map_Mount_Coronet_Floor08_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Mount_Coronet_Floor09_00': {
        'zones': [
            [0],
            ['Map_Mount_Coronet_Floor09_01'],
        ],
        'rules': permutate([0, 1], fl(STRENGTH_FLAG)),
    },
    'Map_Mount_Coronet_Floor09_01': {
        'zones': [
            [0],
            [1],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(STRENGTH_FLAG)), ZT(2, fl(STRENGTH_FLAG))],
            1: [ZT(2, fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG))],
            2: [ZT(1, fl(STRENGTH_FLAG))],
        },
    },
    'Map_Newmoon_Island_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Newmoon_Island_Interior_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Old_Chateau_Room01_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Old_Chateau_Room03_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Old_Chateau_Room04_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Oreburgh_Building01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Oreburgh_Building01_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Oreburgh_Building02_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Oreburgh_Building02_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Oreburgh_Building03_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Oreburgh_Building03_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Oreburgh_Building_Unused_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Oreburgh_Building_Unused_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Oreburgh_City_00': {
        'zones': [
            [0],
            [1, 2, 3, 4, 5],
        ],
        'rules': {
            0: [ZT(1, 0)],
            1: [ZT(0, fl(ROARK_FLAG))],
        },
    },
    'Map_Oreburgh_City_01': {
        'zones': [
            [0, 1, 2, 3, 'Map_Oreburgh_City_00'],
        ],
    },
    'Map_Oreburgh_City_02': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Oreburgh_Gate_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG)),
    },
    'Map_Oreburgh_Mine_Room01_00': {
        'zones': [
            [0, 1, 2, 3, 4, 5],
        ],
    },
    'Map_Oreburgh_PokemonCenter_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(ROCKSMASH_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Oreburgh_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pal_Park_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pal_Park_Interior_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pastoria_City_00': {
        'zones': [
            [0],
            [1, 2],
        ],
        'rules': {
            0: [ZT(1, 0)],
            1: [ZT(0, fl(VEILSTONEGYM_FLAG))],
        },
    },
    'Map_Pastoria_City_01': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Pastoria_City_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pastoria_Marsh_Entrance_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pastoria_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pastoria_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_01': {
        'zones': [
            [0, 1, 3, 4],
            [2, 5, 6, 'Map_Pokemon_League_00'],
            ['Map_Route_223_00'],
        ],
        'rules': permutate([0, 2], fl(WATERFALL_FLAG)),
    },
    'Map_Pokemon_League_Aaron_Room_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_Bertha_Room_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_Cynthia_Room_00': {
        'zones': [
            [0],
            [1],
        ],
        'rules': {
            0: [ZT(1, 0)],
        },
    },
    'Map_Pokemon_League_Flint_Room_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_Interior_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Pokemon_League_Interior_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_League_Interior_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_League_Interior_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_League_Interior_04': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_League_Interior_05': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_League_Lucian_Room_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_PokemonCenter02_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_League_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pokemon_League_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Pokemon_Mansion_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pokemon_Mansion_01': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Pokemon_Mansion_Room01_00': {
        'zones': [
            [0],
            [1],
            [2],
        ],
    },
    'Map_Pokemon_Tower_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_Tower_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_Tower_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Pokemon_Tower_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Ravaged_Path_00': {
        'zones': [
            [0],
            [1],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG)),
    },
    'Map_Resort_Area_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Resort_Area_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Resort_Area_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Ribbon_Syndicate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_205_00': {
        'zones': [
            [0, 1, 2],
            ['Map_Fuego_Ironworks_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Route_205_01': {
        'zones': [
            ['Map_Route_205_00'],
            ['Map_Route_205_02'],
        ],
        'rules': {
            0: [ZT(1, fl(WINDWORKS_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Route_205_02': {
        'zones': [
            ['Map_ValleyWindworks_00', 'Map_Floaroma_Town_01'],
            ['Map_Route_205_01'],
        ],
        'rules': {
            0: [ZT(1, fl(WINDWORKS_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Route_205_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_206_00': {
        'zones': [
            [0, 1, 6, 7, 8, 9, 10, 11],
            [2, 3],
            [4, 5, 12, 13, 'Map_Route_207_00'],
        ],
        'rules': permutate([1, 2], fl(CUT_FLAG)),
    },
    'Map_Route_206_Gate_00': {
        'zones': [
            [0, 2, 3],
            [1, 4, 5],
        ],
        'rules': {
            0: [ZT(1, 0)],
            1: [ZT(0, fl(BIKE_FLAG))],
        },
    },
    'Map_Route_206_Gate_01': {
        'zones': [
            [0, 4, 5],
            [1, 2, 3],
        ],
        'rules': {
            0: [ZT(1, fl(BIKE_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Route_207_01': {
        'zones': [
            [0],
            [1],
            ['Map_Route_207_00'],
        ],
        # Warps 0/1 are standable dead-ends. Entering from the connection is
        # free (matching main where include_starting_warp adds warp 0 before
        # the progressability check), but leaving requires BIKE (matching
        # main's bike_needed per-map gate via is_map_progressable).
        'rules': {
            2: [ZT(0, 0)],
            0: [ZT(2, fl(BIKE_FLAG))],
        },
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_208_01': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Route_208_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_209_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_209_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_210_01': {
        'zones': [
            [0],
            ['Map_Route_210_05'],
        ],
        'rules': permutate([0, 1], fl(PSYDUCK_FLAG)),
    },
    'Map_Route_210_05': {
        'zones': [
            [0],
            ['Map_Route_210_00'],
            ['Map_Route_210_04'],
            ['Map_Route_210_01'],
        ],
        # Route_210_05 is rock-climb terrain. Entering from any connection you can
        # still stand at (randomize) warp 0 for free -- matching the flat model,
        # which adds a gated map's warps to the pool before blocking its exits --
        # but LEAVING warp 0 to any connection needs ROCKCLIMB (and additionally
        # PSYDUCK for the Route_210_01 border). Connection<->connection therefore
        # routes through warp 0 and is gated the same way.
        'rules': {
            0: [ZT(1, fl(ROCKCLIMB_FLAG)), ZT(2, fl(ROCKCLIMB_FLAG)),
                ZT(3, fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG))],
            1: [ZT(0, 0)],
            2: [ZT(0, 0)],
            3: [ZT(0, 0)],
        },
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_212_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_212_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_213_00': {
        'zones': [
            [0, 1, 3, 7],
            [2, 4, 5, 'Map_Valor_Lakefront_03'],
            [6],
        ],
        'rules': permutate([1, 2], fl(ROCKCLIMB_FLAG)),
    },
    'Map_Route_213_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_214_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Route_214_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_215_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_215_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_218_00': {
        'zones': [
            [0, 1],
            ['Map_Route_218_01'],
            # Non-navigable connection to Canalave_City_01 (blocked): isolated
            # zone with no rules so it can never be traversed to/from.
            ['Map_Canalave_City_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_218_01': {
        'zones': [
            [0, 1],
            ['Map_Route_218_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Route_218_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_218_Gate_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_219_00': {
        'zones': [
            ['Map_Sandgem_Town_00'],
            ['Map_Route_220_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_220_00': {
        'zones': [
            ['Map_Route_219_00'],
            ['Map_Route_220_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_220_01': {
        'zones': [
            ['Map_Route_221_00'],
            ['Map_Route_220_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_221_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_222_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Route_222_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_223_00': {
        'zones': [
            ['Map_Pokemon_League_01'],
            ['Map_Route_223_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_223_01': {
        'zones': [
            ['Map_Route_223_00'],
            ['Map_Route_223_02'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_223_02': {
        'zones': [
            ['Map_Route_223_01'],
            ['Map_Route_223_03'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_223_03': {
        'zones': [
            ['Map_Route_223_02'],
            ['Map_Sunyshore_City_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_225_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_225_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_226_00': {
        'zones': [
            [0],
            ['Map_Route_226_01'],
            ['Map_Survival_Area_00'],
        ],
        'rules': permutate([0, 1, 2], fl(ROCKCLIMB_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_226_01': {
        'zones': [
            [0],
            ['Map_Route_226_00'],
            ['Map_Route_226_02'],
        ],
        'rules': merge_rules(
            permutate([0, 1], fl(ROCKCLIMB_FLAG)),
            permutate([1, 2], fl(ROCKCLIMB_FLAG)),
            permutate([0, 2], fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG)),
        ),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_226_02': {
        'zones': [
            [0],
            [1],
            [2],
            ['Map_Route_226_01'],
        ],
        'rules': merge_rules(
            permutate([0, 1, 2, 3], fl(SURF_FLAG)),
            permutate([0, 3], fl(SURF_FLAG) | fl(ROCKCLIMB_FLAG)),
        ),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_227_00': {
        # Route_227_00 is a pass-through map with no warps. On main the forward
        # path (Route_227_01 -> Stark_Mountain) is permanently blocked by the
        # map_to_map_warp_accessibility starting_warp < 0 check. The return path
        # (Stark_Mountain -> Route_227_01) is allowed because Route_227_01 is
        # NOT in map_to_map_warp_accessibility and therefore bypasses the check.
        # Both directions also require BIKE via per-map bike_needed.
        'zones': [
            ['Map_Stark_Mountain_00'],
            ['Map_Route_227_01'],
        ],
        # One-way rule: Stark -> Route_227_01 (matches main). No reverse rule
        # blocks the forward path Route_227_01 -> Stark (matches main).
        'rules': {
            0: [ZT(1, fl(BIKE_FLAG))],
        },
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_227_01': {
        'zones': [
            [0, 'Map_Route_226_02'],
        ],
    },
    'Map_Route_228_00': {
        'zones': [
            [0, 1],
            [2],
            [3],
        ],
        'rules': merge_rules(
            permutate([0, 1], fl(BIKE_FLAG)),
            permutate([0, 2], fl(BIKE_FLAG)),
        ),
    },
    'Map_Route_228_01': {
        'zones': [
            [0],
            ['Map_Route_228_02'],
        ],
        'rules': permutate([0, 1], fl(BIKE_FLAG)),
    },
    'Map_Route_228_Gate_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Route_229_00': {
        'zones': [
            [0],
            ['Map_Route_228_02'],
        ],
        'rules': permutate([0, 1], fl(BIKE_FLAG)),
    },
    'Map_Route_230_00': {
        'zones': [
            ['Map_Route_230_01'],
            ['Map_Fight_Area_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Route_230_01': {
        'zones': [
            ['Map_Route_230_02'],
            ['Map_Route_230_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Route_230_02': {
        'zones': [
            ['Map_Route_229_00'],
            ['Map_Route_230_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
        'legacy_report_in_is_map_progressable': True,
    },
    'Map_Sandgem_House01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Sandgem_PokemonCenter_00': {
        'zones': [
            [0, 1],
            [2],
        ],
        'rules': {
            0: [ZT(1, fl(ROCKSMASH_FLAG))],
            1: [ZT(0, 0)],
        },
    },
    'Map_Sandgem_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Sandgem_Town_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Sendoff_Springs_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_City_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Snowpoint_City_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Snowpoint_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Snowpoint_Temple_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_Temple_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_Temple_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_Temple_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Snowpoint_Temple_04': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Solaceon_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Solaceon_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Solaceon_Ruins_Room01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Solaceon_Ruins_Room02_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Solaceon_Ruins_Room03_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Solaceon_Ruins_Room05_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Solaceon_Ruins_Room05_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Solaceon_Ruins_Room07_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Solaceon_Ruins_Room08_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Solaceon_Town_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Solaceon_Town_01': {
        'zones': [
            [0],
            [1],
            [2],
            [3],
        ],
    },
    'Map_Spring_Path_02': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Stark_Mountain_00': {
        'zones': [
            [0],
            ['Map_Route_227_00'],
        ],
        'rules': permutate([0, 1], fl(BIKE_FLAG)),
    },
    'Map_Stark_Mountain_Room01_00': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Stark_Mountain_Room02_00': {
        'zones': [
            [0],
            ['Map_Stark_Mountain_Room02_01'],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG)),
    },
    'Map_Stark_Mountain_Room02_01': {
        'zones': [
            [0],
            ['Map_Stark_Mountain_Room02_00'],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG)),
    },
    'Map_Sunyshore_City_00': {
        'zones': [
            [0, 4],
            [1],
            [2],
            [3],
        ],
        'rules': {
            0: [ZT(3, fl(LIGHTHOUSE_FLAG))],
            3: [ZT(0, 0)],
        },
    },
    'Map_Sunyshore_City_01': {
        'zones': [
            [0, 1, 'Map_Sunyshore_City_03'],
        ],
    },
    'Map_Sunyshore_City_02': {
        'zones': [
            [0, 1, 2, 3, 4, 'Map_Sunyshore_City_03'],
        ],
    },
    'Map_Sunyshore_City_03': {
        'zones': [
            [0],
            [1],
        ],
        'rules': permutate([0, 1], fl(ROCKCLIMB_FLAG)),
    },
    'Map_Sunyshore_Gym_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Sunyshore_Gym_01': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Sunyshore_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Sunyshore_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Survival_Area_00': {
        'zones': [
            [0],
            [1, 3, 4],
            [2],
            ['Map_Route_226_00'],
        ],
        'rules': merge_rules(
            {0: [ZT(1, 0)]},
            {3: [ZT(0, fl(ROCKCLIMB_FLAG))]},
        ),
    },
    'Map_Survival_Area_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Survival_Area_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Trophy_Garden_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Turnback_Cave_Room01_00': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Turnback_Cave_Room02_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room03_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_02': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_03': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_04': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room04_05': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_02': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_03': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_04': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room05_05': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_02': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_03': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_04': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Turnback_Cave_Room06_05': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Twinleaf_Rival_House_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Twinleaf_Town_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Twinleaf_Your_House_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_ValleyWindworks_00': {
        'zones': [
            [0],
            ['Map_Route_205_02'],
        ],
        'rules': permutate([0, 1], fl(MEADOW_FLAG)),
    },
    'Map_Valor_Cavern_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Valor_Lakefront_01': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Valor_Lakefront_03': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Veilstone_City_00': {
        'zones': [
            [0, 1],
            [2],
            [3],
        ],
        'rules': {
            0: [ZT(2, fl(VEILSTONEGYM_FLAG))],
            1: [ZT(0, 0), ZT(2, fl(VEILSTONEGYM_FLAG))],
            2: [ZT(0, 0)],
        },
    },
    'Map_Veilstone_City_01': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Veilstone_City_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Veilstone_City_03': {
        'zones': [
            [0, 1, 2, 3, 4],
        ],
    },
    'Map_Veilstone_Mall_00': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Veilstone_Mall_01': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Veilstone_Mall_02': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Veilstone_Mall_03': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Veilstone_Mall_04': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Veilstone_Mall_05': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Veilstone_PokemonCenter_00': {
        'zones': [
            [0, 1, 2],
        ],
    },
    'Map_Veilstone_PokemonCenter_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Veilstone_Warehouse_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Verity_Lakefront_03': {
        'zones': [
            [0, 1, 2, 3],
        ],
    },
    'Map_Victory_Road_Floor01_00': {
        'zones': [
            [0],
            [1, 9],
            [2, 3, 4],
            [5],
            [6],
            [7],
            [8],
            [10, 11, 12],
        ],
        'rules': merge_rules(
            permutate([3, 7], fl(ROCKCLIMB_FLAG)),
            permutate([4, 5], fl(ROCKCLIMB_FLAG)),
            permutate([0, 1, 2], fl(ROCKCLIMB_FLAG)),
            {
                0: [ZT(3, fl(ROCKCLIMB_FLAG)), ZT(4, fl(ROCKCLIMB_FLAG)), ZT(5, fl(ROCKCLIMB_FLAG)), ZT(7, fl(ROCKCLIMB_FLAG))],
                1: [ZT(3, 0), ZT(4, fl(ROCKCLIMB_FLAG)), ZT(5, 0), ZT(7, fl(ROCKCLIMB_FLAG))],
                2: [ZT(3, fl(ROCKCLIMB_FLAG)), ZT(4, fl(ROCKCLIMB_FLAG)), ZT(5, fl(ROCKCLIMB_FLAG)), ZT(7, fl(ROCKCLIMB_FLAG))],
                4: [ZT(7, fl(ROCKCLIMB_FLAG)), ZT(3, fl(ROCKCLIMB_FLAG))],
                5: [ZT(7, fl(ROCKCLIMB_FLAG)), ZT(3, 0)],
            }
        ),
    },
    'Map_Victory_Road_Floor02_00': {
        'zones': [
            [0],
            [1],
            [2],
        ],
        'rules': permutate([0, 1], fl(ROCKSMASH_FLAG) | fl(STRENGTH_FLAG)),
    },
    'Map_Victory_Road_Floor03_01': {
        'zones': [
            [0],
            [1],
        ],
    },
    'Map_Victory_Road_Floor04_00': {
        'zones': [
            [0],
            ['Map_Victory_Road_Floor04_01'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Victory_Road_Floor04_01': {
        'zones': [
            [0],
            ['Map_Victory_Road_Floor04_00'],
        ],
        'rules': permutate([0, 1], fl(SURF_FLAG)),
    },
    'Map_Victory_Road_Floor05_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Victory_Road_Floor06_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Wayward_Cave_Room01_00': {
        'zones': [
            [0, 1],
        ],
    },
    'Map_Wayward_Cave_Room01_01': {
        'zones': [
            [0],
            [1],
        ],
    },
}

def _zone_member_sort_key(member):
    if isinstance(member, int):
        return 0, member
    return 1, member


def _build_zone_views():
    zones = {}
    rules = {}
    lookup = {}
    legacy_maps = set()
    for map_name, entry in zone_accessibility.items():
        if 'zones' in entry:
            zones[map_name] = entry['zones']
            lookup[map_name] = {}
            for zone_id, zone_members in enumerate(entry['zones']):
                for member in zone_members:
                    lookup[map_name][member] = zone_id
        if 'rules' in entry:
            rules[map_name] = entry['rules']
        if entry.get('legacy_report_in_is_map_progressable'):
            legacy_maps.add(map_name)
    return zones, rules, lookup, legacy_maps


map_zones, zone_to_zone_rules, _zone_member_lookup, _legacy_is_map_progressable_maps = _build_zone_views()


def _compute_legacy_map_progressable_flag(map_name):
    """Bitwise AND of every non-zero flag across all zone-to-zone rules.

    Returns 0 when the map has no rules, no non-zero flags, or is not in
    the zone tables.

    If you do not get the result you expect you may have to add flags to the rules in the .json
    """
    combined = None  # None = "no non-zero flag seen yet"
    rules_for_map = zone_to_zone_rules.get(map_name, {})
    for zone_rules in rules_for_map.values():
        for zt in zone_rules:
            if zt.flag != 0:
                if combined is None:
                    combined = zt.flag
                else:
                    combined &= zt.flag
    return combined if combined is not None else 0


def _sync_zone_accessibility_map(map_name):
    entry = zone_accessibility.setdefault(map_name, {})
    if map_name in map_zones:
        entry['zones'] = map_zones[map_name]
    else:
        entry.pop('zones', None)
    if map_name in zone_to_zone_rules:
        entry['rules'] = zone_to_zone_rules[map_name]
    else:
        entry.pop('rules', None)

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


# Zone reachability helpers --------------------------------------------------

def _progression_mask_ready(flag_mask, accesible_maps):
    index = 0
    bits = flag_mask
    while bits:
        if (bits & 1) and not check_progession_blockers(index, accesible_maps):
            return False
        bits >>= 1
        index += 1
    return True


def _flag_vector_ready(flag_mask, flags_satisfied):
    if flags_satisfied is None:
        return True
    index = 0
    bits = flag_mask
    while bits:
        if (bits & 1) and (index >= len(flags_satisfied) or flags_satisfied[index] != 1):
            return False
        bits >>= 1
        index += 1
    return True


def get_member_zone(map_name, member):
    if map_name not in map_zones:
        return 0  # implicit default whole-map zone
    zone_id = _zone_member_lookup.get(map_name, {}).get(member)
    if zone_id is None and isinstance(member, str):
        # Most legacy map rules only described warp-to-warp routing; seamless
        # connections that were not explicitly listed remained freely usable.
        # In zone terms, an unlisted connection enters the map through warp 0's
        # zone when possible, otherwise through zone 0.
        return _zone_member_lookup.get(map_name, {}).get(0, 0)
    return zone_id


def is_explicit_zone_member(map_name, member):
    return map_name in map_zones and member in _zone_member_lookup.get(map_name, {})


def is_member_defined_for_randomization(map_name, member):
    # Unreferenced maps use the implicit all-members zone. Referenced maps only
    # randomize members that were placed into a zone.
    return map_name not in map_zones or get_member_zone(map_name, member) is not None


def is_member_ready_with_flags(map_name, member, flags_satisfied):
    zone_id = get_member_zone(map_name, member)
    return zone_id is not None


def reachable_zone_ids(map_name, source_member, accesible_maps):
    """Directly reachable zone ids from source_member under current flags.

    This is intentionally non-transitive: rules describe direct reachability,
    not graph edges to BFS through. That keeps the zone model equivalent to the
    old map_warp_accessibility direct lookup while still allowing zones to group
    mutually reachable warps/connections.
    """
    source_zone = get_member_zone(map_name, source_member)
    if source_zone is None:
        return set()
    if map_name not in map_zones:
        return {0}

    reached = {source_zone}
    for zone_tuple in zone_to_zone_rules.get(map_name, {}).get(source_zone, []):
        if _progression_mask_ready(zone_tuple.flag, accesible_maps):
            reached.add(zone_tuple.zone_id)
    return reached


def reachable_zone_ids_with_flags(map_name, source_member, flags_satisfied):
    """Directly reachable zone ids from source_member under a flag vector.

    Non-transitive for the same reason as reachable_zone_ids().
    """
    source_zone = get_member_zone(map_name, source_member)
    if source_zone is None:
        return set()
    if map_name not in map_zones:
        return {0}

    reached = {source_zone}
    for zone_tuple in zone_to_zone_rules.get(map_name, {}).get(source_zone, []):
        if _flag_vector_ready(zone_tuple.flag, flags_satisfied):
            reached.add(zone_tuple.zone_id)
    return reached


def is_member_to_member_valid(map_name, accesible_maps, from_member, to_member):
    from_zone = get_member_zone(map_name, from_member)
    if from_zone is None:
        return False
    # Unlisted connections keep the historical default: if you can stand in
    # your current zone, you can walk out through that connection. Explicitly
    # zoned connection strings opt into stricter zone-to-zone routing.
    # This check must come before get_member_zone(to_member) because unlisted
    # connections return None from get_member_zone.
    if isinstance(to_member, str) and not is_explicit_zone_member(map_name, to_member):
        return from_zone in reachable_zone_ids(map_name, from_member, accesible_maps)
    to_zone = get_member_zone(map_name, to_member)
    if to_zone is None:
        return False
    return to_zone in reachable_zone_ids(map_name, from_member, accesible_maps)


def get_reachable_members(map_name, from_member, accesible_maps):
    if map_name not in map_zones:
        return None  # caller should use the implicit all-members map data
    reached_zones = reachable_zone_ids(map_name, from_member, accesible_maps)
    members = []
    for zone_id in reached_zones:
        members.extend(map_zones[map_name][zone_id])
    return members


def get_reachable_members_with_flags(map_name, from_member, flags_satisfied):
    if map_name not in map_zones:
        return None  # caller should use the implicit all-members map data
    reached_zones = reachable_zone_ids_with_flags(map_name, from_member, flags_satisfied)
    members = []
    for zone_id in reached_zones:
        members.extend(map_zones[map_name][zone_id])
    return members


def zone_member_has_accessible_exit(map_name, member):
    if map_name not in map_zones:
        return True
    zone_id = get_member_zone(map_name, member)
    if zone_id is None:
        return False
    if len(map_zones[map_name][zone_id]) > 1:
        return True
    # Check if any outgoing rule (ignoring flags — map_warp_divide mirrors
    # main's static map_warp_accessibility) leads to a zone that contains
    # at least one other WARP member.  Rules leading only to connection
    # strings do not make the warp a "connect".
    for zone_tuple in zone_to_zone_rules.get(map_name, {}).get(zone_id, []):
        target_zone = zone_tuple.zone_id
        if target_zone >= len(map_zones[map_name]):
            continue
        for m in map_zones[map_name][target_zone]:
            if isinstance(m, int) and m != member:
                return True
    return False


def get_member_to_member_flag_mask(map_name, from_member, to_member, flags_satisfied=None):
    from_zone = get_member_zone(map_name, from_member)
    to_zone = get_member_zone(map_name, to_member)
    if from_zone is None or to_zone is None:
        return 0
    if map_name not in map_zones:
        return 0

    if from_zone == to_zone:
        return 0
    for zone_tuple in zone_to_zone_rules.get(map_name, {}).get(from_zone, []):
        if zone_tuple.zone_id == to_zone and _flag_vector_ready(zone_tuple.flag, flags_satisfied):
            return zone_tuple.flag
    return 0


def _rebuild_zone_lookup_for_map(map_name):
    _zone_member_lookup[map_name] = {}
    for zone_id, zone_members in enumerate(map_zones.get(map_name, [])):
        for member in zone_members:
            _zone_member_lookup[map_name][member] = zone_id


def redirect_paired_warp_ids(map_name, paired_ids):
    # Pair removal collapses the randomization availability pool, not the map's
    # physical reachability model. Zone data is authoritative: paired doors that
    # should be freely reachable are listed in the same zone, while noisy models
    # can intentionally split paired members and gate them with rules. Rewriting
    # zones here destroys that distinction, so this hook is intentionally a no-op
    # for the zone-accessibility model.
    return


# If warp_id = -1 we check whether any zone on the map can be traversed;
# otherwise we check whether the incoming warp's zone can currently reach any
# other member (warp/connection). A warp whose zone can only reach itself given
# the currently-satisfied flags is a dead end -- e.g. a warp stranded behind an
# unmet HM gate expressed as a zone rule.
#
# IMPORTANT: a warp in a single-member zone with NO outgoing rules (not even
# unsatisfied ones) is a standable dead-end, matching main's behaviour where
# map_warp_accessibility[warp_id] = [] always returns True (progressable).
# Only warps behind an UNMET gate are not progressable.
def is_map_progressable(map, accesible_maps, warp_id, ignore=False):
    if warp_id == -1:
        # Legacy per-map flag: mirrors main's bike_needed / cut_needed etc.
        # by checking the union of all zone-rule flags on the map.  Runs even
        # when ignore=True because the connection-traversal loop in
        # build_warps_to_randomize calls with ignore=True.  This is a
        # temporary bridge — once all regressions pass, test data can be
        # regenerated and the variable removed.
        if map in _legacy_is_map_progressable_maps:
            legacy_flag = _compute_legacy_map_progressable_flag(map)
            if legacy_flag and not _progression_mask_ready(legacy_flag, accesible_maps):
                return False
        if not ignore:
            # Progressable if ANY warp on the map can progress to another member.
            warp_members = [m for zone in map_zones.get(map, []) for m in zone if isinstance(m, int)]
            if not warp_members:
                return True  # implicit/unzoned map: assume progressable
            return any(is_map_progressable(map, accesible_maps, w) for w in warp_members)
    if warp_id != -1:
        zone_id = get_member_zone(map, warp_id)
        if zone_id is None:
            return False
        if map not in map_zones:
            return True  # implicit whole-map zone: every member is mutually reachable
        for reached_zone in reachable_zone_ids(map, warp_id, accesible_maps):
            for member in map_zones[map][reached_zone]:
                # Only count OTHER WARP members as making this warp progressable.
                # Connection members are zone-routing targets, not progress proofs
                # (matching main's is_map_progressable which only checks
                # map_warp_accessibility, never connections).
                if isinstance(member, int) and member != warp_id:
                    return True  # can progress to some other warp
        # No other warp reachable under current flags. If the warp has no
        # outgoing rules at all (not just unsatisfied ones), it is a standable
        # dead-end: progressable (matching main's [] behaviour). If it HAS
        # rules that are currently unmet, it is gated: not progressable.
        has_outgoing_rules = len(zone_to_zone_rules.get(map, {}).get(zone_id, [])) > 0
        if not has_outgoing_rules:
            return True
        return False
    return True


def is_warp_to_warp_valid(map, accesible_maps, from_warp_id, to_warp_id):
    return is_member_to_member_valid(map, accesible_maps, from_warp_id, to_warp_id)


def is_warp_ready(warp_tuple: WT, accesible_maps):
    return _progression_mask_ready(warp_tuple.flag, accesible_maps)
