from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        # Variables for SMA - BANANAS
        self.warmup_period = 1000
        self.average = np.array([])
        self.max_lot_size = 10
        self.profit = 0

        self.coconut_average = np.array([])
        self.coconut_max_lot_size = 300
        self.coconut_profit = 0

        self.pina_average = np.array([])
        self.pina_max_lot_size = 150
        self.pina_profit = 0
        # Variables for BLSH - PEARLS
        self.pmax = -1
        self.pmin = float('inf')
        self.price_range = 0
        self.epsilon = 0.4
        self.mid_range = [float('inf'), -1]
        self.mid_prices = []
        self.mid_prices_length = 20
        self.quantity = 3

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
        coconuts_position = state.position.get(coconuts)
        pinas_position = state.position.get(pinas)

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
        print("Own trades: ", state.own_trades)

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
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.average[:-1] = self.average[1:]
                    self.average[-1] = current_price
                    print("self.average: ", self.average)

                    sma = np.average(self.average)

                    if sma < max_buy:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -bananas_position_limit - bananas_position,
                                              -self.max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("SELL", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > min_ask:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              bananas_position_limit - bananas_position,
                                              self.max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("BUY ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders

            if product == coconuts:  # SMA for COCONUTS
                if state.timestamp < self.warmup_period:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.coconut_average = np.append(self.coconut_average, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.coconut_average[:-1] = self.coconut_average[1:]
                    self.coconut_average[-1] = current_price
                    print("self.average: ", self.coconut_average)

                    sma = np.average(self.coconut_average)

                    if sma < max_buy:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -coconuts_position_limit - coconuts_position,
                                              -self.coconut_max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("SELL", str(best_bid_volume) + "COCONUTS", max_buy)
                    elif sma > min_ask:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              coconuts_position_limit - coconuts_position,
                                              self.coconut_max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("BUY ", str(best_ask_volume) + " COCONUTS", min_ask)
                    result[product] = orders

            if product == pinas:  # SMA for PINAS
                if state.timestamp < self.warmup_period:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.pinas_average = np.append(self.pinas_average, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.pinas_average[:-1] = self.pinas_average[1:]
                    self.pinas_average[-1] = current_price
                    print("self.average: ", self.average)

                    sma = np.average(self.pinas_average)

                    if sma < max_buy:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -pinas_position_limit - pinas_position,
                                              -self.pina_max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("SELL", str(best_bid_volume) + "PINAS", max_buy)
                    elif sma > min_ask:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              pinas_position_limit - pinas_position,
                                              self.pina_max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("BUY ", str(best_ask_volume) + " PINAS", min_ask)
                    result[product] = orders

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