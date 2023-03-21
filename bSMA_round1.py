from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order



class Trader:
    def __init__(self):
        self.warmup_period = 500
        self.average = np.array([])
        self.resolution_counter = 0
        self.resolution = 500

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Simplified constants
        pearls_position_limit = 20
        bananas_position_limit = 20
        pearls = 'PEARLS'
        bananas = 'BANANAS'

        result = {}
        for product in state.order_depths.keys():
            # Initialize the list of Orders to be sent as an empty list
            # Initialize other variables used in this scope
            orders: list[Order] = []
            order_depth: OrderDepth = state.order_depths[product]
            bananas_position = state.position.get(bananas)
            pearls_position = state.position.get(pearls)
            if bananas_position is None:
                bananas_position = 0
            if pearls_position is None:
                pearls_position = 0

            if product == bananas:  # SMA for BANANAS
                if state.timestamp < self.warmup_period:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    self.average = np.append(self.average, min(state.order_depths[product].sell_orders.keys()))
                elif self.resolution_counter == self.resolution:  # Make market orders every 500 interval
                    current_price = min(order_depth.sell_orders.keys())
                    self.average[:-1] = self.average[1:]
                    self.average[-1] = current_price

                    sma = np.average(self.average)
                    print("New SMA: " + str(sma))

                    if sma < current_price:  # Buy if average is less than price
                        best_ask = min(order_depth.sell_orders.keys())
                        best_ask_volume = -order_depth.sell_orders[best_ask]
                        if bananas_position + best_ask_volume > pearls_position_limit:
                            best_ask_volume = pearls_position_limit - bananas_position  # Buy all position quota
                        print("BUY", str(best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, best_ask_volume))
                    elif sma >= current_price:  # Sell if average is more than price
                        best_bid = max(order_depth.buy_orders.keys())
                        best_bid_volume = -order_depth.buy_orders[best_bid]
                        if bananas_position + best_bid_volume < (-1) * pearls_position_limit:
                            best_bid_volume = (-1) * pearls_position_limit - bananas_position
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, best_bid_volume))

                    result[product] = orders
                else:  # Increment resolution counter and update self.average
                    self.resolution_counter = self.resolution_counter + 100
                    self.average[:-1] = self.average[1:]
                    self.average[-1] = min(state.order_depths[product].sell_orders.keys())
        return result
