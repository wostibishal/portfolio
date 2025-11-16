from enum import Enum

class Role(str, Enum):
    SUPER = "super"
    RETAILER = "retailer"
    COSTUMER = "costumer"
