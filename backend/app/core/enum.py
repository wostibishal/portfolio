from enum import Enum

class Role(str, Enum):
    SUPER = "super",
    RETAILER = "retailer",
    COSTUMER = "costumer",


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"