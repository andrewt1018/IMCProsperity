from typing import Dict, List
import numpy as np
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.iter = 0
        self.profit = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        self.iter = self.iter + 1
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
            orders: list[Order] = []
            order_depth: OrderDepth = state.order_depths[product]

            at_max = (bananas_position == -bananas_position_limit)
            if product == bananas:
                if not at_max:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = min(order_depth.buy_orders.get(best_bid),
                                          bananas_position_limit + bananas_position)
                    orders.append(Order(product, best_bid, -best_bid_volume))
                    print("SELL", str(best_bid_volume) + "BANANAS", best_bid)
                    at_max = (bananas_position - best_bid_volume == -bananas_position_limit)
                    force_quit = 0
                    while not at_max:
                        force_quit = force_quit + 1
                        if force_quit == 15:
                            print("Maximum amount not sold")
                            break
                        best_bid = best_bid - 1
                        new_volume = min(order_depth.buy_orders.get(best_bid),
                                         bananas_position_limit + bananas_position - best_bid_volume)
                        orders.append(Order(product, best_bid, -new_volume))
                        best_bid_volume = best_bid_volume + new_volume
                        print("SELL", str(new_volume) + "BANANAS", best_bid)
                        at_max = (bananas_position - best_bid_volume == -bananas_position_limit)

                    result[product] = orders

                if self.iter == 999 or self.iter == 1000:  # Final iteration, bananas_position should be -20
                    best_ask = min(order_depth.sell_orders.keys()) - 1
                    best_ask_volume = 0
                    closed = (bananas_position == 0)
                    force_quit = 0
                    while not closed:
                        force_quit = force_quit + 1
                        if force_quit == 15:
                            print("Maximum amount not bought")
                            break
                        best_ask = best_ask + 1
                        new_volume = min(order_depth.sell_orders.get(best_ask), -(bananas_position + best_ask_volume))
                        orders.append(Order(product, best_ask, new_volume))
                        best_ask_volume = best_ask_volume + new_volume
                        print("BUY", str(new_volume) + "BANANAS", best_ask)
                        closed = (bananas_position + best_ask_volume == 0)
        return result
