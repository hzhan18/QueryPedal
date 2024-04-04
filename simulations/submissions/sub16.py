from dataclasses import dataclass
from bakery import assert_equal

@dataclass
class Grocery:
    item: str
    cost: int
    on_sale: bool
    
total = [Grocery("g", 5, True),
         Grocery("g", 10, True),
         Grocery("g", 3, True)]    
    
def sum_groceries(b:list[Grocery])-> int:
    count = 0
    for c in b:
        count += c.cost
assert_equal(sum_groceries(total), 18)
