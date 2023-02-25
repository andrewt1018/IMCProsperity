from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.warmup_period = 500
        self.average = np.array([])
        self.symbol = 'PEARLS'

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        ready = False

        # Warmup period
        if state.timestamp < self.warmup_period:
            for product in state.order_depths.keys():
                if product == self.symbol:
                    self.average = np.append(self.average, min(state.order_depths[product].sell_orders.keys()))
        else:
            ready = True

        if ready:
            # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
            for product in state.order_depths.keys():
                if product == self.symbol:

                    # Initialize the list of Orders to be sent as an empty list
                    orders: list[Order] = []
                    order_depth: OrderDepth = state.order_depths[product]

                    current_price = min(order_depth.sell_orders.keys())
                    self.average[:-1] = self.average[1:]
                    self.average[-1] = current_price

                    sma = np.average(self.average)
                    print("New SMA: " + str(sma))

                    if sma < current_price:  # Buy if average is less than price
                        best_ask = max(order_depth.sell_orders.keys())
                        best_ask_volume = order_depth.sell_orders[best_ask]
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                    elif sma > current_price:  # Sell if average is more than price
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = order_depth.buy_orders[best_bid]
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, best_bid_volume))

                    result[product] = orders

        return result
