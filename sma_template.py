from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        # Variables for SMA
        self.warmup_period = 1000
        self.ukulele = np.array([])
        self.coco = np.array([])
        self.pinas = np.array([])
        self.berries = np.array([])
        self.diving = np.array([])
        self.ukulele = np.array([])
        self.ukulele = np.array([])
        self.ukulele = np.array([])
        self.ukulele = np.array([])
        self.max_lot_size = 10
        self.profit = 0

        # Variables for BLSH - PEARLS
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
        berries = 'BERRIES'
        diving = 'DIVING_GEAR'
        dip = 'DIP'
        ukulele = 'UKULELE'
        picnic = 'PICNIC_BASKET'
        bag = 'BAGUETTE'

        pearls_position_limit = 20
        ukulele_position_limit = 20
        coconuts_position_limit = 600
        pinas_position_limit = 300
        berries_position_limit = 250
        diving_position_limit = 50
        ukulele_position_limit = 300
        ukulele_position_limit = 150
        ukulele_position_limit = 70
        ukulele_position_limit = 70

        ukulele_position = state.position.get(bananas)
        pearls_position = state.position.get(pearls)
        coconuts_position = state.position.get(coconuts)
        pinas_position = state.position.get(pinas)
        berries_position = state.position.get(berries)
        diving_position = state.position.get(diving)
        ukulele_position = state.position.get(dip)
        ukulele_position = state.position.get(bag)
        ukulele_position = state.position.get(ukulele)
        ukulele_position = state.position.get(picnic)

        if ukulele_position is None:
            ukulele_position = 0
        if pearls_position is None:
            pearls_position = 0
        if coconuts_position is None:
            coconuts_position = 0
        if pinas_position is None:
            pinas_position = 0
        if berries_position is None:
            berries_position = 0
        if diving_position is None:
            diving_position = 0
        if ukulele_position is None:
            ukulele_position = 0
        if ukulele_position is None:
            ukulele_position = 0
        if ukulele_position is None:
            ukulele_position = 0
        if ukulele_position is None:
            ukulele_position = 0

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

            if product == ukulele:  # SMA for UKULELE
                if len(self.ukulele) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.ukulele = np.append(self.ukulele, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.ukulele[:-1] = self.ukulele[1:]
                    self.ukulele[-1] = current_price
                    # print("self.average: ", self.average)

                    sma = np.average(self.ukulele)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -ukulele_position_limit - ukulele_position,
                                              2)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              ukulele_position_limit - ukulele_position,
                                              -2)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders

        return result
