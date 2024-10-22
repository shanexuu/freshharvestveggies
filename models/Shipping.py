class Shipping:
    def __init__(self, delivery: bool, delivery_address: str = '', delivery_fee: float = 10.0) -> None:
        """
        Initialize the shipping details.
        :param delivery: Whether the order is for delivery or pick-up
        :param delivery_address: The address for delivery (if applicable)
        :param delivery_fee: The fee for delivery (default $10.00)
        """
        self.__delivery = delivery
        self.__delivery_address = delivery_address
        self.__delivery_fee = delivery_fee if delivery else 0.0
        # Status could be 'Pending', 'In Transit', 'Delivered', etc.
        self.__status = "Pending"  
        

    @property
    def delivery(self) -> bool:
        return self.__delivery

    @property
    def delivery_address(self) -> str:
        return self.__delivery_address

    @property
    def delivery_fee(self) -> float:
        return self.__delivery_fee

    @property
    def status(self) -> str:
        return self.__status

    def update_status(self, new_status: str) -> None:
        """
        Update the shipping status.
        :param new_status: The new status of the shipping
        """
        self.__status = new_status

    def get_shipping_details(self) -> str:
        """
        Get a summary of the shipping details.
        :return: A string with the shipping details.
        """
        if self.__delivery:
            return f"Delivery to: {self.__delivery_address}, Fee: {self.__delivery_fee}, Status: {self.__status}"
        else:
            return "Order will be collected in person."
