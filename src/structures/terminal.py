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
        __pragma__('js', '{}', 'Memory.counters["terminal_time"] = TERMINAL_TIME')
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
        actual = Memory.counters["terminal_time"]
        __pragma__('js', '{}', 'Memory.counters["terminal_time"] = actual - 1')


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

