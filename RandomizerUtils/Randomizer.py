"""
Randomizer.py

Core file containing the randomizer

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
import json
import sys
import os
import logging
import tempfile
import shutil
import zipfile

from RandomizerUtils import Definitions
from gen3 import EmeraldWarpRandomizer, FireRedWarpRandomizer
from nds.gen4 import PlatinumWarpRandomizer, PlatinumWarpMapInfo
from nds.gen4 import JohtoWarpRandomizer
from nds.gen5 import White2WarpRandomizer
import RandomizerUtils.Definitions
import RandomizerUtils.StructureDefinitions as structs
import RandomizerUtils.RandomGenerator as random_generator


def iter_visit_order(gen_functions, flag_order=None):
    """
    Yield the flag events in progression order as
    ``(section, header, flag, new_maps)``.

    When ``flag_order`` is given it is an explicit sequence of flag indices (a
    real acquisition timeline). Every event is yielded in that exact order inside
    a single ``'progression'`` section, numbered sequentially, so the output
    reads naturally from first-obtained to last-obtained.

    When ``flag_order`` is ``None`` the legacy grouping is used: ``'forced'`` for
    entries in ``FORCED_FLAG_ORDER`` (numbered in their forced sequence) followed
    by ``'others'`` for every remaining flag event in ``FLAG_EVENT_LIST`` index
    order. ``header`` is a display label such as ``'1. rocksmash_event'`` and
    ``flag`` is the flag index the event corresponds to.

    Flag event lists are cumulative (a later event repeats the maps required by
    earlier events), so ``new_maps`` contains only the map/warp requirement
    strings not already yielded by an earlier event -- i.e. the *new* maps
    unlocked by reaching that event.
    """
    info_module = gen_functions.info()
    forced_order = getattr(info_module, 'FORCED_FLAG_ORDER', [])
    flag_event_list = getattr(info_module, 'FLAG_EVENT_LIST', [])

    # Resolve each FLAG_EVENT_LIST entry to its module-level variable name
    # (e.g. 'trainerschool_event') by mapping the event object back to its name
    # via object identity. Unresolved entries fall back to '<unknown>'.
    name_by_id = {id(value): name for name, value in vars(info_module).items()}
    event_names = [name_by_id.get(id(event), '<unknown>') for event in flag_event_list]

    seen_maps = set()

    def new_maps_for(flag):
        result = []
        for req in flag_event_list[flag]:
            if req in seen_maps:
                continue  # already unlocked by an earlier event, not a new map
            seen_maps.add(req)
            result.append(req)
        return result

    # Explicit timeline: emit every event in acquisition order, numbered 1..N.
    if flag_order is not None:
        for position, flag in enumerate(flag_order, start=1):
            yield 'progression', '%d. %s' % (position, event_names[flag]), flag, new_maps_for(flag)
        return

    # Legacy grouping (used when no timeline is available, e.g. logging).
    # Forced flags first, in their required order.
    for position, flag in enumerate(forced_order, start=1):
        yield 'forced', '%d. %s' % (position, event_names[flag]), flag, new_maps_for(flag)

    # Everything not in the forced order, in FLAG_EVENT_LIST index order.
    for flag in range(len(flag_event_list)):
        if flag in forced_order:
            continue
        yield 'others', event_names[flag], flag, new_maps_for(flag)


def build_visit_order_lines(gen_functions, extra_lines_for_map=None, flag_order=None):
    """
    Build the grouped visit-order text (see ``iter_visit_order``) as a list of
    lines. Each new map is written as ``To <map>[:warp]``; groups with no new
    maps get a placeholder line. ``extra_lines_for_map`` is an optional callback
    ``(req, flag) -> [str, ...]`` whose lines are appended right after each
    ``To`` line (used to attach a route to reach that map). ``flag_order`` is
    forwarded to ``iter_visit_order`` to emit events in an explicit timeline.
    """
    lines = []
    section = None
    for group_section, header, flag, new_maps in iter_visit_order(gen_functions, flag_order=flag_order):
        if group_section == 'others' and section != 'others':
            lines.append('========== OTHERS ==========')
            lines.append('')
        section = group_section
        lines.append('=== %s ===' % header)
        lines.append('')
        if not new_maps:
            lines.append('(no new maps - all already reachable)')
            lines.append('')
        for req in new_maps:
            lines.append('To %s' % req)
            if extra_lines_for_map is not None:
                lines.extend(extra_lines_for_map(req, flag))
            lines.append('')
    return lines


def log_visit_order(gen_functions, logger=None):
    """
    Log every new map to visit, grouped by flag event, in progression order.

    Output is returned as a string and, if ``logger`` is provided, sent to it;
    otherwise it is printed.
    """
    output = '\n'.join(build_visit_order_lines(gen_functions))
    if logger is not None:
        logger.info(output)
    else:
        print(output)
    return output


def build_node(parent_node, map_nodes, map_warps, valid_warps, gen_functions):
    warps, connections = map_warps[parent_node.map]
    for warp in warps:
        for chain_break in gen_functions.info().map_chain_breaks:
            if chain_break in warp.dest_map:
                continue

        if warp.dest_map in map_nodes:
            parent_node.add_warps(warp, map_nodes[warp.dest_map])
            valid_warps.append(warp)
        else:
            if warp.dest_map not in map_warps:
                continue
            warp_node = structs.MapNode(warp.dest_map)
            map_nodes[warp.dest_map] = warp_node
            result = build_node(warp_node, map_nodes, map_warps, valid_warps, gen_functions)
            if not result:
                map_nodes.pop(warp.dest_map, None)
                continue
            parent_node.add_warps(warp, warp_node)
            valid_warps.append(warp)
    for connection in connections:
        if connection.map in map_nodes:
            parent_node.add_connection(map_nodes[connection.map])
        else:
            if connection.map not in map_warps:
                continue
            connection_node = structs.MapNode(connection.map)
            map_nodes[connection.map] = connection_node
            result = build_node(connection_node, map_nodes, map_warps, valid_warps, gen_functions)
            if not result:
                map_nodes.pop(connection.map, None)
                continue
            parent_node.add_connection(connection_node)
    if len(parent_node.connections) == 0 and len(parent_node.warp_nodes) == 0:
        return False
    return True


def build_map(map_warps: dict, gen_functions):
    map_nodes = dict()
    valid_warps = []
    starting_node = structs.MapNode(gen_functions.define_starting_map_id())
    map_nodes[gen_functions.define_starting_map_id()] = starting_node
    build_node(starting_node, map_nodes, map_warps, valid_warps, gen_functions)
    return starting_node, map_nodes, valid_warps


# Need to compile a list of every warp available
# Also build a list of warps to be ignored that we shouldn't randomize
def build_available_warps(randomized_map_warps, map_warps, all_maps, gen_functions):
    available_warps = []
    ignore_warps = []
    for map_name in map_warps:
        if map_name not in all_maps:
            # If the map is not in all_maps, we have determined this map is unreachable and we don't want to include
            # it in our randomzier, so we add do dont_randomize and skip the map
            #gen_functions.info().dont_randomize.append(map_name)
            continue
        skip = False
        for dont_randomize_map in gen_functions.info().dont_randomize:
            # Next we need to check if map is in don't randomize, since we allow things like "Map_Littleroot" and all
            # maps that begin with that would be auto added to dont randomize we need to go through entire don't
            # randomize instead of checking if map_name is in dont_randomize_map
            if dont_randomize_map in map_name:
                skip = True
                break
        if skip:
            continue

        randomized_warps, randomized_connections = randomized_map_warps[map_name]
        warps, connections = map_warps[map_name]
        to_ignore = map_name in gen_functions.info().not_needed
        index = -1
        for warp in warps:
            index = index + 1
            if 'gym' in map_name.lower() and warp.dest_map == map_name:
                # Warps inside gym dont get randomized, we consider these warps to be ignored
                continue

            if map_name in gen_functions.info().dont_randomize_warp \
                    and warp.warp_id in gen_functions.info().dont_randomize_warp[map_name]:
                # we also want to skip any warps that are in the don't randomize_warp
                # eventually we will actually give dont randomize warps filler warps from don't randomize but that
                # happens at the very end of randomizer
                continue

            skip = False
            for dont_randomize_map in gen_functions.info().dont_randomize:
                if dont_randomize_map in warp.dest_map:
                    # We need to check to make sure that destination map is also allowed to be randomized
                    skip = True
                    break
            if skip:
                continue

            if not to_ignore:
                # This warp is a valid warp that we must randomize
                available_warps.append([map_name, randomized_warps[index]])
            else:
                # If map is in not needed its allowed to be ignored
                ignore_warps.append([map_name, randomized_warps[index]])
    return available_warps, ignore_warps


def compute_pairs_for_map(game_map, warps, gen_functions):
    # Detects groups of physically adjacent warps on a single map (two warp tiles
    # next to each other that the game treats as a single door). Returns a list of
    # groups, where each group is a list of warp_ids. This is the same grouping the
    # randomizer applies, so a paired door can be treated as one logical warp.
    paired_warps = dict()
    if len(warps) > 1:
        warp_coords = dict()
        for warp in warps:
            if 'gym' in game_map.lower() and (warp.dest_map == game_map or 'gym' in warp.dest_map.lower()):
                continue
            if warp.no_pair:
                continue
            for x in range(0, warp.width):
                for y in range(0, warp.height):
                    warp_x = warp.x + x
                    warp_y = warp.y + y
                    # need to check x + 1 and y + 1 to see if warps are next to each other
                    for offset in [-1, 0, 1]:
                        for coord_to_try in [(warp_x + offset, warp_y), (warp_x, warp_y + offset)]:
                            if coord_to_try in warp_coords and warp_coords[coord_to_try] != warp.warp_id:
                                # if this offset coord exists as a warp and is not our current warp,
                                # we know we have found a pair
                                if game_map in paired_warps:
                                    found_pair = False
                                    for pair in paired_warps[game_map]:
                                        if warp_coords[coord_to_try] in pair and warp.warp_id not in pair:
                                            pair.append(warp.warp_id)
                                            found_pair = True
                                            break
                                    if not found_pair:
                                        paired_warps[game_map].append([warp_coords[coord_to_try], warp.warp_id])
                                else:
                                    paired_warps[game_map] = [[warp_coords[coord_to_try], warp.warp_id]]
                    warp_coords[(warp_x, warp_y)] = warp.warp_id  # finally add warp to warp coords for look up

        # Honor manually-defined pairs (custom "treat these warps as one door" flagging).
        # This lets non-adjacent warps on the same map be grouped just like physically
        # adjacent ones. Every gen's info module defines a `forced_warp_pairs` dict of the
        # form { map_name: [ [warp_id, warp_id, ...], ... ] }. These groups are injected
        # here so the consolidation step below merges any overlaps with adjacency pairs.
        forced_pairs = gen_functions.info().forced_warp_pairs
        for forced_group in forced_pairs.get(game_map, []):
            forced_group = [warp_id for warp_id in forced_group]
            if len(forced_group) > 1:
                paired_warps.setdefault(game_map, []).append(forced_group)

        # It is possible that duplicate pairs exist so we must consolidate pairs into a single warp pair
        while True:
            completed = True
            if game_map not in paired_warps:
                break  # No need to do anything if map has no pairs
            for i in range(0, len(paired_warps[game_map])):
                paired_ids = paired_warps[game_map][i]
                merge = None
                for warp_id in paired_ids:
                    j = 0
                    for pair_to_check in paired_warps[game_map]:
                        # check if any warp_id in current pairing exists in any other pair
                        if i != j and warp_id in pair_to_check:
                            merge = pair_to_check  # warp exists in another pair therefore we must merge pairs
                            break
                        j = j + 1
                    if merge is not None:
                        break
                if merge is not None:
                    for warp_id in merge:  # add all warps from merge into paired warps then remove merge from pairs
                        if warp_id not in paired_warps[game_map][i]:
                            paired_warps[game_map][i].append(warp_id)
                    paired_warps[game_map].remove(merge)
                    completed = False  # to adjust for size change in len(paired_warps[game_map]), we break out
                    break  # of for loop and loop on the while loop
            if completed:
                break  # if we get through the entire for loop without handling any merges, we are good to move on

    return paired_warps.get(game_map, [])


# We will condense all pairs into a single warp in available and ignore warps
# This will keep things simpler and only deal with fixing pairs at the end
# That way during the actual randomization we never have to worry about dealing with pair logic
def remove_pair_warps(available_warps, ignore_warps, randomized_map_warps, map_warps, all_maps, gen_functions):
    paired_warps = dict()
    for game_map in all_maps:
        if 'Map_Castelia_City_h28' in game_map:
            debug = -2
        # We will iterate through all maps to find any pairs that exist
        warps, connections = map_warps[game_map]
        groups = compute_pairs_for_map(game_map, warps, gen_functions)
        if groups:
            paired_warps[game_map] = groups

        # Ok finally we need to remove all except for first warp id of all pairs from available and ignore warps
        # this helps to ensure that we dont have to deal with any paired warps while randomizing
        if game_map not in paired_warps:
            continue  # No need to do anything if map has no pairs
        warps, connections = randomized_map_warps[game_map]
        for paired_ids in paired_warps[game_map]:
            # This is an important check, if a paired_warp is in map_to_map_warp_accessibility
            # we need to make sure the warp used in map_to_map_warp_accessibility isnt being erased
            # as such we update that entry to make sure it is using the warp in the pair that will still exist
            if game_map in gen_functions.info().map_to_map_warp_accessibility:
                for key_map in gen_functions.info().map_to_map_warp_accessibility[game_map]:
                    warp_tuple = gen_functions.info().map_to_map_warp_accessibility[game_map][key_map]
                    if warp_tuple.warp_id in paired_ids:
                        gen_functions.info().map_to_map_warp_accessibility[game_map][key_map] = \
                            gen_functions.info().WT(paired_ids[0], warp_tuple.flag)

            # Now we can remove all pairs except the first warp in paired_ids from available pool
            for warp_id in paired_ids[1:]:
                if [game_map, warps[warp_id]] in available_warps:
                    available_warps.remove([game_map, warps[warp_id]])
                elif [game_map, warps[warp_id]] in ignore_warps:
                    ignore_warps.remove([game_map, warps[warp_id]])
    return paired_warps


# After all randomization has occurred we need to go through and make sure all pairs are now matching and repaired
def restore_paired_warps(final_map_warps, paired_warps):
    for game_map in paired_warps:
        warps, connections = final_map_warps[game_map]
        for paired_ids in paired_warps[game_map]:
            # We know that the first warp in paired_ids should be the warp that was randomized
            # we need to make sure all other warps for the pair then match
            randomized_warp = paired_ids[0]
            for warp_id in paired_ids[1:]:
                warps[warp_id].dest_map = warps[randomized_warp].dest_map
                warps[warp_id].dest_warp_id = warps[randomized_warp].dest_warp_id


# Split map/warp pairs into an end node or a connecting node
def map_warp_divide(all_maps, map_warps, gen_functions, available_warps):
    end = []
    connects = []
    for game_map in all_maps:
        if game_map in gen_functions.info().not_needed:
            continue  # It is already assumed all not needed are end maps that can only be used at end of randomization

        # In order to get an accurate number of warps per map we can use available_warps since it is already adjusted
        # by removing all paired warps
        warp_count = 0
        for warp in available_warps:
            if warp[0] == game_map:
                warp_count = warp_count + 1
        warps, connections = map_warps[game_map]
        if warp_count > 1 and 'gym' not in game_map.lower():
            # We now this map has multiple real warps that potentially connect so we must check
            for warp in warps:
                if game_map not in gen_functions.info().map_warp_accessibility:
                    # if the map isnt specified in map warp accessibility we know that every warp connects
                    connects.append([game_map, warp.warp_id])
                elif warp.warp_id not in gen_functions.info().map_warp_accessibility[game_map] or \
                        (game_map in gen_functions.info().dont_randomize_warp and
                         warp.warp_id in gen_functions.info().dont_randomize_warp[game_map]):
                    # The warp was intended to not be randomized thus we should not add it to any list that we should
                    # consider
                    continue
                else:
                    if len(gen_functions.info().map_warp_accessibility[game_map][warp.warp_id]) != 0:
                        # Warp connects to additional warps
                        connects.append([game_map, warp.warp_id])
                    else:
                        # This warp connects with no other warps thus is considered an end point
                        end.append([game_map, warp.warp_id])
        else:
            if len(connections) > 0:
                # If there is only one warp or less, as long as there is a connection we can assume the map can continue
                connects.append([game_map, -1])
            elif warp_count == 1:
                # if there is only 1 warp and no connections, we know for certainty the map is a dead end
                end.append([game_map, -1])
            else:
                # len(connections) == 0 and warp_count == 0, therefore there are no valid warps on this map and it is
                # not considered reachable
                continue
    return end, connects


def get_all_accessible_warps_from_warp(game_map, warp_id, accessible_maps, gen_functions, randomized_map_warps,
                                       available_warps, orig_map_warps, include_starting_warp):
    accessible_warps = []
    dont_randomize_warps = []
    warps, connections = randomized_map_warps[game_map]
    for warp in warps:
        check_warps, check_connections = randomized_map_warps[game_map]
        if warp.warp_id == warp_id:
            if include_starting_warp:
                # This for scenario when coming from connection and we want to include it in our don't randomize
                # and accessible warp list, so we must check its a don't randomize warp
                if [game_map, warps[warp.warp_id]] not in available_warps:
                    if check_warps[warp.warp_id].dest_map == '':
                        # We know warp was not intended to be randomized so lets move on from rom this warp
                        dont_randomize_warps.append(warp.warp_id)
                        continue
                accessible_warps.append(warp.warp_id)
            continue  # skip incoming warp
        if [game_map, warps[warp.warp_id]] not in available_warps:
            # There are two scenarios where this could occur, firstly the warp was intentionally removed to not be
            # available or the warp as already been randomized, the only way to check is to see if the warp has been
            # randomized

            if check_warps[warp.warp_id].dest_map == '':
                # We know warp was not intended to be randomized so lets move on from rom this warp
                dont_randomize_warps.append(warp.warp_id)
                continue

        if game_map in gen_functions.info().map_warp_accessibility:
            # we must now check if incoming warp can reach this current warp following the rules specified
            if warp.warp_id not in gen_functions.info().map_warp_accessibility[game_map] or \
                    (game_map in gen_functions.info().dont_randomize_warp and
                     warp.warp_id in gen_functions.info().dont_randomize_warp[game_map]):
                # this is a don't randomize warp, so lets just ignore this warp
                continue
            if not gen_functions.info().is_warp_to_warp_valid(game_map, accessible_maps, warp_id, warp.warp_id):
                continue  # We know that we cannot currently go from incoming warp to this warp

        # If we have made it passed all these checks we know that the warp is accessible from our current warp
        accessible_warps.append(warp.warp_id)
    return accessible_warps, dont_randomize_warps


def add_to_accessible_maps(accessible_maps, current_map, previous_map, incoming_warp_id):
    if current_map in accessible_maps:
        if (incoming_warp_id != -1 and incoming_warp_id not in accessible_maps[current_map]) or \
                (incoming_warp_id == -1 and previous_map not in accessible_maps[current_map]):
            if incoming_warp_id != -1:
                accessible_maps[current_map].append(incoming_warp_id)
            else:
                accessible_maps[current_map].append(previous_map)
    else:
        if incoming_warp_id != -1:
            accessible_maps[current_map] = [incoming_warp_id]  # came from warp
        else:
            accessible_maps[current_map] = [previous_map]  # came from connection


# Accessible_maps allows us to keep track of everything across multiple loops
# Visited Maps is intended to reset after each run through
def build_warps_to_randomize(accessible_maps, visited_maps, warps_to_randomize, randomized_map_warps, available_warps,
                             current_map, previous_map, incoming_warp_id, gen_functions, orig_map_warps):
    if current_map == 'Map_Galactic_HQ_Floor02_00':
        help = 0
    if current_map not in randomized_map_warps:
        return

    warps, connections = randomized_map_warps[current_map]
    starting_warp = 0
    include_starting_warp = incoming_warp_id == -1

    # Ok lets determine if we have already checked this exact map/warp id combination or this exact connection path
    if current_map in visited_maps:
        if (incoming_warp_id != -1 and incoming_warp_id in visited_maps[current_map]) or \
                (incoming_warp_id == -1 and previous_map in visited_maps[current_map]):
            # In this pass we have already checked this path, breaks any potential loops
            return
        else:
            if incoming_warp_id != -1:
                visited_maps[current_map].append(incoming_warp_id)  # came from warp
            else:
                visited_maps[current_map].append(previous_map)  # came from connection
    else:
        if incoming_warp_id != -1:
            visited_maps[current_map] = [incoming_warp_id]  # came from warp
        else:
            visited_maps[current_map] = [previous_map]  # came from connection

    # Similarly lets update accessible_maps
    add_to_accessible_maps(accessible_maps, current_map, previous_map, incoming_warp_id)

    if incoming_warp_id != -1:
        starting_warp = incoming_warp_id  # since we entered map from warp, our starting warp will be incoming warp

        # Next we need to check if we are entering from a cont go back warp
        # Basically if we hit a 1-way warp we want to consider this warp as a dead end, this ensures that any other
        # warps that potentially connect to this one way are not dead ends but rather maps that connect to the main
        # loop
        if current_map in gen_functions.info().potential_softlock_warps and \
                incoming_warp_id in gen_functions.info().potential_softlock_warps[current_map]:
            starting_warp = -3  # Lets us know that we should not add any warps to randomize for this map
    else:
        # Since we are coming from a connection we need to handle setting our starting warp a bit differently
        # We need to check if we can add any warps from current_map
        if len(warps) == 0:
            starting_warp = -2  # there are no warps to check
        if current_map in gen_functions.info().map_to_map_warp_accessibility and \
                previous_map in gen_functions.info().map_to_map_warp_accessibility[current_map]:
            # map_to_map_warp_accessibility defines special scenarios for what warps to use when going from previous
            # map to current map, if it is specified then we use that warp to start
            wt_to_check = gen_functions.info().map_to_map_warp_accessibility[current_map][previous_map]
            if gen_functions.info().is_warp_ready(wt_to_check, accessible_maps):
                starting_warp = wt_to_check.warp_id
            else:
                starting_warp = -2  # Not currently able to traverse to any warp from this connection

    if starting_warp != -2:  # we need to check warps
        # Lets get a list of every warp that connects to our current warp that we can reach and isn't intended to not
        # be randomized
        accessible_warps, dont_randomize_warps = get_all_accessible_warps_from_warp(current_map, starting_warp,
                                                                                    accessible_maps, gen_functions,
                                                                                    randomized_map_warps,
                                                                                    available_warps, orig_map_warps,
                                                                                    include_starting_warp)

        for dont_randomize_warp in dont_randomize_warps:
            # Even though we dont want to randomize these warps we need to check if this warp belongs to dont_randomize
            # list, and if it does we should fill in the correct dont randomize info just in case and follow path
            # as these maps may lead to new areas or even be required as an event flag
            orig_warps, orig_connections = orig_map_warps[current_map]
            for dont_randomize_map in gen_functions.info().dont_randomize:
                if dont_randomize_map in orig_warps[dont_randomize_warp].dest_map or dont_randomize_map in current_map:
                    # we know this warp belongs to don't randomize
                    warps[dont_randomize_warp].dest_map = orig_warps[dont_randomize_warp].dest_map
                    warps[dont_randomize_warp].dest_warp_id = orig_warps[dont_randomize_warp].dest_warp_id
                    add_to_accessible_maps(accessible_maps, current_map, previous_map, dont_randomize_warp)
                    build_warps_to_randomize(accessible_maps, visited_maps, warps_to_randomize, randomized_map_warps,
                                             available_warps, warps[dont_randomize_warp].dest_map, current_map,
                                             warps[dont_randomize_warp].dest_warp_id, gen_functions, orig_map_warps)
                    break

        if starting_warp != -3:  # starting_warp = -3 in can't go back scenario, we dont want to add any warps
            for accessible_warp in accessible_warps:
                # If the warp has not been randomized yet we need to make sure the warp is included in the
                # warps_to_randomize list, otherwise if it already has been randomized we need to follow that warp to
                # the next map and repeat the process on that map
                if warps[accessible_warp].dest_map == '':
                    # warp has yet to be set, lets check if we need to add to warps_to_randomize
                    to_add = [current_map, warps[accessible_warp]]
                    if to_add not in warps_to_randomize:
                        warps_to_randomize.append(to_add)
                else:
                    # warp has already been randomized, progress
                    add_to_accessible_maps(accessible_maps, current_map, previous_map, accessible_warp)
                    build_warps_to_randomize(accessible_maps, visited_maps, warps_to_randomize, randomized_map_warps,
                                             available_warps, warps[accessible_warp].dest_map, current_map,
                                             warps[accessible_warp].dest_warp_id, gen_functions, orig_map_warps)

    # Ok finally we need to progress through all progess-able connections attached to map
    if not gen_functions.info().is_map_progressable(current_map, accessible_maps,  -1, True):
        # First we check if the map is considered progress-able i.e. if a map requires a flag/hm to get through
        return  # Map is not progress-able so don't assume we can go through connections
    for connection in connections:
        # connections are much easier :D
        # First check if connection is navigable, if not navigable, cannot make connection
        is_valid_connection = True
        for non_navigable_connection in gen_functions.info().non_navigable_connections:
            if current_map == non_navigable_connection[0]:
                if connection.map in non_navigable_connection:
                    is_valid_connection = False
                    break

        if not is_valid_connection:
            continue  # the connection is considered non-navigable therefore skip connection

        # Check specific connection to connection rules to see if we can progress through to next connection
        if current_map in gen_functions.info().connection_to_connection_rules:
            if connection.map in gen_functions.info().connection_to_connection_rules[current_map]:
                flag = gen_functions.info().connection_to_connection_rules[current_map][connection.map]
                bits = bin(flag)  # Convert flag into bits representation
                connetion_pass = True
                index = 0
                for bit in reversed(bits):
                    if bit == '1':
                        if not gen_functions.info().check_progession_blockers(index, accessible_maps):
                            connetion_pass = False  # One of the requirements is missing for flag
                            break
                    index = index + 1
                if not connetion_pass:
                    continue

        # Honor seamless border-warp routing when LEAVING current_map.
        # map_to_map_warp_accessibility not only says which warp we land on when
        # entering a map, it also names the single border warp we must be standing
        # at to cross a seamless connection out of it. Previously this loop only
        # enforced the entering side, so the fill could walk out of a map through a
        # governed border from a warp/zone that cannot actually reach that border
        # (e.g. crossing Map_Pokemon_League_01 -> Map_Pokemon_League_00 from the
        # zone-A courtyard even though that crossing requires zone-B warp 2). That
        # over-approximated reachability and let required warps (Flash) be stranded
        # on an isolated island. Only cross when the border warp is actually
        # reachable from where we entered - mirroring the tracker's reachable_room_warps.
        if current_map in gen_functions.info().map_to_map_warp_accessibility and \
                connection.map in gen_functions.info().map_to_map_warp_accessibility[current_map]:
            border_wt = gen_functions.info().map_to_map_warp_accessibility[current_map][connection.map]
            if not gen_functions.info().is_warp_ready(border_wt, accessible_maps):
                continue  # the border crossing is gated behind an unmet flag/HM
            if starting_warp != border_wt.warp_id:
                if starting_warp < 0:
                    continue  # no concrete entry warp (one-way drop / no warps) -> can't route to the border
                if not gen_functions.info().is_warp_to_warp_valid(current_map, accessible_maps,
                                                                  starting_warp, border_wt.warp_id):
                    continue  # cannot walk to the required border warp from where we entered

        # Connection is safe to progress though so lets move on to next map
        build_warps_to_randomize(accessible_maps, visited_maps, warps_to_randomize, randomized_map_warps,
                                 available_warps, connection.map, current_map, -1, gen_functions, orig_map_warps)
    return


def randomizer_flag_event_rules(end, connecting_warps, accessible_maps, warps_to_randomize, gen_functions, rng):
    chance = rng.randrange(0, 101)
    # Find the current forced order flag we are on
    current_forced = 0
    for flag in gen_functions.info().FORCED_FLAG_ORDER:
        if not gen_functions.info().search_for_needed_maps(gen_functions.info().FLAG_EVENT_LIST[flag], accessible_maps):
            current_forced = flag
            break

    # We can now select a map with the following rules
    # If map/warp goes towards current forced flag
    # if map/warp goes towards a non-forced flag
    # if map/warp goes towards a currently non accessible connecting warp
    requirement_list = []
    for req in gen_functions.info().FLAG_EVENT_LIST[current_forced]:
        if req not in requirement_list:
            requirement_list.append(req)  # get all required maps for current flag in forced order
    for i in range(0, gen_functions.info().END_FLAG + 1):
        if i not in gen_functions.info().FORCED_FLAG_ORDER:
            for req in gen_functions.info().FLAG_EVENT_LIST[i]:
                if req not in requirement_list:
                    requirement_list.append(req)  # add non order forced flags into requirement list

    # Satisfies first two checks
    for req in requirement_list:
        map_name = req
        warp_parts = []
        if ':' in req:
            map_name = req.split(':')[0]
            warp_parts = req.split(':')
        if end[0] == map_name:
            if len(warp_parts) == 0 and map_name not in accessible_maps:
                return True
            else:
                if str(end[1].warp_id) in warp_parts:
                    return True

    # Satisfies third check
    if chance > 30 or end in warps_to_randomize:
        return False  # if the warp is in the to randomize list then we know we can already reach warp

    if end[0] not in accessible_maps or end[1].warp_id not in accessible_maps[end[0]]:
        if gen_functions.info().is_map_progressable(end[0], accessible_maps, end[1].warp_id):
            if [end[0], end[1].warp_id] in connecting_warps:
                return True  # Verify this warp is a connecting warp and that it is progress-able

    return False


def select_random_warp(warps_to_randomize, available_warps, ignore_warps, randomized_map_warps, accessible_maps,
                       connecting_warps, ending_warps, gen_functions, rng):
    # first select a warp that is in current map world
    start = rng.choice(warps_to_randomize)

    if len(ignore_warps) == 0:
        return False

    # then we must choose a warp from available, if no warps left in available select from ignore list
    if len(available_warps) <= 1:
        while True:
            end = rng.choice(ignore_warps)
            if gen_functions.is_not_needed_map_ok(end[0]):
                break
    else:
        # need to find a suitable random selection

        connect_maps = []
        for connect in connecting_warps:
            if connect[0] not in connect_maps:
                connect_maps.append(connect[0])

        end_maps = []
        for end in ending_warps:
            if end[0] not in end_maps:
                end_maps.append(end[0])

        # First Thing We Want To Get At Least 1 Warp/Connection to every map that has leads to another connection/warp
        # This will give the map a wide spread
        has_all_connects = True
        for connect_map in connecting_warps:
            if connect_map[1] == -1:
                # there are no warps to this map so we can't assume that we will be able to reach it immediately
                continue
            if connect_map[0] not in accessible_maps:
                # if map is not in accessible_maps it means we do not yet currently have a path to this map
                # However if every warp in this map is not progress-able then there is no reason to be visiting this
                # map yet and are ok with not having a warp to this map yet
                map_has_warp = False
                for warp in available_warps:
                    if warp[0] == connect_map[0]:
                        map_has_warp = True  # First we need to verify that this warp is actually available
                        break
                if map_has_warp:
                    if gen_functions.info().is_map_progressable(connect_map[0], accessible_maps, connect_map[1]):
                        has_all_connects = False  # Map is considered progress-able so we should have a warp to this map
                        break

        # A check if there are any flags yet to be satisfied
        has_all_flags_met = True
        for i in range(0, gen_functions.info().END_FLAG + 1):
            if not gen_functions.info().search_for_needed_maps(gen_functions.info().FLAG_EVENT_LIST[i],
                                                               accessible_maps):
                has_all_flags_met = False
                break

        # A way to check if we have used all dead end points we want to include
        used_all_ends = True
        for end_map in ending_warps:
            if end_map[0] not in gen_functions.info().not_needed:
                if end_map[0] in accessible_maps:
                    # Maps can potentially have multiple warps, but if a warp doesn't connect to any other warp
                    # we still need to consider that as an end point, in this scenario we need to check if we actually
                    # have the end point warp included or not
                    has_warp = False
                    for accessible_warp in accessible_maps[end_map[0]]:
                        if end_map[1] == accessible_warp or end_map[1] == -1:
                            # if the warp exists in accessible_maps for the given map or the given map has only 1 warp
                            # we can consider the map already visited
                            has_warp = True
                            break
                    if not has_warp:
                        # Finally we need to check if this warp is even in the available_warps to choose from
                        map_has_warp = False
                        for warp in available_warps:
                            if warp[0] == end_map[0]:
                                map_has_warp = True
                                break
                        if map_has_warp:
                            # Warp is valid and has not been selected therefore we are missing an end point
                            used_all_ends = False
                            break
                if end_map[0] not in accessible_maps:
                    used_all_ends = False  # end map is not reachable currently
                    break

        # Basically just only allow us to select warps that aren't in the accessible warps yet
        used_all_no_dead_ends = True
        for warp in available_warps:
            if warp not in warps_to_randomize:
                used_all_no_dead_ends = False

        count = 0
        while True:
            # Ok select end point until we hit whatever condition we are on
            if count >= 100000:
                # safety if we ever loop that many times, chances are we are stuck stuck
                return False
            count = count + 1
            end = rng.choice(available_warps)
            if end == start:
                continue
            if end[0] == start[0]:
                continue  # no warp can lead back to same map

            if not has_all_connects:
                # Ensures we have never encountered this map before and that there is at least one progress-able
                # path
                pair = [end[0], end[1].warp_id]
                if end[0] in accessible_maps or not gen_functions.info().is_map_progressable(end[0], accessible_maps,
                                                                                             end[1].warp_id):
                    continue
                elif end[0] not in connect_maps:
                    continue
                elif end[0] in connect_maps and pair not in connecting_warps:
                    continue
                break  # selected warps are good
            elif not has_all_flags_met:
                # We now have a responsibility to make sure we include every flagged map
                if not randomizer_flag_event_rules(end, connecting_warps, accessible_maps, warps_to_randomize,
                                                   gen_functions, rng):
                    continue
                break
            elif not used_all_ends:
                if end[0] not in end_maps:
                    continue
                break
            elif not used_all_no_dead_ends:
                if end in warps_to_randomize:
                    continue
                break
            else:
                break

    # Now we need to update warp in randomized map warps
    start_warps, start_connections = randomized_map_warps[start[0]]
    end_warps, end_connections = randomized_map_warps[end[0]]

    start_warps[start[1].warp_id].dest_map = end[0]
    start_warps[start[1].warp_id].dest_warp_id = end[1].warp_id
    end_warps[end[1].warp_id].dest_map = start[0]
    end_warps[end[1].warp_id].dest_warp_id = start[1].warp_id

    # Finally we need to remove start/end
    if end in available_warps:
        available_warps.remove(end)
    if end in ignore_warps:
        ignore_warps.remove(end)
    if start in available_warps:
        available_warps.remove(start)
    if start in ignore_warps:
        ignore_warps.remove(start)
    if start in warps_to_randomize:
        warps_to_randomize.remove(start)
    if end in warps_to_randomize:
        warps_to_randomize.remove(end)
    return True


# Pretty much entirely used for debugging, just a copy of checks used in selecting random warps
def crisis_randomize_debug(accessible_maps, connecting_warps, available_warps, warps_to_randomize,
                           ending_warps, gen_functions):
    for connect_map in connecting_warps:
        if connect_map[1] == -1:
            continue
        if connect_map[0] not in accessible_maps:
            map_has_warp = False
            for warp in available_warps:
                if warp[0] == connect_map[0]:
                    map_has_warp = True
                    break  # DO NOT PUT A BREAK POINT HERE FOR DEBUG
            if map_has_warp:
                if gen_functions.info().is_map_progressable(connect_map[0], accessible_maps, connect_map[1]):
                    break  # PLACE BREAKPOINT HERE FOR DEBUG

    for i in range(0, gen_functions.info().END_FLAG + 1):
        if not gen_functions.info().search_for_needed_maps(gen_functions.info().FLAG_EVENT_LIST[i], accessible_maps):
            break  # PLACE BREAKPOINT HERE FOR DEBUG

    for end_map in ending_warps:
        if end_map[0] not in gen_functions.info().not_needed:
            if end_map[0] in accessible_maps:
                has_warp = False
                for accessible_warp in accessible_maps[end_map[0]]:
                    if end_map[1] == accessible_warp or end_map[1] == -1:
                        has_warp = True
                        break  # DO NOT PUT A BREAK POINT HERE FOR DEBUG
                if not has_warp:
                    map_has_warp = False
                    for warp in available_warps:
                        if warp[0] == end_map[0]:
                            map_has_warp = True
                            break
                    if map_has_warp:
                        break  # PLACE BREAKPOINT HERE FOR DEBUG
            if end_map[0] not in accessible_maps:
                break  # PLACE BREAKPOINT HERE FOR DEBUG

    # used_all_no_dead_ends = True
    for warp in available_warps:
        if warp not in warps_to_randomize:
            # used_all_no_dead_ends = False
            break  # PLACE BREAKPOINT HERE FOR DEBUG


# Don't randomize warps are warps that are impossible or near impossible to reach, therefore we give these warps
# warps from the not needed to ensure if a player ever does reach one of these warps, the warp still appears randomized
def select_random_for_dont_randomize_warp(randomized_map_warps, rng, gen_functions, ignore_warps):
    for map_name in gen_functions.info().dont_randomize_warp:
        warp_ids = gen_functions.info().dont_randomize_warp[map_name]
        for warp_id in warp_ids:
            if map_name in randomized_map_warps:
                start_warps, start_connections = randomized_map_warps[map_name]
                if warp_id >= len(start_warps):
                    continue
                if start_warps[warp_id].dest_map != '':
                    print("Issue with don't randomize warp")  # PLACE BREAKPOINT HERE FOR DEBUG
                    continue
                # Find a random warp from not needed
                while True:
                    if map_name == 'Map_Nimbasa_City' and warp_id == 7:
                        end = []
                        end.append('Map_Gear_Station_Interior_h66')
                        end.append(structs.Warp(422, 458, 32, 'Map_Gear_Station_Interior_h66', 7, 8, 62, 66, 1, 1, False)) #idk I inverted 7 and 8 and it worked
                        break
                    else:
                        end = rng.choice(ignore_warps)
                    if gen_functions.is_not_needed_map_ok(end[0]):
                        break

                # Now we need to update warp in randomized map warps
                end_warps, end_connections = randomized_map_warps[end[0]]

                start_warps[warp_id].dest_map = end[0]
                start_warps[warp_id].dest_warp_id = end[1].warp_id
                end_warps[end[1].warp_id].dest_map = map_name
                end_warps[end[1].warp_id].dest_warp_id = warp_id

                # Finally we need to remove end
                if end in ignore_warps:
                    ignore_warps.remove(end)


def randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps):
    available_warps, ignore_warps = build_available_warps(randomized_map_warps, map_warps, all_maps, gen_functions)
    pairs = remove_pair_warps(available_warps, ignore_warps, randomized_map_warps, map_warps, all_maps, gen_functions)
    ends, connects = map_warp_divide(all_maps, map_warps, gen_functions, available_warps)

    # print('ENDS:')
    # for entry in ends:
    #     print(entry[0])
    # print('----------')

    # Build out data structures for us to keep track of maps we can currently reach and warps available for us to
    # randomize currently
    accessible_maps = dict()
    warps_to_randomize = []
    visited = dict()
    visited.clear()
    build_warps_to_randomize(accessible_maps, visited, warps_to_randomize, randomized_map_warps,
                             available_warps, gen_functions.define_starting_map_id(), '', -1, gen_functions, map_warps)

    while True:
        # Exit conditions for randomization
        if len(warps_to_randomize) == 0 and len(available_warps) != 0:
            # reached incomplete map lets do one more pass through build_warps_to_randomize and if still stuck
            # seed is invalid
            visited.clear()
            build_warps_to_randomize(accessible_maps, visited, warps_to_randomize, randomized_map_warps,
                                     available_warps, gen_functions.define_starting_map_id(), '', -1, gen_functions,
                                     map_warps)
            if len(warps_to_randomize) == 0:
                # seed is bad, give us a debug function call and then exit randomizer process
                crisis_randomize_debug(accessible_maps, connects, available_warps, warps_to_randomize, ends,
                                       gen_functions)
                return False

        elif len(warps_to_randomize) == 0 and len(available_warps) == 0:
            break  # Seed completed

        # First we do a random pick/insertion
        if not select_random_warp(warps_to_randomize, available_warps, ignore_warps, randomized_map_warps,
                                  accessible_maps, connects, ends, gen_functions, rng):
            # unable to find a valid selection for randomization, we will do one more pass through, if still failing,
            # seed is invalid
            visited.clear()
            build_warps_to_randomize(accessible_maps, visited, warps_to_randomize, randomized_map_warps,
                                     available_warps, gen_functions.define_starting_map_id(), '', -1, gen_functions,
                                     map_warps)
            if not select_random_warp(warps_to_randomize, available_warps, ignore_warps, randomized_map_warps,
                                      accessible_maps, connects, ends, gen_functions, rng):
                crisis_randomize_debug(accessible_maps, connects, available_warps, warps_to_randomize, ends,
                                       gen_functions)
                return False
        # Then we build all nodes again
        visited.clear()
        build_warps_to_randomize(accessible_maps, visited, warps_to_randomize, randomized_map_warps,
                                 available_warps, gen_functions.define_starting_map_id(), '', -1, gen_functions,
                                 map_warps)

    select_random_for_dont_randomize_warp(randomized_map_warps, rng, gen_functions, ignore_warps)
    restore_paired_warps(randomized_map_warps, pairs)
    return True


def parse_sekii_id(warp):
    # A sekii_id identifies a tracked location and comes in two forms:
    #   "<map>:<value>" -> a "warp" (has a map component)
    #   ":<value>"      -> a "mark" (no map component, e.g. a badge/event)
    # Returns a (map, value, is_mark) tuple, or None when the warp has no
    # sekii_id (i.e. it isn't a tracked location).
    sekii_id = getattr(warp, 'sekii_id', None)
    if not sekii_id:
        return None
    map_part, _, value_part = sekii_id.partition(':')
    return map_part, value_part, map_part == ''


def build_room_warps(map_warps):
    # Group maps into "rooms" by joining all of their connections together.
    # Returns a mapping of each map name to the list of (map_name, warp) present in
    # that room. Rooms whose joined warp list has exactly two warps are jump rooms.
    parent = {}

    def find(node):
        parent.setdefault(node, node)
        root = node
        while parent[root] != root:
            root = parent[root]
        while parent[node] != root:
            parent[node], node = root, parent[node]
        return root

    def union(a, b):
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[root_b] = root_a

    for map_name in map_warps:
        find(map_name)
        for connection in map_warps[map_name][1]:
            if connection.map in map_warps:
                union(map_name, connection.map)

    room_warps = {}
    for map_name in map_warps:
        room = room_warps.setdefault(find(map_name), [])
        for warp in map_warps[map_name][0]:
            room.append((map_name, warp))

    return {map_name: room_warps[find(map_name)] for map_name in map_warps}


def build_warp_pairs(map_warps, gen_functions):
    # Returns map_name -> {warp_id: representative_warp_id}, grouping physically
    # adjacent warps (paired doors) so a whole door can be treated as one warp.
    # Warps that aren't paired are simply absent (they represent themselves).
    map_warp_pairs = {}
    for map_name in map_warps:
        rep = {}
        for group in compute_pairs_for_map(map_name, map_warps[map_name][0], gen_functions):
            representative = group[0]
            for warp_id in group:
                rep[warp_id] = representative
        map_warp_pairs[map_name] = rep
    return map_warp_pairs


def warp_door_key(map_warp_pairs, map_name, warp_id):
    # A "door" uniquely identifies a logical warp: a map plus the representative
    # warp_id of its pair group (or the warp_id itself if it isn't paired).
    return map_name, map_warp_pairs.get(map_name, {}).get(warp_id, warp_id)


def build_map_connections(map_warps, gen_functions):
    # map_name -> list of adjacent maps reachable by a *navigable* connection.
    #
    # Connections are directional here: a connection flagged non-navigable (in the
    # direction map_name -> connection.map) is impassable and excluded, mirroring
    # build_warps_to_randomize. Flag-gated connections (connection_to_connection_rules)
    # are treated as passable because the tracker models logical reachability
    # assuming full progression.
    non_navigable = gen_functions.info().non_navigable_connections
    map_connections = {}
    for map_name in map_warps:
        adjacent = []
        for connection in map_warps[map_name][1]:
            if connection.map not in map_warps:
                continue
            # Skip connections marked non-navigable from map_name's side
            blocked = False
            for pair in non_navigable:
                if map_name == pair[0] and connection.map in pair:
                    blocked = True
                    break
            if blocked:
                continue
            adjacent.append(connection.map)
        map_connections[map_name] = adjacent
    return map_connections


def reachable_room_warps(room_warps, entry_map, entry_warp_id, map_connections, gen_functions, cache=None,
                         strict_cross_map=True, flags_satisfied=None):
    # Return the list of (map, warp) that a player can actually reach after
    # arriving at (entry_map, entry_warp_id), staying within the given room.
    #
    # This honors both accessibility tables:
    #   * map_warp_accessibility: within a single map you can only walk between
    #     warps the game says are connected (an empty list means the warp is a
    #     one-way drop with no exit).
    #   * map_to_map_warp_accessibility: crossing a seamless connection between
    #     two maps is only possible at the specific border warp the table names.
    #     Crossing OUT of a listed map requires standing at (or reaching) that
    #     border warp; crossing IN drops you at the border warp on the other
    #     side rather than letting you roam the whole map freely. A map that
    #     enumerates its cross-map routing cannot use any connection it does not
    #     list. Connections between two maps that neither table mentions are
    #     treated as free movement.
    # The entry warp itself is excluded from the result.
    #
    # strict_cross_map controls how an *unlisted* connection out of a map that
    # does enumerate its cross-map routing is treated. With the default True the
    # connection is impassable (the tracker's per-arrival model). With False the
    # connection is treated as free movement instead; this is used by the
    # start-to-goal pathfinder, whose curated routing tables would otherwise
    # fragment free overworld travel while still honoring map_warp_accessibility.
    #
    # flags_satisfied gates the progression flags carried by the accessibility
    # rules. When None (the default) every flag is considered satisfied, i.e.
    # full progression -- this is what the tracker and the Cynthia trace use.
    # Otherwise it must be a list of 0/1 values (as produced for check_flags):
    # a rule whose flag is not satisfied is treated as impassable, allowing
    # callers to build tracker maps that only assume some events are done.
    # The cache key includes strict_cross_map and the flag mask so a caller that
    # reuses one cache across different settings never gets a stale result.
    cache_key = (entry_map, entry_warp_id, strict_cross_map,
                 None if flags_satisfied is None else tuple(flags_satisfied))
    if cache is not None and cache_key in cache:
        return cache[cache_key]

    accessibility = gen_functions.info().map_warp_accessibility
    map_to_map = gen_functions.info().map_to_map_warp_accessibility

    def flag_ok(flag):
        # A rule is traversable when its flag is satisfied. With flags_satisfied
        # None we assume full progression, so every flag passes.
        return flags_satisfied is None or check_flags(flag, flags_satisfied)

    def map_enterable(map_name):
        # A map with per-map flag requirements (map_flag_requirements, e.g. a
        # Surf-only water route) can't be walked through until those flags are
        # satisfied -- mirrors is_map_progressable's per-map HM gate.
        return map_flags_ok(gen_functions, map_name, flags_satisfied)

    warps_by_map = {}
    for room_map, room_warp in room_warps:
        warps_by_map.setdefault(room_map, {})[room_warp.warp_id] = room_warp

    def intra_map_targets(map_name, warp_id):
        # Warps in the same map reachable from warp_id, honoring flag gating.
        map_warps = warps_by_map.get(map_name, {})
        if map_name not in accessibility:
            return [wid for wid in map_warps if wid != warp_id]
        if warp_id not in accessibility[map_name]:
            return []  # warp isn't routed/randomized -> no internal connections
        return [wt.warp_id for wt in accessibility[map_name][warp_id]
                if wt.warp_id in map_warps and flag_ok(wt.flag)]

    def can_leave_map(map_name, warp_id):
        # Whether this warp can reach the map's connection edges (to walk out).
        # A warp with no (flag-satisfied) internal connections also can't reach a
        # connection.
        if map_name not in accessibility:
            return True
        if warp_id not in accessibility[map_name]:
            return False
        return any(flag_ok(wt.flag) for wt in accessibility[map_name][warp_id])

    def crossing(from_map, to_map):
        # Describe traversing the seamless connection from_map -> to_map.
        # Returns None when the crossing is not permitted, otherwise a
        # (source_req, dest_land) pair where:
        #   source_req -- the warp in from_map you must stand at to cross
        #                 (None means any warp able to reach the map edge);
        #   dest_land  -- the warp you arrive at in to_map (None means you
        #                 enter freely and may roam the whole map).
        # Progression flags on the rules are honored via flag_ok (which passes
        # everything under the default full-progression assumption).
        source_req = None
        dest_land = None
        governed = False
        if from_map in map_to_map and to_map in map_to_map[from_map]:
            governed = True
            outgoing = map_to_map[from_map][to_map]
            if not flag_ok(outgoing.flag):
                return None  # the route out exists but its flag is not satisfied
            source_req = outgoing.warp_id
        if to_map in map_to_map and from_map in map_to_map[to_map]:
            governed = True
            incoming = map_to_map[to_map][from_map]
            # The incoming border rule is the only way to enter to_map from
            # from_map; if its flag isn't satisfied the crossing is blocked.
            # (Leaving dest_land None here would wrongly look like a free
            # connection and let the player walk in without the flag, e.g. into
            # a Surf-gated route before Surf.)
            if not flag_ok(incoming.flag):
                return None
            dest_land = incoming.warp_id
        if not governed and from_map in map_to_map:
            # from_map enumerates its cross-map routing; an unlisted connection
            # is intentionally not traversable for the tracker, but the path
            # finder treats it as free movement instead.
            if strict_cross_map:
                return None
            return None, None
        return source_req, dest_land

    result_keys = set()
    result = []

    def add_result(map_name, warp_id):
        if (map_name, warp_id) == (entry_map, entry_warp_id):
            return
        if (map_name, warp_id) not in result_keys:
            result_keys.add((map_name, warp_id))
            result.append((map_name, warps_by_map[map_name][warp_id]))

    visited_warps = set()
    roamed_maps = set()          # maps entered via a free connection -> freely walkable
    warp_frontier = [(entry_map, entry_warp_id)]
    map_frontier = []

    def try_crossings(map_name, source_req_ok, from_warp_id):
        # Enqueue every connection leaving map_name that is currently traversable.
        # source_req_ok(req) decides whether the required border warp is reached.
        for adjacent in map_connections.get(map_name, ()):
            cross = crossing(map_name, adjacent)
            if cross is None:
                continue  # blocked by cross-map routing rules
            source_req, dest_land = cross
            if source_req is None:
                if from_warp_id is not None and not can_leave_map(map_name, from_warp_id):
                    continue  # a one-way drop cannot reach the map edge
            elif not source_req_ok(source_req):
                continue  # not standing at the required border warp
            if dest_land is None:
                # Free connection: roam into the adjacent map. Warp-less maps (pure
                # connective overworld tiles) are still roamed so their onward
                # connections can be followed.
                if adjacent not in roamed_maps:
                    map_frontier.append(adjacent)
            else:
                if dest_land in warps_by_map.get(adjacent, {}) and map_enterable(adjacent):
                    add_result(adjacent, dest_land)
                    warp_frontier.append((adjacent, dest_land))

    while warp_frontier or map_frontier:
        if map_frontier:
            map_name = map_frontier.pop()
            if map_name in roamed_maps:
                continue
            roamed_maps.add(map_name)
            if not map_enterable(map_name):
                continue  # can't walk this map without its required flag/HM
            # Entering a map from a free connection lets you roam its overworld,
            # but warps sitting behind an unsatisfied intra-map flag gate (e.g. a
            # Waterfall-only ledge in Sunyshore City) are NOT part of that free
            # region -- reaching them still requires crossing the gated edge. So
            # instead of blanket-adding every warp, keep only the warps that stay
            # reachable through flag-satisfied intra-map edges. A warp that is
            # never an intra-map target is a one-way drop / border arrival and
            # remains standable; a targeted warp survives only while some warp
            # still in the set has a flag-ok edge to it (iterated to a fixpoint so
            # a warp reachable only via a pruned warp is pruned too).
            reachable_ids = set(warps_by_map.get(map_name, {}))
            map_rules = accessibility.get(map_name)
            if map_rules:
                targeted = {wt.warp_id for wts in map_rules.values() for wt in wts}
                changed = True
                while changed:
                    changed = False
                    for w in list(reachable_ids):
                        if w not in targeted:
                            continue  # drop / border-arrival warp: always standable
                        if not any(wt.warp_id == w and flag_ok(wt.flag)
                                   for src in reachable_ids
                                   for wt in map_rules.get(src, [])):
                            reachable_ids.discard(w)
                            changed = True
            for warp_id in reachable_ids:
                add_result(map_name, warp_id)
            # From a roamed map every border warp is reachable.
            try_crossings(map_name, lambda req: True, None)
            continue

        map_name, warp_id = warp_frontier.pop()
        if (map_name, warp_id) in visited_warps:
            continue
        visited_warps.add((map_name, warp_id))
        add_result(map_name, warp_id)
        if not map_enterable(map_name):
            continue  # arrived via a door, but can't walk the map without its flag/HM
        for target_id in intra_map_targets(map_name, warp_id):
            add_result(map_name, target_id)
            warp_frontier.append((map_name, target_id))
        # We can only cross a governed connection from its exact border warp;
        # other border warps are reached as their own frontier nodes via intra
        # movement, at which point their crossings fire.
        try_crossings(map_name, lambda req, w=warp_id: req == w, warp_id)

    if cache is not None:
        cache[cache_key] = result
    return result


def reachable_exit_doors(reach, entry_map, entry_warp_id, map_warp_pairs):
    # Distinct logical doors (excluding the entry door) reachable from the arrival
    # warp, mapped to a representative warp that can be taken through that door.
    entry_door = warp_door_key(map_warp_pairs, entry_map, entry_warp_id)
    doors = {}
    for room_map, room_warp in reach:
        door = warp_door_key(map_warp_pairs, room_map, room_warp.warp_id)
        if door == entry_door:
            continue
        doors.setdefault(door, room_warp)
    return doors


def resolve_tracked_destination(dest_map, dest_warp_id, randomized_map_warps, map_room_warps,
                                map_connections, map_warp_pairs, gen_functions, reach_cache=None,
                                trace=None):
    # Follow a warp's destination to the tracked location it ultimately reaches.
    #
    # From the arrival warp we compute the warps actually reachable in that room
    # (respecting map_warp_accessibility) and decide:
    #   * arrival (or a single reachable warp) is sekii-tagged -> that location
    #   * exactly one non-entry door reachable, untagged  -> a corridor: jump
    #     through it and repeat
    #   * no reachable door                               -> 'dead_end'
    #   * more than one reachable door / tagged warp      -> 'unknown'
    # Returns (dest_tuple, final_map, final_warp_id) where dest_tuple matches
    # parse_sekii_id output or ('', 'dead_end'|'unknown', True).
    seen_doors = set()
    while True:
        arrival = randomized_map_warps[dest_map][0][dest_warp_id]
        arrival_tag = parse_sekii_id(arrival)
        if arrival_tag is not None:
            return arrival_tag, dest_map, dest_warp_id

        reach = reachable_room_warps(map_room_warps.get(dest_map, []), dest_map, dest_warp_id,
                                     map_connections, gen_functions, cache=reach_cache)

        tagged = [room_warp for _, room_warp in reach if getattr(room_warp, 'sekii_id', None)]
        if len(tagged) == 1:
            return parse_sekii_id(tagged[0]), dest_map, dest_warp_id
        if len(tagged) > 1:
            return ('', 'unknown', True), dest_map, dest_warp_id

        doors = reachable_exit_doors(reach, dest_map, dest_warp_id, map_warp_pairs)
        if len(doors) == 0:
            return ('', 'dead_end', True), dest_map, dest_warp_id
        if len(doors) > 1:
            return ('', 'unknown', True), dest_map, dest_warp_id

        # Exactly one forced exit -> a corridor. Jump through it and continue.
        entry_door = warp_door_key(map_warp_pairs, dest_map, dest_warp_id)
        if entry_door in seen_doors:
            if trace is not None:
                trace.append(('loop', dest_map, dest_warp_id, entry_door))
            return ('', 'unknown', True), dest_map, dest_warp_id
        seen_doors.add(entry_door)

        exit_warp = next(iter(doors.values()))
        next_map = exit_warp.dest_map
        next_warp_id = exit_warp.dest_warp_id
        if trace is not None:
            trace.append(('jump', dest_map, dest_warp_id, exit_warp.warp_id, next_map, next_warp_id))
        if next_map == '' or next_map == 'Map_None' or next_warp_id < 0 \
                or next_map not in randomized_map_warps \
                or next_warp_id >= len(randomized_map_warps[next_map][0]):
            # The corridor's far door leads nowhere valid -> a dead end.
            return ('', 'dead_end', True), dest_map, dest_warp_id
        dest_map, dest_warp_id = next_map, next_warp_id



def clean_up_map_warps(map_warps):
    clean_map_warps = dict()
    for map_name in map_warps:
        # For every map warp we must create clean copy where dest map and dest warp id are not set
        # This allows for us to easily check that every warp that was meant to be set was in fact set
        warps, connections = map_warps[map_name]
        temp1 = []
        temp2 = []
        for warp in warps:
            temp1.append(structs.Warp(warp.x, warp.y, 0, '', -1, warp.warp_id, warp.header_id,
                                      sekii_id=getattr(warp, 'sekii_id', None)))
        for connection in connections:
            temp2.append(structs.Connection('', 0, connection.map))
        clean_map_warps[map_name] = [temp1, temp2]
    return clean_map_warps


def check_randomized_map_warps(randomized_map_warps, map_warps, gen_functions, all_maps):
    # Lets Check that every warp intended to be randomized was randomized
    for map_name in randomized_map_warps:
        warps, connections = randomized_map_warps[map_name]
        orig_warps, orig_connections = map_warps[map_name]
        index = 0
        for warp in warps:
            if warp.dest_map == '' or warp.dest_warp_id == -1:
                # Map wasn't randomized... lets figure out if that is ok?
                is_in_dont_randomize = False  # need to check if map is in dont randomize
                for dont_randomize_map in gen_functions.info().dont_randomize:
                    if dont_randomize_map in map_name:
                        is_in_dont_randomize = True

                if map_name not in all_maps:
                    # We dont even consider this map as ever reachable and should not be randomized
                    warp.dest_map = orig_warps[index].dest_map
                    warp.dest_warp_id = orig_warps[index].dest_warp_id
                elif is_in_dont_randomize or map_name in gen_functions.info().not_needed:
                    # these maps are expected to not be randomized thus it is ok if it wasnt randomized
                    # however we should at least make sure that randomized_map_warps gets the correct warp info
                    warp.dest_map = orig_warps[index].dest_map
                    warp.dest_warp_id = orig_warps[index].dest_warp_id
                elif 'gym' in map_name.lower():
                    # Warps inside gym shouldn't be randomized, however the main entry of the gym should be randomized
                    if orig_warps[index].dest_map == map_name:
                        # A warp inside gym, so shouldn't be random
                        warp.dest_map = orig_warps[index].dest_map
                        warp.dest_warp_id = orig_warps[index].dest_warp_id
                    else:
                        # Gym entrance not randomized... this is a failure
                        return False
                elif (map_name in gen_functions.info().dont_randomize_warp and
                      warp.warp_id in gen_functions.info().dont_randomize_warp[map_name]):
                    # specific warp is listed as a dont randomize warp
                    # these warps should be assigned random warps from the not needed list
                    return False
                else:
                    # A warp should only not be defined it its specified in not needed, don't randomize, don't randomize
                    # warp, is not included in the all maps or is a warp inside a gym
                    # if we hit this scenario we have a bug
                    return False
            index = index + 1

    # If we get past the entire for loop then we know all warps are set
    return True


def check_flags(flag, current_flags_satisfied):
    bits = bin(flag)  # git binary representation of flag
    index = 0
    warp_pass = True
    for bit in reversed(bits):
        if bit == '1' and current_flags_satisfied[index] != 1:
            # if bit set, we check bits index location to determine if we currently consider that flag satisfied
            # if that flag is not satisfied, this is not a valid warp to go to
            warp_pass = False
            break
        index = index + 1
    return warp_pass


def map_flags_ok(gen_functions, map_name, flags_satisfied):
    # Whether a map's per-map flag requirements (map_flag_requirements, e.g. a
    # Surf-only water route) are met given flags_satisfied. This mirrors the
    # per-map gate at the top of is_map_progressable so the route/tracker
    # reachability engine honors the same rules. Gens that don't define
    # map_flag_requirements (or a None flag mask == full progression) pass freely.
    required_flags = getattr(gen_functions.info(), 'map_flag_requirements', {}).get(map_name, 0)
    if required_flags == 0 or flags_satisfied is None:
        return True
    return check_flags(required_flags, flags_satisfied)


# Find map based off current flag restrictions
# If it can't find map return empty path, otherwise return path taken
def find_map(map_to_find, warp_to_find, randomized_map_warps, gen_functions, current_flags_satisfied):
    paths_tested = [[(gen_functions.define_starting_map_id(), -1)]]
    maps_visited = [gen_functions.define_starting_map_id()]

    if map_to_find == gen_functions.define_starting_map_id():
        return [(gen_functions.define_starting_map_id(), -1)]

    while True:
        new_paths_tested = []
        for path in paths_tested:
            last_map, last_warp_id = path[len(path) - 1]

            next_warp_to_check = -2
            # check any special conditions for determining warp to start from if coming from connection
            if last_warp_id == -1:
                if (last_map in gen_functions.info().map_to_map_warp_accessibility and
                        path[len(path) - 2][0] in gen_functions.info().map_to_map_warp_accessibility[last_map]):
                    # ok so we should use this to define warp to start
                    warp_tuple = gen_functions.info().map_to_map_warp_accessibility[last_map][path[len(path) - 2][0]]
                    if check_flags(warp_tuple.flag, current_flags_satisfied):
                        # warp is valid
                        next_warp_to_check = warp_tuple.warp_id
            else:
                next_warp_to_check = last_warp_id

            warps, connections = randomized_map_warps[last_map]
            if next_warp_to_check != -2:
                # First we take all accessible warps and add them to the paths tested
                for warp in warps:
                    # Check map to see if there are any warp to warp restrictions
                    if last_map in gen_functions.info().map_warp_accessibility:
                        # if there are warp restrictions we must abide by these warp restrictions and add only the
                        # the allowed warps
                        if warp.warp_id in gen_functions.info().map_warp_accessibility[last_map]:
                            # warp rules will define the warps that connect to
                            warp_rules = gen_functions.info().map_warp_accessibility[last_map][warp.warp_id]


# This sanity check will be two fold... First we will check flag order list and ensure no warp is locked behind
# A check that should be complete after the current check we are on, and will create a cheat log for us
# cheat log is not 100% guaranteed to be the shortest path
# Second we will check that every map is reachable to starting map
def sanity_randomize_check(randomized_map_warps, map_warps, gen_functions, all_maps):
    flags_satisfied = [0] * len(gen_functions.info().FLAG_EVENT_LIST)
    for main_flag_check in gen_functions.info().FORCED_FLAG_ORDER:
        maps_to_find = gen_functions.info().FLAG_EVENT_LIST[main_flag_check]
        for map_to_find in maps_to_find:
            warp_to_find = -1
            if ':' in map_to_find:
                parts = map_to_find.split(':')
                map_to_find = parts[0]
                warp_to_find = int(parts[1])
            find_map(map_to_find, warp_to_find, randomized_map_warps, gen_functions, flags_satisfied)


def write_tracker_file(tracker_path, randomized_map_warps, map_warps, gen_functions, game='platinum',
                       line_colors=None):
    # Build room data (maps joined by their seamless connections) plus a
    # map->adjacent-maps table so we can resolve a warp's destination while
    # respecting map_warp_accessibility (which warps are actually reachable from
    # the arrival warp within a room).
    map_room_warps = build_room_warps(randomized_map_warps)
    map_connections = build_map_connections(randomized_map_warps, gen_functions)
    # Group physically adjacent warps (paired doors) so a paired door counts as a
    # single logical warp for door detection and emits only one line
    map_warp_pairs = build_warp_pairs(map_warps, gen_functions)
    # Cache accessibility BFS results keyed by arrival warp
    reach_cache = {}

    # Set up an extensive debug log dedicated to the "unknown" destination cases.
    # It is written next to the tracker file so it is easy to find after a run.
    debug_log_path = os.path.splitext(tracker_path)[0] + '_unknown_debug.log'
    logger = logging.getLogger('warp_randomizer.tracker.unknown')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    # Remove any handlers left over from a previous run so we don't duplicate output
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    debug_handler = logging.FileHandler(debug_log_path, mode='w', encoding='utf-8')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(debug_handler)
    logger.debug('Unknown-destination debug log for game=%s', game)

    with open(tracker_path, 'w', newline='\n') as f:
        # First line is the game marker, then one CSV row per tracked warp:
        # <game>,<mapA>,<valueA>,<warp|mark>,<mapB?>,<valueB>,
        f.write('#%s\n' % game)
        for map_name in randomized_map_warps:
            warps, connections = randomized_map_warps[map_name]
            for warp in warps:
                # Only emit one line per logical door - skip the non-representative
                # warps of a paired (adjacent) door since they share a destination
                _, door_rep = warp_door_key(map_warp_pairs, map_name, warp.warp_id)
                if door_rep != warp.warp_id:
                    continue
                # Only sekii-tagged warps are tracked locations. Marks are
                # destinations only, so they can never be a start node. (This also
                # naturally skips corridor doors, which are always untagged.)
                source = parse_sekii_id(warp)
                if source is None or source[2]:
                    continue
                # Follow the warp's destination to the tracked location it reaches,
                # jumping through forced corridors and honoring map_warp_accessibility.
                # If the destination is invalid it's a dead end.
                dest_map = warp.dest_map
                dest_warp_id = warp.dest_warp_id
                if dest_map == '' or dest_map == 'Map_None' or dest_warp_id < 0 \
                        or dest_map not in randomized_map_warps \
                        or dest_warp_id >= len(randomized_map_warps[dest_map][0]):
                    dest = ('', 'dead_end', True)
                else:
                    jump_trace = []
                    dest, final_map, final_warp_id = resolve_tracked_destination(
                        dest_map, dest_warp_id, randomized_map_warps, map_room_warps,
                        map_connections, map_warp_pairs, gen_functions,
                        reach_cache=reach_cache, trace=jump_trace)
                source_map, source_value, _ = source
                dest_map_label, dest_value, dest_is_mark = dest
                warp_type = 'mark' if dest_is_mark else 'warp'
                # An optional per-line colour is emitted as the trailing (7th)
                # field, e.g. "...,mart,#ce4069". Lines not in line_colors keep
                # the historical empty colour field.
                color = ''
                if line_colors is not None:
                    color = line_colors.get((source_map, source_value), '')
                f.write('%s,%s,%s,%s,%s,%s,%s\n' % (
                    game, source_map, source_value, warp_type, dest_map_label, dest_value, color))

    # Summarise and detach the debug handler so the file is flushed and closed
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def _shortest_path_states(randomized_map_warps, gen_functions, start_map, dest_map,
                          flags_satisfied=None, dest_warp_id=None):
    # Core reachability search shared by the path/route helpers. Returns
    # (states, edges) describing the shortest door-path from start_map to
    # dest_map, or ([], []) when no path exists.
    #
    # When dest_warp_id is None the search stops at the first warp of dest_map
    # that is reachable; when it is given, the search targets that specific warp
    # (map, dest_warp_id) instead.
    #
    # states[i] is a (map, warp_id) tuple; edges[i] is the edge taken to reach
    # states[i]. edges[0] is always None (the start). For i >= 1, edges[i] is
    # either the warp object of the door that was stepped through, or None when
    # states[i] was reached by walking inside the room.
    #
    # Reachability is modelled exactly like the tracker: reachable_room_warps
    # tells us which warps the player can walk to from a given position while
    # honoring both map_warp_accessibility (intra-map routing / one-way drops)
    # and map_to_map_warp_accessibility (seamless border crossings), following
    # connections through the whole room. Taking a warp door moves the player to
    # that warp's randomized destination. flags_satisfied is forwarded to
    # reachable_room_warps (None assumes full progression).
    #
    # A 0-1 BFS keeps the door count minimal: walking inside a room costs 0 and
    # taking a door costs 1, so the returned path goes through as few warps as
    # possible.
    from collections import deque

    if start_map not in randomized_map_warps or dest_map not in randomized_map_warps:
        return [], []
    if dest_warp_id is not None and dest_warp_id >= len(randomized_map_warps[dest_map][0]):
        return [], []  # requested a warp that does not exist on the destination map

    map_room_warps = build_room_warps(randomized_map_warps)
    map_connections = build_map_connections(randomized_map_warps, gen_functions)
    reach_cache = {}

    inf = float('inf')
    dist = {}
    prev = {}  # state -> (previous_state, door_warp_or_None); None means a walk
    frontier = deque()

    # The player starts standing in start_map, so every warp of that map is
    # immediately available as a starting point (cost 0).
    for warp in randomized_map_warps[start_map][0]:
        state = (start_map, warp.warp_id)
        dist[state] = 0
        prev[state] = (None, None)
        frontier.append(state)

    target = None
    while frontier:
        state = frontier.popleft()
        map_name, warp_id = state
        if dist[state] == inf:
            continue
        d = dist[state]
        if map_name == dest_map and (dest_warp_id is None or warp_id == dest_warp_id):
            target = state
            break

        # Walk edges (cost 0): every warp reachable inside the current room,
        # honoring the accessibility rules and connections.
        reach = reachable_room_warps(map_room_warps.get(map_name, []), map_name, warp_id,
                                     map_connections, gen_functions, cache=reach_cache,
                                     strict_cross_map=False, flags_satisfied=flags_satisfied)
        for room_map, room_warp in reach:
            neighbor = (room_map, room_warp.warp_id)
            if dist.get(neighbor, inf) > d:
                dist[neighbor] = d
                prev[neighbor] = (state, None)
                frontier.appendleft(neighbor)

        # Door edge (cost 1): step through this warp to its destination.
        warp = randomized_map_warps[map_name][0][warp_id]
        next_map = warp.dest_map
        next_warp_id = warp.dest_warp_id
        if next_map and next_map != 'Map_None' and next_warp_id is not None and next_warp_id >= 0 \
                and next_map in randomized_map_warps \
                and next_warp_id < len(randomized_map_warps[next_map][0]):
            neighbor = (next_map, next_warp_id)
            if dist.get(neighbor, inf) > d + 1:
                dist[neighbor] = d + 1
                prev[neighbor] = (state, warp)
                frontier.append(neighbor)

    if target is None:
        return [], []

    # Walk the predecessor chain back to a start state.
    chain = []
    state = target
    while state is not None:
        previous_state, door_warp = prev[state]
        chain.append((state, door_warp))
        state = previous_state
    chain.reverse()
    states = [entry[0] for entry in chain]
    edges = [entry[1] for entry in chain]
    return states, edges


def _connection_path(from_map, to_map, map_connections):
    # Shortest sequence of maps (inclusive of both ends) walked from from_map to
    # to_map over seamless connections, used to describe a walk in the route file.
    if from_map == to_map:
        return [from_map]
    from collections import deque
    prev = {from_map: None}
    frontier = deque([from_map])
    while frontier:
        current = frontier.popleft()
        if current == to_map:
            break
        for adjacent in map_connections.get(current, ()):
            if adjacent not in prev:
                prev[adjacent] = current
                frontier.append(adjacent)
    if to_map not in prev:
        return [from_map, to_map]  # fallback: no connection route found
    path = []
    node = to_map
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path


def find_path_warps(randomized_map_warps, map_warps, gen_functions, start_map, dest_map,
                    flags_satisfied=None):
    # Return the ordered list of warp objects (doors) a player must step through
    # to get from start_map to dest_map in the randomized world. See
    # _shortest_path_states for the reachability model and flags_satisfied.
    _states, edges = _shortest_path_states(randomized_map_warps, gen_functions, start_map, dest_map,
                                           flags_satisfied=flags_satisfied)
    return [edge for edge in edges if edge is not None]


def find_route_steps(randomized_map_warps, gen_functions, start_map, dest_map, flags_satisfied=None,
                     dest_warp_id=None):
    # Build the human-readable, step-by-step route from start_map to dest_map.
    # Plain "Map_X" lines are maps walked through via connections; "Map_X[n]"
    # lines are warp n of Map_X (a door being taken, immediately followed by the
    # warp arrived at on the other side). Returns [] when no route exists.
    # When dest_warp_id is given the route targets that specific warp and ends on
    # its warp label rather than the bare destination map name.
    #
    # A step that can only be taken once a progression flag is held is annotated
    # with " (w/ <flags>)". The gate can come from any of the reachability
    # sources: a per-map requirement (map_flag_requirements, built from the
    # *_needed lists), an intra-map routing rule (map_warp_accessibility) or a
    # seamless border crossing (map_to_map_warp_accessibility).
    states, edges = _shortest_path_states(randomized_map_warps, gen_functions, start_map, dest_map,
                                          flags_satisfied=flags_satisfied, dest_warp_id=dest_warp_id)
    if not states:
        return []

    map_connections = build_map_connections(randomized_map_warps, gen_functions)
    if flags_satisfied is not None:
        # Don't describe a walk that crosses a map the player can't yet traverse
        # (e.g. a Surf water route before Surf); keep the printed path consistent
        # with the reachability model used by _shortest_path_states above.
        map_connections = {
            m: [a for a in adj if map_flags_ok(gen_functions, a, flags_satisfied)]
            for m, adj in map_connections.items()
        }

    info_module = gen_functions.info()
    map_req = getattr(info_module, 'map_flag_requirements', {})
    accessibility = getattr(info_module, 'map_warp_accessibility', {})
    map_to_map = getattr(info_module, 'map_to_map_warp_accessibility', {})

    # flag bit index -> short human name, e.g. 5 -> 'bike' (from BIKE_FLAG).
    flag_names = {}
    for _name, _value in vars(info_module).items():
        if _name.endswith('_FLAG') and _name != 'END_FLAG' and isinstance(_value, int):
            flag_names.setdefault(_value, _name[:-len('_FLAG')].lower())

    def mask_to_text(mask):
        # " (w/ bike, cut)" for a gate bitmask, or '' when nothing is required.
        if not mask:
            return ''
        names = []
        bit = 0
        while (1 << bit) <= mask:
            if mask & (1 << bit):
                names.append(flag_names.get(bit, 'flag%d' % bit))
            bit += 1
        return ' (w/ %s)' % ', '.join(names)

    def flag_satisfied(mask):
        return flags_satisfied is None or check_flags(mask, flags_satisfied)

    def crossing_mask(from_map, to_map):
        # Flags gating the seamless connection from_map -> to_map (either the
        # outgoing or the incoming border rule may carry one).
        mask = 0
        if from_map in map_to_map and to_map in map_to_map[from_map]:
            mask |= map_to_map[from_map][to_map].flag
        if to_map in map_to_map and from_map in map_to_map[to_map]:
            mask |= map_to_map[to_map][from_map].flag
        return mask

    def intra_map_mask(map_name, src_warp, dst_warp):
        # Flags gating movement between two warps of the same map. Finds the
        # flag-satisfied intra-map path from src to dst that needs the fewest
        # flags and returns the union of the flags it crosses.
        if src_warp == dst_warp or map_name not in accessibility:
            return 0
        rules = accessibility[map_name]
        best = {src_warp: 0}
        changed = True
        while changed:
            changed = False
            for node in list(best):
                base = best[node]
                for wt in rules.get(node, []):
                    if not flag_satisfied(wt.flag):
                        continue
                    new_mask = base | wt.flag
                    current = best.get(wt.warp_id)
                    if current is None or bin(new_mask).count('1') < bin(current).count('1'):
                        best[wt.warp_id] = new_mask
                        changed = True
        return best.get(dst_warp, 0)

    def warp_label(map_name, warp_id, warp_obj=None):
        # "Map_X[n]", with " (sekii_id)" appended when the warp is a tracked one.
        if warp_obj is None:
            warp_obj = randomized_map_warps[map_name][0][warp_id]
        sekii_id = getattr(warp_obj, 'sekii_id', None)
        if sekii_id:
            return '%s[%d] (%s)' % (map_name, warp_id, sekii_id)
        return '%s[%d]' % (map_name, warp_id)

    lines = [start_map]
    current_map, current_warp_id = states[0]
    # Flags needed by an intra-map hop that produced no line of its own; they are
    # attached to the next emitted line (the door taken from that warp).
    pending_mask = 0
    for edge, state in zip(edges[1:], states[1:]):
        state_map, state_warp_id = state
        if edge is None:
            if state_map == current_map:
                # Intra-map hop: no line, but remember any flags it needed.
                pending_mask |= intra_map_mask(current_map, current_warp_id, state_warp_id)
            else:
                # Walked to state_map: list every map crossed (excluding where we
                # already stand), annotating each with the flags needed to enter
                # it (border-crossing rule + that map's own requirement).
                path = _connection_path(current_map, state_map, map_connections)
                for i in range(1, len(path)):
                    step_mask = pending_mask | crossing_mask(path[i - 1], path[i]) | map_req.get(path[i], 0)
                    pending_mask = 0
                    lines.append(path[i] + mask_to_text(step_mask))
        else:
            # Stepped through a door: show the source warp (carrying any flags the
            # intra-map hop to reach it needed) then the arrival warp.
            lines.append(warp_label(current_map, edge.warp_id, edge) + mask_to_text(pending_mask))
            pending_mask = 0
            lines.append(warp_label(state_map, state_warp_id))
        current_map, current_warp_id = state_map, state_warp_id

    # Finish by naming the destination. When a specific warp was requested end on
    # its warp label; otherwise name the destination map itself (unless we already
    # walked into it as the last plain line). Ignore any trailing flag annotation
    # when checking whether the destination was already emitted.
    if dest_warp_id is not None:
        dest_label = warp_label(dest_map, dest_warp_id)
    else:
        dest_label = dest_map

    def strip_flags(text):
        marker = text.find(' (w/ ')
        return text[:marker] if marker != -1 else text

    if not lines or strip_flags(lines[-1]) != dest_label:
        lines.append(dest_label)
    return lines


def write_route_file(routes_path, randomized_map_warps, gen_functions, start_map):
    # Write the progression visit-order list (see build_visit_order_lines): every
    # flag event in the order it is actually obtained (the acquisition timeline
    # built below), listing only the new maps unlocked by each event. Under every
    # "To <map>[:warp]" line, append the step-by-step route to travel from
    # start_map to that map in the randomized world (see find_route_steps).
    #
    # The route for a map is computed with the flags we can expect to already
    # have when that event is reached. Those flags come from a progression
    # timeline built below: the free (non-forced) flags are tried first, before
    # any forced flag, and any that aren't reachable yet are retried after each
    # forced flag is resolved. So an event's route uses every forced flag ordered
    # before it in FORCED_FLAG_ORDER plus every free flag obtainable by that
    # point (e.g. the Bike, if its shop was reachable earlier).
    info = gen_functions.info()
    forced_order = info.FORCED_FLAG_ORDER
    flag_event_list = info.FLAG_EVENT_LIST
    flag_count = len(flag_event_list)

    # Free (non-forced) flags are HMs/items that aren't pinned to a fixed spot in
    # the progression order (e.g. the Bike). Instead of assuming they are all
    # obtained last, we try to grab them as early as possible - before any forced
    # flag - and, whenever one isn't reachable yet, retry it after each following
    # forced flag is resolved. This builds a realistic acquisition timeline.
    free_flags = [f for f in range(flag_count) if f not in forced_order]

    # Cache reachability of a single (map, warp) target under a given satisfied
    # set so the repeated fixpoint passes below don't redo the same BFS.
    reach_cache = {}

    def target_reachable(dest_map, dest_warp_id, satisfied_key, vec):
        key = (dest_map, dest_warp_id, satisfied_key)
        if key not in reach_cache:
            states, _ = _shortest_path_states(randomized_map_warps, gen_functions,
                                              start_map, dest_map,
                                              flags_satisfied=vec, dest_warp_id=dest_warp_id)
            reach_cache[key] = bool(states)
        return reach_cache[key]

    def event_reachable(flag, satisfied):
        # An event is obtainable only when every map/warp it requires is
        # reachable with the flags currently held.
        satisfied_key = frozenset(satisfied)
        vec = [1 if f in satisfied else 0 for f in range(flag_count)]
        for req in flag_event_list[flag]:
            parts = req.split(':')
            dest_map = parts[0]
            dest_warp_id = int(parts[1]) if len(parts) > 1 else None
            if not target_reachable(dest_map, dest_warp_id, satisfied_key, vec):
                return False
        return True

    # Build the progression timeline. satisfied_before[flag] is the set of flags
    # the player already holds when this flag's event is reached, so its route is
    # drawn with exactly those flags available. timeline_order records the events
    # in the order they are obtained so the file reads naturally top-to-bottom.
    satisfied = set()
    satisfied_before = {}
    unresolved_free = set(free_flags)
    timeline_order = []

    def resolve_free_flags():
        # Grab every free flag reachable now; obtaining one may unlock another,
        # so loop until no further progress (a fixpoint).
        progressed = True
        while progressed:
            progressed = False
            for f in sorted(unresolved_free):
                if event_reachable(f, satisfied):
                    satisfied_before[f] = set(satisfied)
                    satisfied.add(f)
                    unresolved_free.discard(f)
                    timeline_order.append(f)
                    progressed = True

    # Free flags first...
    resolve_free_flags()
    # ...then each forced flag in order, retrying the free flags after each one.
    for flag in forced_order:
        satisfied_before[flag] = set(satisfied)
        satisfied.add(flag)
        timeline_order.append(flag)
        resolve_free_flags()

    # A free flag that never became reachable (genuinely blocked): draw its route
    # with everything that could be obtained, so it honestly reports no route.
    for f in sorted(unresolved_free):
        satisfied_before[f] = set(satisfied)
        timeline_order.append(f)

    def flags_satisfied_for(flag):
        reached = satisfied_before.get(flag, set())
        return [1 if f in reached else 0 for f in range(flag_count)]

    def route_for(req, flag):
        parts = req.split(':')
        dest_map = parts[0]
        dest_warp_id = int(parts[1]) if len(parts) > 1 else None
        steps = find_route_steps(randomized_map_warps, gen_functions, start_map, dest_map,
                                 flags_satisfied=flags_satisfied_for(flag),
                                 dest_warp_id=dest_warp_id)
        if not steps:
            return ['  (no route found)']
        return ['  -> %s' % step for step in steps]

    lines = build_visit_order_lines(gen_functions, extra_lines_for_map=route_for,
                                    flag_order=timeline_order)

    # Append routes to any extra endgame targets (e.g. the Elite Four / Champion
    # chambers) listed in info().final_rooms. These aren't tied to a progression
    # flag, so draw them assuming every flag has been obtained (full progression).
    final_rooms = getattr(info, 'final_rooms', None)
    if final_rooms:
        all_flags = [1] * flag_count
        lines.append('========== FINAL ROOMS ==========')
        lines.append('')
        for req in final_rooms:
            parts = req.split(':')
            dest_map = parts[0]
            dest_warp_id = int(parts[1]) if len(parts) > 1 else None
            steps = find_route_steps(randomized_map_warps, gen_functions, start_map, dest_map,
                                     flags_satisfied=all_flags, dest_warp_id=dest_warp_id)
            lines.append('To %s' % req)
            if not steps:
                lines.append('  (no route found)')
            else:
                lines.extend('  -> %s' % step for step in steps)
            lines.append('')

    with open(routes_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))
        if lines:
            f.write('\n')


def write_path_tracker_file(tracker_path, randomized_map_warps, map_warps, gen_functions,
                            start_map, dest_map, color, game='platinum', flags_satisfied=None):
    # Write a normal tracker file, but colour every tracked warp that lies on a
    # shortest door-path from start_map to dest_map with the given colour code.
    # flags_satisfied restricts which progression flags may be traversed (None
    # assumes full progression); see find_path_warps.
    doors = find_path_warps(randomized_map_warps, map_warps, gen_functions, start_map, dest_map,
                            flags_satisfied=flags_satisfied)

    line_colors = {}
    for warp in doors:
        tag = parse_sekii_id(warp)
        if tag is None:
            continue  # untagged corridor door - it has no tracker line of its own
        map_part, value_part, is_mark = tag
        if is_mark:
            continue  # marks are destinations only, never a tracked source line
        line_colors[(map_part, value_part)] = color

    write_tracker_file(tracker_path, randomized_map_warps, map_warps, gen_functions,
                       game=game, line_colors=line_colors)


def write_warp_pairs_file(warps_path, randomized_map_warps):
    # Write every randomized warp pair, one per line, in the form:
    #   MapA[warpA] <-> MapB[warpB]
    # Each pair is emitted only once (the two directions of a warp share a line).
    # Only true two-way pairs are written: both sides must point at each other.
    # Some warps (e.g. most shops) are never randomized and still lead to their
    # original location, while that original location is correctly randomized to
    # point somewhere else. Those one-directional links are skipped.
    seen = set()
    lines = []
    for map_name in randomized_map_warps:
        warps, connections = randomized_map_warps[map_name]
        for warp in warps:
            dest_map = warp.dest_map
            dest_warp_id = warp.dest_warp_id
            if dest_map == '' or dest_map == 'Map_None' or dest_warp_id < 0:
                # Warp was never assigned a destination -> nothing to pair.
                continue
            # Look up the warp on the destination side and confirm it points back
            # at this warp. If it doesn't, this is a one-way link and we skip it.
            if dest_map not in randomized_map_warps:
                continue
            dest_warps = randomized_map_warps[dest_map][0]
            if dest_warp_id >= len(dest_warps):
                continue
            dest_warp = dest_warps[dest_warp_id]
            if dest_warp.dest_map != map_name or dest_warp.dest_warp_id != warp.warp_id:
                continue
            # Canonical key so we don't print both directions of the same pair.
            side_a = (map_name, warp.warp_id)
            side_b = (dest_map, dest_warp_id)
            key = tuple(sorted((side_a, side_b)))
            if key in seen:
                continue
            seen.add(key)

            def format_side(side_map, side_warp):
                # Append the sekii_id in braces when the warp is a tracked location.
                sekii_id = getattr(side_warp, 'sekii_id', None)
                if sekii_id:
                    return '%s[%s] (%s)' % (side_map, side_warp.warp_id, sekii_id)
                return '%s[%s]' % (side_map, side_warp.warp_id)

            lines.append('%s <-> %s' % (
                format_side(map_name, warp), format_side(dest_map, dest_warp)))

    with open(warps_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))
        if lines:
            f.write('\n')


def start_randomizer(input_rom_path, output_rom_path, rom_type, fixed_seed=-1, revision=0):
    if fixed_seed != -1:
        if isinstance(fixed_seed, int):
            rng = random_generator.Random(seed=fixed_seed)
        else:
            rng = random_generator.Random(seed=hash(fixed_seed))
    else:
        fixed_seed = random_generator.randrange(sys.maxsize)
        rng = random_generator.Random(seed=fixed_seed)

    if rom_type == Definitions.GEN3_EMERALD:
        gen_functions = EmeraldWarpRandomizer.EmeraldRandomizerFunctions()
    elif rom_type == Definitions.GEN4_PLATINUM:
        gen_functions = PlatinumWarpRandomizer.PlatinumRandomizerFunctions()
    elif rom_type == Definitions.GEN4_HEARTGOLD or rom_type == Definitions.GEN4_SOULSILVER:  # todo add back later
        gen_functions = JohtoWarpRandomizer.HeartGoldSoulSilverRandomizerFunctions()
    elif rom_type == Definitions.GEN3_FIRERED or rom_type == Definitions.GEN3_LEAFGREEN:
        gen_functions = FireRedWarpRandomizer.FireRedRandomizerFunctions(rom_type, revision)
    elif rom_type == Definitions.GEN5_WHITE2:  # todo put b2 back when we support it
        gen_functions = White2WarpRandomizer.White2RandomizerFunctions()
    else:
        return True, fixed_seed, True

    print('Loading data')
    map_warps = gen_functions.load_map_data()
    starting_node, map_nodes, valid_warps = build_map(map_warps, gen_functions)
    non_reachable_to_add = gen_functions.determine_unreachable_maps(map_nodes, map_warps)
    all_maps = list(map_nodes.keys())
    all_maps = all_maps + non_reachable_to_add
    randomized_map_warps = clean_up_map_warps(map_warps)

    print('Randomizing')
    if not randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps):
        print('Seed Failed')
        return False, fixed_seed, False

    if not check_randomized_map_warps(randomized_map_warps, map_warps, gen_functions, all_maps):
        print('Seed Incorrect')
        return False, fixed_seed, False

    print('Writing meta')
    additional_output_base = os.path.splitext(output_rom_path)[0]

    # Collect every output file (ROM + meta text files) in a temporary
    # directory so they can be bundled into a single .zip archive instead of
    # being scattered across the destination folder as loose files.
    staging_dir = tempfile.mkdtemp(prefix='warp_randomizer_')
    staged_files = []
    try:
        base_name = os.path.basename(additional_output_base)
        # The destination path is a .zip archive, so derive the ROM's filename
        # inside the archive from the input ROM's extension (.gba / .nds) to keep
        # it a valid, loadable game file.
        rom_extension = os.path.splitext(input_rom_path)[1]
        rom_name = base_name + rom_extension

        seed_path = os.path.join(staging_dir, base_name + '_seed.txt')
        print("seed path is: " + seed_path)
        with open(seed_path, 'w') as f:
            f.write(str(fixed_seed))
        staged_files.append(seed_path)

        warps_path = os.path.join(staging_dir, base_name + '_warps.txt')
        print("warps path is: " + warps_path)
        write_warp_pairs_file(warps_path, randomized_map_warps)
        staged_files.append(warps_path)

        tracker_path = os.path.join(staging_dir, base_name + '_tracker.txt')
        print("tracker path is: " + tracker_path)
        write_tracker_file(tracker_path, randomized_map_warps, map_warps, gen_functions)
        staged_files.append(tracker_path)

        if rom_type == Definitions.GEN4_PLATINUM:
            # Human-readable, step-by-step progression route: the visit order of every
            # newly-unlocked map (forced flag events first, then the rest) with the
            # path to reach each map from the starting town.
            routes_path = os.path.join(staging_dir, base_name + '_routes.txt')
            print("routes path is: " + routes_path)
            write_route_file(
                routes_path, randomized_map_warps, gen_functions,
                gen_functions.define_starting_map_id())
            staged_files.append(routes_path)

        print('Writing ROM')
        staged_rom_path = os.path.join(staging_dir, rom_name)
        gen_functions.write_rom(input_rom_path, staged_rom_path, randomized_map_warps)
        staged_files.append(staged_rom_path)

        zip_path = additional_output_base + '.zip'
        print("zip path is: " + zip_path)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file_path in staged_files:
                archive.write(file_path, os.path.basename(file_path))
    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)

    return True, fixed_seed, False


def logic_brute_forcer(rom_type, fixed_seed=-1):
    if fixed_seed != -1:
        if isinstance(fixed_seed, int):
            rng = random_generator.Random(seed=fixed_seed)
        else:
            rng = random_generator.Random(seed=hash(fixed_seed))
    else:
        fixed_seed = random_generator.randrange(sys.maxsize)
        rng = random_generator.Random(seed=fixed_seed)

    if rom_type == Definitions.GEN3_EMERALD:
        gen_functions = EmeraldWarpRandomizer.EmeraldRandomizerFunctions()
    elif rom_type == Definitions.GEN4_PLATINUM:
        gen_functions = PlatinumWarpRandomizer.PlatinumRandomizerFunctions()
    # elif rom_type == Definitions.GEN4_HEARTGOLD or rom_type == Definitions.GEN4_SOULSILVER:
    #     gen_functions = JohtoWarpRandomizer.HeartGoldSoulSilverRandomizerFunctions()
    else:
        return True, fixed_seed

    map_warps = gen_functions.load_map_data()
    starting_node, map_nodes, valid_warps = build_map(map_warps, gen_functions)
    non_reachable_to_add = gen_functions.determine_unreachable_maps(map_nodes, map_warps)
    all_maps = list(map_nodes.keys())
    all_maps = all_maps + non_reachable_to_add
    randomized_map_warps = clean_up_map_warps(map_warps)

    if not randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps):
        print('moo')
        return False, fixed_seed

    if rom_type == Definitions.GEN4_PLATINUM:
        """This is for testing for gyms locked behind one-way warps"""
        # for entry in PlatinumWarpMapInfo.potential_softlock_warps:
        #     for warp_id in PlatinumWarpMapInfo.potential_softlock_warps[entry]:
        #         dest = map_warps[entry][0][warp_id].dest_map
        #         dest_warp = map_warps[entry][0][warp_id].dest_warp_id
        #         if 'Gym' in dest or 'League' in dest:
        #             if len(map_warps[dest][0]) == 1 and len(map_warps[dest][1]) == 0:
        #                 print(fixed_seed)
        #                 print('%s warp %i points to %s warp %i' % (entry, map_warps[entry][0][warp_id].warp_id, dest, dest_warp))
        #                 return True, fixed_seed

        """This is for finding maps locked behind an incorrect HM requirement"""
        found = False
        cancelled = False
        out = ''
        for event_idx in range(len(PlatinumWarpMapInfo.FLAG_EVENT_LIST)):
            for entry in PlatinumWarpMapInfo.FLAG_EVENT_LIST[event_idx]:
                entry = entry.split(':')[0]
                for warp_id in range(len(map_warps[entry][0])):
                    dest = map_warps[entry][0][warp_id].dest_map
                    dest_warp = map_warps[entry][0][warp_id].dest_warp_id
                    if dest in PlatinumWarpMapInfo.map_warp_accessibility.keys():
                        for warp_accessibility_id in PlatinumWarpMapInfo.map_warp_accessibility[dest]:
                            if warp_accessibility_id != dest_warp:
                                for warp_tuple in PlatinumWarpMapInfo.map_warp_accessibility[dest][
                                    warp_accessibility_id]:
                                    if warp_tuple.warp_id == dest_warp and (warp_tuple.flag >> event_idx) & 0b1 == 1:
                                        found = True
                                        out = '%s warp %i points to %s warp %i' % (
                                        dest, dest_warp, entry, map_warps[entry][0][warp_id].warp_id)
                                        continue
                                    if found and warp_tuple.warp_id == dest_warp and (
                                            warp_tuple.flag >> event_idx) & 0b1 == 0:
                                        cancelled = True
                                        continue

        if found and not cancelled:
            print(fixed_seed)
            print(out)
            return True, fixed_seed


if __name__ == "__main__":
    # result = start_randomizer(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    """This is for running the brute forcer"""
    # while True:
    #     result = logic_brute_forcer(Definitions.GEN4_PLATINUM)
    #     if result is not None:
    #         if result[0]:
    #             break
    #         else:
    #             continue
    #     else:
    #         continue
    # print('end')
