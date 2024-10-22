from typing import List, Tuple
from Order import Order
from Customer import Customer
from models.Item import Product
from datetime import datetime, timedelta


class Report:
    
    def __init__(self, orders: List[Order], customers: List[Customer], products: List[Product]) -> None:
        """
        Initialize the Report class with lists of orders, customers, and products.
        :param orders: List of orders placed by customers.
        :param customers: List of all customers (private and corporate).
        :param products: List of available products.
        """
        self.__orders = orders
        self.__customers = customers
        self.__products = products


    def __is_in_timeframe(self, order: Order, timeframe: str) -> bool:
        """
        Check if the order is in the given timeframe.
        :param order: The order to check.
        :param timeframe: The timeframe ('week', 'month', 'year').
        :return: True if the order is within the timeframe, False otherwise.
        """
        now = datetime.now()
        if timeframe == 'week':
            return order.order_date >= now - timedelta(weeks=1)
        elif timeframe == 'month':
            return order.order_date >= now - timedelta(days=30)
        elif timeframe == 'year':
            return order.order_date >= now - timedelta(days=365)
        return False

    def get_sales_report(self, timeframe: str) -> float:
        """
        Calculate total sales for the given timeframe (week, month, year).
        :param timeframe: The time range for the sales report.
        :return: Total sales amount.
        """
        total_sales = 0.0
        for order in self.__orders:
          
            if self.__is_in_timeframe(order, timeframe):
                total_sales += order.total_amount
        return total_sales

    def list_customers(self) -> Tuple[List[Customer], List[Customer]]:
        """
        List private and corporate customers.
        :return: A tuple containing two lists (private customers, corporate customers).
        """
        private_customers = [cust for cust in self.__customers if cust.is_private()]
        corporate_customers = [cust for cust in self.__customers if cust.is_corporate()]
        return private_customers, corporate_customers

    def popular_items(self) -> Tuple[Product, Product]:
        """
        Identify the most and least popular items.
        :return: A tuple with the most popular product and the unpopular product.
        """
        product_popularity = {product: 0 for product in self.__products}
        
        for order in self.__orders:
            for product, quantity in order.items:
                product_popularity[product] += quantity
        
        most_popular = max(product_popularity, key=product_popularity.get)
        unpopular = min(product_popularity, key=product_popularity.get)
        
        return most_popular, unpopular

    
