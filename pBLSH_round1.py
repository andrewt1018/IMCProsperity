from typing import Dict, List

import numpy as np

from datamodel import OrderDepth, TradingState, Order

class Trader:
    def __init__(self):
        self.pmax = -1
        self.pmin = float('inf')
        self.price_range = 0
        self.epsilon = 0.4
        self.mid_range = [float('inf'), -1]
        self.mid_prices = []
        self.mid_prices_length = 20
        self.quantity = 3

        self.profit = 0

    ## Simple buy low sell high algorithm for trading pearls
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        pearls = 'PEARLS'
        bananas = 'BANANAS'
        pearls_position_limit = 20
        bananas_position_limit = 20

        bananas_position = state.position.get(bananas)
        pearls_position = state.position.get(pearls)
        if bananas_position is None:
            bananas_position = 0
        if pearls_position is None:
            pearls_position = 0

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
        print("Own trades: ", state.own_trades)

        result = {}

        for product in state.order_depths.keys():
            # Initialize the list of Orders to be sent as an empty list
            # Initialize other variables used in this scope
            orders: list[Order] = []
            order_depth: OrderDepth = state.order_depths[product]

            if product == pearls:
                max_ask = max(order_depth.sell_orders.keys())
                min_buy = min(order_depth.buy_orders.keys())
                min_ask = min(order_depth.sell_orders.keys())
                max_buy = max(order_depth.buy_orders.keys())
                mid_price = (max_buy + min_ask) / 2.0
                if len(self.mid_prices) < self.mid_prices_length:
                    self.mid_prices.append(mid_price)
                else:
                    self.mid_prices[:-1] = self.mid_prices[1:]
                    self.mid_prices[-1] = mid_price

                average = np.average(self.mid_prices)
                if mid_price < self.mid_range[0]:
                    self.mid_range[0] = mid_price
                if mid_price > self.mid_range[1]:
                    self.mid_range[1] = mid_price
                self.price_range = self.mid_range[1] - self.mid_range[0]
                if self.price_range == 0:
                    continue

                print("Mid_range: ", self.mid_range)
                print("Mid_price: ", mid_price)

                # If there is a significant shift upwards in the mid_price equivalent to
                # or more than 50% of range, then SELL the maximum buy order
                if max_buy >= average:
                    sell_quantity = max(-order_depth.buy_orders.get(max_buy),
                                        (-1) * pearls_position_limit - pearls_position)
                    # sell_quantity = -self.quantity
                    orders.append(Order(product, max_buy, sell_quantity))
                    # orders.append(Order(product, round(mid_price), sell_quantity))
                    print("SELL ", str(sell_quantity) + " PEARLS", max_buy)
                    # print("SELL ", str(sell_quantity) + " PEARLS", round(mid_price))
                    result[product] = orders

                if min_ask <= average:
                    buy_quantity = min(-order_depth.sell_orders.get(min_ask), pearls_position_limit - pearls_position)  # Signed buy quantity
                    # buy_quantity = self.quantity
                    orders.append(Order(product, min_ask, buy_quantity))
                    # orders.append(Order(product, round(mid_price), buy_quantity))
                    print("BUY ", str(buy_quantity) + " PEARLS", min_ask)
                    # print("BUY ", str(buy_quantity) + " PEARLS", round(mid_price))
                    result[product] = orders

        return result

