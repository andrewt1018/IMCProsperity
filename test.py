from typing import Dict, List

import numpy as np

from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.pmax = -1
        self.pmin = float('inf')
        self.price_range = 0
        self.epsilon = 0.50
        self.mid_range = [float('inf'), -1]

    ## Simple buy low sell high algorithm for trading pearls
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        pearls_position_limit = 20
        bananas_position_limit = 20

        pearls = 'PEARLS'
        bananas = 'BANANAS'

        result = {}
        print("Position: ", state.position)
        print("Observations: ", state.observations)
        for product in state.order_depths.keys():
            order_depth: OrderDepth = state.order_depths[product]
            max_buy = min(order_depth.buy_orders.keys())
            orders: list[Order] = []
            orders.append(Order(product, max_buy, 1))
            result[product] = orders
        return result