from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.pmax = -1
        self.pmin = float('inf')
        self.price_range = 0
        self.epsilon = 0.50

    ## Simple buy low sell high algorithm for trading pearls
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

            if product == pearls:
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
                    buy_quantity = pearls_position_limit - pearls_position # Signed buy quantity
                    max_buy_price = max(order_depth.buy_orders.keys())
                    orders.append(Order(product, max_buy_price, buy_quantity))
                    result[product] = orders

        return result

