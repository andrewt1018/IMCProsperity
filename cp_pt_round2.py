from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        # Pairs trading variables
        self.pt_ratio = np.array([])
        self.warmup_period = 1000
        self.in_pt = False
        self.coconut_pt_position = 0
        self.pina_pt_position = 0
        self.open_epsilon = 0.20
        self.close_epsilon = 0.02

        self.profit = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        pearls = 'PEARLS'
        bananas = 'BANANAS'
        coconuts = 'COCONUTS'
        pinas = 'PINA_COLADAS'
        pearls_position_limit = 20
        bananas_position_limit = 20
        coconuts_position_limit = 600
        pinas_position_limit = 300

        bananas_position = state.position.get(bananas)
        pearls_position = state.position.get(pearls)
        pinas_position = state.position.get(pinas)
        coconuts_position = state.position.get(coconuts)
        if bananas_position is None:
            bananas_position = 0
        if pearls_position is None:
            pearls_position = 0
        if coconuts_position is None:
            coconuts_position = 0
        if pinas_position is None:
            pinas_position = 0

        # Calculate Revenue
        if state.own_trades is not None:
            for symbol in state.own_trades:
                for trade in state.own_trades.get(symbol):
                    if trade.timestamp == state.timestamp - 100:  # Ensure trade is from previous iteration
                        if trade.seller == "":  # SUBMISSION << ""
                            self.profit = self.profit - trade.price * trade.quantity
                        elif trade.buyer == "":  # "" << SUBMISSION
                            self.profit = self.profit + trade.price * trade.quantity
        print("Profit: ", self.profit)
        print("Positions: ", state.position)
        result = {}

        orders: list[Order] = []

        coconuts_order_depth = state.order_depths.get(coconuts)
        pina_order_depth = state.order_depths.get(pinas)

        max_buy_pina = max(pina_order_depth.buy_orders.keys())
        max_buy_coco = max(coconuts_order_depth.buy_orders.keys())
        min_sell_pina = min(pina_order_depth.sell_orders.keys())
        min_sell_coco = min(coconuts_order_depth.sell_orders.keys())
        mid_coco = (min_sell_coco - max_buy_coco) / 2.0
        mid_pina = (min_sell_pina - max_buy_pina) / 2.0
        ratio = mid_pina / mid_coco
        # Update pairs trading average
        if len(self.pt_ratio) < self.warmup_period / 100:  # Ensure there are 10 in the average ratio array
            # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
            self.pt_ratio = np.append(self.pt_ratio, ratio)
        else:
            self.pt_ratio[:-1] = self.pt_ratio[1:]
            self.pt_ratio[-1] = ratio

        average_ratio = np.average(self.pt_ratio)
        print("Average_ratio: ", average_ratio)
        if self.in_pt:
            if (self.coconut_pt_position != 0 or self.pina_pt_position != 0) or (
                    average_ratio * (1 + self.close_epsilon) > ratio > average_ratio * (1 - self.close_epsilon)):
                self.in_pt = not self.in_pt
                if self.coconut_pt_position < 0 and self.pina_pt_position > 0:
                    # Buy back coconuts and sell back pinas
                    orders.append(Order(coconuts, min(coconuts_order_depth.sell_orders.keys()),
                                        -coconuts_position))
                    print("TRADING", -self.coconut_pt_position, coconuts, " at",
                          min(coconuts_order_depth.sell_orders.keys()))
                    result[coconuts] = orders

                    orders: list[Order] = []
                    orders.append(Order(pinas, max(pina_order_depth.buy_orders.keys()),
                                        -pinas_position))
                    print("TRADING", -self.pina_pt_position, pinas, " at",
                          max(pina_order_depth.buy_orders.keys()))
                    result[pinas] = orders
                elif self.coconut_pt_position > 0 and self.pina_pt_position < 0:
                    # Buy back pinas and buy back coconuts
                    orders.append(Order(pinas, min(pina_order_depth.sell_orders.keys()),
                                        -pinas_position))
                    print("TRADING", -self.pina_pt_position, pinas, " at",
                          min(pina_order_depth.sell_orders.keys()))
                    result[pinas] = orders

                    orders: list[Order] = []
                    orders.append(Order(coconuts, max(coconuts_order_depth.buy_orders.keys()),
                                        -coconuts_position))
                    print("TRADING", -self.coconut_pt_position, coconuts, " at",
                          max(coconuts_order_depth.sell_orders.keys()))
                    result[coconuts] = orders
        else:
            if ratio > average_ratio * (1 + self.open_epsilon):  # Buy coconuts, sell pinas
                self.in_pt = not self.in_pt
                new_orders, volume = buy_max(coconuts, coconuts_order_depth, coconuts_position_limit, coconuts_position, orders)
                orders = orders + new_orders
                result[coconuts] = orders
                orders: list[Order] = []
                self.coconut_pt_position = volume

                new_orders, volume = sell_max(pinas, pina_order_depth, pinas_position_limit, pinas_position, orders)
                orders = orders + new_orders
                result[pinas] = orders
                orders: list[Order] = []
                self.pina_pt_position = -volume
            elif ratio < average_ratio * (1 - self.open_epsilon):  # Buy pinas, sell coconuts
                self.in_pt = not self.in_pt
                new_orders, volume = buy_max(pinas, pina_order_depth, pinas_position_limit, pinas_position, orders)
                orders = orders + new_orders
                result[pinas] = orders
                orders: list[Order] = []
                self.pina_pt_position = volume

                new_orders, volume = sell_max(coconuts, coconuts_order_depth, coconuts_position_limit, coconuts_position, orders)
                orders = orders + new_orders
                result[coconuts] = orders
                orders: list[Order] = []
                self.coconut_pt_position = -volume

        return result


def sell_max(symbol, order_depth: OrderDepth, position_limit, current_position, orders: list[Order]):
    best_bid = max(order_depth.buy_orders.keys())
    total_volume = 0
    at_max = (total_volume == position_limit)
    while not at_max:
        if order_depth.buy_orders.get(best_bid) is None:
            break
        new_volume = min(order_depth.buy_orders.get(best_bid),
                         position_limit - current_position - total_volume)
        total_volume = total_volume + new_volume
        orders.append(Order(symbol, best_bid, -new_volume))
        print("SELL", -new_volume, symbol, " at", best_bid)
        best_bid = best_bid - 1
        at_max = (total_volume == position_limit)
    return orders, total_volume


def buy_max(symbol, order_depth: OrderDepth, position_limit, current_position, orders: list[Order]):
    best_ask = min(order_depth.sell_orders.keys())
    total_volume = 0
    at_max = (total_volume == position_limit)
    while not at_max:
        if order_depth.sell_orders.get(best_ask) is None:
            break
        new_volume = min(-order_depth.sell_orders.get(best_ask),
                         position_limit - current_position - total_volume)
        total_volume = total_volume + new_volume
        orders.append(Order(symbol, best_ask, new_volume))
        print("BUY", new_volume, symbol, " at", best_ask)
        best_ask = best_ask + 1
        at_max = (total_volume == position_limit)
    return orders, total_volume
