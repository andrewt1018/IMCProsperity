from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        # Variables for SMA - BANANAS
        self.warmup_period = 500
        self.average = np.array([])
        self.resolution_counter = 0
        self.resolution = 500

        # Variables for BLSH - PEARLS
        self.pmax = -1
        self.pmin = float('inf')
        self.price_range = 0
        self.epsilon = 0.50

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
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
            elif product == pearls:
                min_ask = max(order_depth.sell_orders.keys())
                max_buy = min(order_depth.buy_orders.keys())
                mid_price = (max_buy + min_ask) / 2.0
                if mid_price > self.pmax:
                    self.pmax = mid_price
                if mid_price < self.pmin:
                    self.pmin = mid_price
                self.price_range = self.pmax - self.pmin

                # If current mid_price is within 10% of the range from the max, then sell everything
                if self.pmax + self.epsilon * self.price_range > mid_price > self.pmax - self.epsilon * self.price_range:
                    sell_quantity = (-1) * pearls_position_limit - pearls_position  # Signed sell quantity
                    min_sell_price = min(order_depth.sell_orders.keys())
                    orders.append(Order(product, min_sell_price, sell_quantity))
                    result[product] = orders

                if self.pmin + self.epsilon * self.price_range > mid_price > self.pmin - self.epsilon * self.price_range:
                    buy_quantity = pearls_position_limit - pearls_position  # Signed buy quantity
                    max_buy_price = max(order_depth.buy_orders.keys())
                    orders.append(Order(product, max_buy_price, buy_quantity))
                    result[product] = orders

        return result
