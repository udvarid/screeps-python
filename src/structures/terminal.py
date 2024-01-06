from src.constant.my_constants import TERMINAL_TIME
from src.defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def operate_terminals():
    if not Memory.counters["terminal_time"] or Memory.counters["terminal_time"] <= 0:
        time_limit = TERMINAL_TIME
        __pragma__('js', '{}', 'Memory.counters["terminal_time"] = time_limit')
        energy_cost = undefined
        for room_name in Object.keys(Game.rooms):
            room = Game.rooms[room_name]
            terminal = room.terminal
            if room.controller.level >= 6 and terminal is not undefined:
                mineral = Memory.room_snapshot[room.name]['mineral']
                mineral_amount = terminal.store.getUsedCapacity(mineral)
                energy_amount = terminal.store.getUsedCapacity(RESOURCE_ENERGY)
                if mineral_amount >= 1000 and energy_amount >= 1000:
                    if energy_cost == undefined:
                        energy_cost = calculate_energy_cost()
                    best_order = get_best_order(energy_cost, room_name, mineral)
                    if best_order is not undefined and best_order[1] > 0:
                        Game.market.deal(best_order[0].id, 1000, room_name)
                else:
                    if created_ghodium_order(terminal):
                        return
                    if create_booster_order(terminal):
                        return
                    if bought_extra_energy(terminal, energy_cost):
                        return

    else:
        actual = Memory.counters["terminal_time"]
        __pragma__('js', '{}', 'Memory.counters["terminal_time"] = actual - 1')


def bought_extra_energy(terminal, energy_cost):
    energy_amount = terminal.room.storage.store.getUsedCapacity(RESOURCE_ENERGY)
    room_name = terminal.room.name
    if energy_amount < 100000 and Game.market.credits > 5000000:
        if energy_cost == undefined:
            energy_cost = calculate_energy_cost()
        best_order = get_best_energy_order(energy_cost, room_name)
        if best_order is not undefined:
            Game.market.deal(best_order[0].id, 10000, room_name)


def create_booster_order(terminal):
    neighbours = Memory['room_map'][terminal.room.name]['neighbours']
    n_rooms = []
    if neighbours['up'] != 'NO' and neighbours['up'] != '?':
        n_rooms.append(neighbours['up'])
    if neighbours['bottom'] != 'NO' and neighbours['bottom'] != '?':
        n_rooms.append(neighbours['bottom'])
    if neighbours['right'] != 'NO' and neighbours['right'] != '?':
        n_rooms.append(neighbours['right'])
    if neighbours['left'] != 'NO' and neighbours['left'] != '?':
        n_rooms.append(neighbours['left'])

    room_has_occupied_neighbour = False
    for n_room in n_rooms:
        room_state = Memory['room_map'][n_room]
        if room_state is not undefined and room_state['owner'] == 'occupied':
            room_has_occupied_neighbour = True

    if room_has_occupied_neighbour:
        boosted_minerals = [RESOURCE_CATALYZED_UTRIUM_ACID,
                            RESOURCE_CATALYZED_KEANIUM_ALKALIDE,
                            RESOURCE_CATALYZED_LEMERGIUM_ALKALIDE,
                            RESOURCE_CATALYZED_GHODIUM_ALKALIDE]
        for boosted_mineral in boosted_minerals:
            missing_mineral = get_missing_mineral(terminal, boosted_mineral)
            if missing_mineral == 0:
                continue
            room_has_mineral_order = room_has_active_order(terminal, boosted_mineral)
            if room_has_mineral_order:
                continue
            history = Game.market.getHistory(boosted_mineral)
            if len(history) == 0:
                continue
            price = history[len(history) - 1]['avgPrice'] * 1.1
            room_name = terminal.room.name
            print("creating {} order in room {}".format(boosted_mineral, room_name))
            Game.market.createOrder(ORDER_BUY, boosted_mineral, price, missing_mineral, room_name)
            return True
    return False


def created_ghodium_order(terminal):
    missing_ghodium = get_missing_mineral(terminal, RESOURCE_GHODIUM)
    if missing_ghodium == 0:
        return False
    room_has_ghodium_order = room_has_active_order(terminal, RESOURCE_GHODIUM)
    if room_has_ghodium_order:
        return False
    history = Game.market.getHistory(RESOURCE_GHODIUM)
    if len(history) == 0:
        return False
    price = history[len(history) - 1]['avgPrice'] * 1.1
    room_name = terminal.room.name
    print("creating Ghodium order in room {}".format(room_name))
    Game.market.createOrder(ORDER_BUY, RESOURCE_GHODIUM, price, missing_ghodium, room_name)
    return True


def room_has_active_order(terminal, mineral):
    my_orders = Game.market.orders
    my_order_ids = Object.keys(my_orders)
    room_has_mineral_order = False
    for my_order_id in my_order_ids:
        my_order = my_orders[my_order_id]
        if my_order['resourceType'] == mineral and \
                my_order['roomName'] == terminal.room.name and \
                my_order['remainingAmount'] > 0:
            room_has_mineral_order = True
            break
    return room_has_mineral_order


def get_missing_mineral(terminal, mineral):
    mineral_in_terminal = terminal.store.getUsedCapacity(mineral)
    mineral_in_store = terminal.room.storage.store.getUsedCapacity(mineral)
    mineral_in_hauler = 0
    haulers = list(filter(lambda c: c.memory.role == 'hauler', terminal.room.find(FIND_MY_CREEPS)))
    for hauler in haulers:
        mineral_in_hauler += hauler.store.getUsedCapacity(mineral)
    mineral_in_claimer = 0
    safe_mode_claimers = list(filter(lambda c: c.memory.role == 'safe_mode_claimer',
                                     terminal.room.find(FIND_MY_CREEPS)))
    for safe_mode_claimer in safe_mode_claimers:
        mineral_in_claimer += safe_mode_claimer.store.getUsedCapacity(mineral)
    mineral_in_labs = 0
    labs = list(filter(lambda s: s.sturctureType == STRUCTURE_LAB, terminal.room.find(FIND_MY_STRUCTURES)))
    for lab in labs:
        mineral_in_labs += lab.store.getUsedCapacity(mineral)
    mineral_in_room = mineral_in_terminal + mineral_in_store + mineral_in_hauler + mineral_in_claimer + mineral_in_labs
    return max(1000 - mineral_in_room, 0)


def calculate_energy_cost():
    order_sell = Game.market.getAllOrders({'type': ORDER_SELL, 'resourceType': RESOURCE_ENERGY})
    order_sell_smallest = sorted(order_sell, key=lambda c: c.price)[0]
    return order_sell_smallest.price * 1.1


def get_best_order(energy_cost, room_name, mineral):
    orders = Game.market.getAllOrders({'type': ORDER_BUY, 'resourceType': mineral})
    orders_with_cost = []
    for order in orders:
        if order.amount < 1000:
            continue
        cost = Game.market.calcTransactionCost(1000, room_name, order.roomName)
        profit = order.price * 1000 - cost * energy_cost
        orders_with_cost.append((order, profit))
    if len(orders_with_cost) > 0:
        best_order = sorted(orders_with_cost, key=lambda c: c[1])[len(orders_with_cost) - 1]
        return best_order
    else:
        return undefined


def get_best_energy_order(energy_cost, room_name):
    orders = Game.market.getAllOrders({'type': ORDER_SELL, 'resourceType': RESOURCE_ENERGY})
    orders_with_cost = []
    for order in orders:
        if order.amount < 10000:
            continue
        cost = Game.market.calcTransactionCost(10000, room_name, order.roomName)
        if cost > 3333 or order.price > energy_cost * 1.2:
            return undefined
        total_cost = order.price * 10000 + cost * energy_cost
        orders_with_cost.append((order, total_cost))
    if len(orders_with_cost) > 0:
        sorted_orders = sorted(orders_with_cost, key=lambda c: c[1])
        best_order = sorted_orders[0]
        return best_order
    else:
        return undefined
