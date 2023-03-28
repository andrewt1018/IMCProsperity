from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        # Variables for SMA
        self.warmup_period = 1000
        self.average = np.array([])
        self.coco = np.array([])
        self.pinas = np.array([])
        self.berries = np.array([])
        self.diving = np.array([])
        self.dip = np.array([])
        self.ukulele = np.array([])
        self.picnic = np.array([])
        self.bag = np.array([])
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
        bananas_position_limit = 20
        coconuts_position_limit = 600
        pinas_position_limit = 300
        berries_position_limit = 250
        diving_position_limit = 50
        dip_position_limit = 300
        bag_position_limit = 150
        ukulele_position_limit = 70
        picnic_position_limit = 70

        bananas_position = state.position.get(bananas)
        pearls_position = state.position.get(pearls)
        coconuts_position = state.position.get(coconuts)
        pinas_position = state.position.get(pinas)
        berries_position = state.position.get(berries)
        diving_position = state.position.get(diving)
        dip_position = state.position.get(dip)
        bag_position = state.position.get(bag)
        ukulele_position = state.position.get(ukulele)
        picnic_position = state.position.get(picnic)

        if bananas_position is None:
            bananas_position = 0
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
        if dip_position is None:
            dip_position = 0
        if bag_position is None:
            bag_position = 0
        if ukulele_position is None:
            ukulele_position = 0
        if picnic_position is None:
            picnic_position = 0

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

            if product == picnic:  # SMA for PICNIC_BASKET
                if len(self.picnic) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.picnic = np.append(self.picnic, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.picnic[:-1] = self.picnic[1:]
                    self.picnic[-1] = current_price
                    # print("self.average: ", self.average)

                    sma = np.average(self.picnic)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -picnic_position_limit - picnic_position,
                                              2)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              picnic_position_limit - picnic_position,
                                              -2)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders

            if product == bag:  # SMA for BAGUETTE
                if len(self.bag) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.bag = np.append(self.bag, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.bag[:-1] = self.bag[1:]
                    self.bag[-1] = current_price
                    # print("self.average: ", self.average)

                    sma = np.average(self.bag)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -bag_position_limit - bag_position,
                                              2)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              bag_position_limit - bag_position,
                                              -2)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders

            if product == dip:  # SMA for DIP
                if len(self.dip) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.dip = np.append(self.dip, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.dip[:-1] = self.dip[1:]
                    self.dip[-1] = current_price
                    # print("self.average: ", self.average)

                    sma = np.average(self.dip)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -dip_position_limit - dip_position,
                                              2)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              dip_position_limit - dip_position,
                                              -2)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders

            if product == bananas:  # SMA for BANANAS
                if len(self.average) < self.warmup_period / 100:
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
                    # print("self.average: ", self.average)

                    sma = np.average(self.average)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -bananas_position_limit - bananas_position,
                                              2)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BANANAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              bananas_position_limit - bananas_position,
                                              -2)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " BANANAS", min_ask)
                    result[product] = orders
            
            if product == coconuts:  # SMA for COCONUTS
                if len(self.coco) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.coco = np.append(self.coco, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.coco[:-1] = self.coco[1:]
                    self.coco[-1] = current_price
                    # print("self.coco: ", self.coco)

                    sma = np.average(self.coco)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -coconuts_position_limit - coconuts_position,
                                              self.max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "COCONUTS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              coconuts_position_limit - coconuts_position,
                                              -self.max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " COCONUTS", min_ask)
                    result[product] = orders

            if product == pinas:  # SMA for BANANAS
                if len(self.pinas) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.pinas = np.append(self.pinas, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.pinas[:-1] = self.pinas[1:]
                    self.pinas[-1] = current_price
                    # print("self.pinas: ", self.pinas)

                    sma = np.average(self.pinas)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -pinas_position_limit - pinas_position,
                                              self.max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "PINAS", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              pinas_position_limit - pinas_position,
                                              -self.max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " PINAS", min_ask)
                    result[product] = orders
            
            if product == berries:  # SMA for berries
                if len(self.berries) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.berries = np.append(self.berries, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.berries[:-1] = self.berries[1:]
                    self.berries[-1] = current_price
                    # print("self.pinas: ", self.pinas)

                    sma = np.average(self.pinas)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -berries_position_limit - berries_position,
                                              self.max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "BERRIES", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              berries_position_limit - berries_position,
                                              -self.max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + "BERRIES", min_ask)
                    result[product] = orders

            if product == diving:  # SMA for BANANAS
                if len(self.diving) < self.warmup_period / 100:
                    # Update the new SMA by treating the 'average' numpy array as a queue (FIFO)
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys())) / 2.0
                    self.diving = np.append(self.diving, mid_price)
                else:
                    min_ask = min(order_depth.sell_orders.keys())
                    max_buy = max(order_depth.buy_orders.keys())
                    current_price = (min_ask + max_buy) / 2.0
                    # Update SMA
                    self.diving[:-1] = self.diving[1:]
                    self.diving[-1] = current_price
                    # print("self.diving: ", self.diving)

                    sma = np.average(self.diving)

                    if sma < current_price:  # Indicating a downwards trend
                        # if best_bid >= sma - self.epsilon * average_range:
                        best_bid_volume = max(-order_depth.buy_orders[max_buy],
                                              -diving_position_limit - diving_position,
                                              self.max_lot_size)
                        orders.append(Order(product, max_buy, best_bid_volume))
                        print("BUY", str(best_bid_volume) + "DIVING", max_buy)
                    elif sma > current_price:  # Indicating an upwards trend
                        # if best_ask <= sma + self.epsilon * average_range:
                        best_ask_volume = min(-order_depth.sell_orders[min_ask],
                                              diving_position_limit - diving_position,
                                              -self.max_lot_size)
                        orders.append(Order(product, min_ask, best_ask_volume))
                        print("SELL ", str(best_ask_volume) + " DIVING", min_ask)
                    result[product] = orders

            if product == pearls:
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

                # print("Mid_range: ", self.mid_range)
                # print("Mid_price: ", mid_price)

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
                    buy_quantity = min(-order_depth.sell_orders.get(min_ask),
                                       pearls_position_limit - pearls_position)  # Signed buy quantity
                    # buy_quantity = self.quantity
                    orders.append(Order(product, min_ask, buy_quantity))
                    # orders.append(Order(product, round(mid_price), buy_quantity))
                    print("BUY ", str(buy_quantity) + " PEARLS", min_ask)
                    # print("BUY ", str(buy_quantity) + " PEARLS", round(mid_price))
                    result[product] = orders

        return result
