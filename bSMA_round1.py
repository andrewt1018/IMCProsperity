from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.warmup_period = 1000
        self.average = np.array([])
        self.min_asks = np.array([])
        self.max_buys = np.array([])
        self.epsilon = 0.30
        self.max_lot_size = 10
        self.upwards = False
        self.profit = 0

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

        print("Positions: ", state.position)
        print("Own trades: ", state.own_trades)

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

        result = {}

        for product in state.order_depths.keys():
            # Initialize the list of Orders to be sent as an empty list
            # Initialize other variables used in this scope
            orders: list[Order] = []
            order_depth: OrderDepth = state.order_depths[product]

            if product == bananas:  # SMA for BANANAS
                if state.timestamp < self.warmup_period:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.average = np.append(self.average, mid_price)
                    # self.average = np.append(self.average, min(order_depth.sell_orders.keys()))
                    self.min_asks = np.append(self.min_asks, min(order_depth.sell_orders.keys()))
                    self.max_buys = np.append(self.max_buys, max(order_depth.buy_orders.keys()))
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    # current_price = min(order_depth.sell_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    average_range = (np.average(self.min_asks) + np.average(self.max_buys)) / 2.0
                    sma = np.average(self.average)
                    print("New SMA: ", str(sma))
                    print("Current price: ", current_price)

                    # Update SMA
                    self.average[:-1] = self.average[1:]
                    self.average[-1] = current_price
                    print("self.average: ", self.average)

                    if sma < max_buy:  # Indicating a downwards trend
                        if not self.upwards:  # Do not buy if progression is already downwards
                            continue
                        else:  # Sell because progression used to be downwards and now their is a shift
                            # if best_bid >= sma - self.epsilon * average_range:
                            best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                                  -bananas_position_limit - bananas_position,
                                                  -self.max_lot_size)
                            orders.append(Order(product, max_buy, best_bid_volume))
                            print("SELL", str(best_bid_volume) + "BANANAS", max_buy)
                            self.upwards = False
                    elif sma > min_ask:  # Indicating an upwards trend
                        if self.upwards:  # Do not buy if progression is already upwards
                            continue
                        else:
                            # if best_ask <= sma + self.epsilon * average_range:
                            best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                                  bananas_position_limit - bananas_position,
                                                  self.max_lot_size)
                            orders.append(Order(product, min_ask, best_ask_volume))
                            print("BUY ", str(best_ask_volume) + " BANANAS", min_ask)
                            self.upwards = True

                    result[product] = orders
        return result
