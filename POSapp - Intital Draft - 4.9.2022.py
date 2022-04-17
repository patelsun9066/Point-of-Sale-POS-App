import datetime
from datetime import date


class InventoryItem:

    def __init__(self, item_name, item_category, item_price, unit_cost, selling_price, inventory_item_number):
        # Private data members that will be initialized upon new inventory item entry from user
        self._item_name = item_name
        self._item_category = item_category
        self._item_price = item_price
        self._unit_cost = unit_cost
        self._selling_price = selling_price
        self._inventory_item_number = inventory_item_number
        # Private data members for system tracking
        self._sales_tax = 0.07
        self._gross_margin = self._selling_price - self._unit_cost
        self._quantity = 0
        self._initial_date_created = ""

    def get_item_name(self):
        return self._item_name

    def get_item_price(self):
        return self._item_price

    def get_unit_cost(self):
        return self._unit_cost

    def get_selling_price(self):
        return self._selling_price

    def get_inventory_item_number(self):
        return self._inventory_item_number

    def get_quantity(self):
        return self._quantity

    def set_quantity(self, quantity_change):
        self._quantity += quantity_change

    def set_initial_date_created(self, date_created):
        self._initial_date_created = date_created


class InventoryTracking:

    def __init__(self):
        self._inventory_stock_amount = {}
        self._inventory_items = {}
        self._inventory_expiration_dates = {}

    def add_inventory_item(self, item_name, item_category, item_price, unit_cost, selling_price, inventory_item_number):

        new_inventory_item_object = InventoryItem(item_name, item_category, item_price, unit_cost, selling_price,
                                                  inventory_item_number)
        new_inventory_item_number = new_inventory_item_object.get_inventory_item_number()
        today = date.today()
        today_string = today.strftime("%m/%d/%y")
        new_inventory_item_object.set_initial_date_created(today_string)

        for items in self._inventory_items:
            if inventory_item_number in items:
                return False

        self._inventory_items[new_inventory_item_number] = new_inventory_item_object

        return True

    def inventory_stock_additions(self, addition_date, transaction_id, inventory_item_number, quantity):

        year = int(addition_date[5:9])
        day = int(addition_date[2:4])
        month = int(addition_date[0])
        converted_addition_date = datetime.datetime(year, month, day)

        new_addition = [converted_addition_date, transaction_id, quantity]
        inventory_item_object = ""

        for items in self._inventory_items:
            if inventory_item_number in items:
                if inventory_item_number not in self._inventory_stock_amount:
                    self._inventory_stock_amount[inventory_item_number] = [new_addition]
                    inventory_item_object = self._inventory_items[items]
                else:
                    self._inventory_stock_amount[items].append(new_addition)
                    inventory_item_object = self._inventory_items[items]

        inventory_item_object.set_quantity(quantity)

        return True

    def inventory_stock_decreases(self, deduction_date, transaction_id, inventory_item_number, quantity):

        negative_quantity = -quantity
        year = int(deduction_date[5:9])
        day = int(deduction_date[2:4])
        month = int(deduction_date[0])
        converted_deduction_date = datetime.datetime(year, month, day)

        new_deduction = [converted_deduction_date, transaction_id, negative_quantity]
        inventory_item_object = ""

        for items in self._inventory_items:
            if inventory_item_number in items:
                if inventory_item_number not in self._inventory_stock_amount:
                    self._inventory_stock_amount[inventory_item_number] = [new_deduction]
                    inventory_item_object = self._inventory_items[items]
                else:
                    self._inventory_stock_amount[items].append(new_deduction)
                    inventory_item_object = self._inventory_items[items]

        inventory_item_object.set_quantity(negative_quantity)

        return True

    def expiration_date(self, transaction_id, expiration_date):

        year = int(expiration_date[5:9])
        day = int(expiration_date[2:4])
        month = int(expiration_date[0])
        converted_expiration_date = datetime.datetime(year, month, day)

        transaction_for_date = {}

        for items in self._inventory_stock_amount:
            for lists in self._inventory_stock_amount[items]:
                if transaction_id in lists:
                    if transaction_id not in transaction_for_date:
                        transaction_for_date[items] = lists
                    else:
                        transaction_for_date[items].append(lists)

        for values in transaction_for_date.values():
            self._inventory_expiration_dates[values[1]] = converted_expiration_date

        print(self._inventory_expiration_dates)

        return True

    def expiration_date_approaching_alert(self, today_date):

        year = int(today_date[5:9])
        day = int(today_date[2:4])
        month = int(today_date[0])
        converted_today_date = datetime.datetime(year, month, day)

        expiration_approaching = {}

        for transactions in self._inventory_expiration_dates:
            if converted_today_date >= self._inventory_expiration_dates[transactions]:
                expiration_approaching[transactions] = self._inventory_expiration_dates[transactions]

        return expiration_approaching

    def shelf_life_remaining(self, current_date):

        year = int(current_date[5:9])
        day = int(current_date[2:4])
        month = int(current_date[0])
        converted_current_date = datetime.datetime(year, month, day)

        shelf_life_remaining_dic = {}

        expiration_date = 0

        for transactions in self._inventory_expiration_dates:
            expiration_date = self._inventory_expiration_dates[transactions]
            shelf_life_remaining = expiration_date - converted_current_date
            shelf_life_remaining_dic[transactions] = shelf_life_remaining

        return shelf_life_remaining_dic














    def get_inventory_stock(self):
        return self._inventory_stock_amount

    def get_inventory_items(self):
        return self._inventory_items

    def get_inventory_expirations_date(self):
        return self._inventory_expiration_dates














new_inventory = InventoryTracking()
new_inventory.add_inventory_item("cat food", "pet food", 4.99, 2.99, 6.99, "N1009")
print(new_inventory.add_inventory_item("cat food", "pet food", 4.99, 2.99, 6.99, "N1009"))
print(new_inventory.inventory_stock_additions("4/15/2022", "123", "N1009", 10))
print(new_inventory.inventory_stock_additions("4/15/2022", "245", "N1009", 10))
print(new_inventory.inventory_stock_decreases("4/15/2022", "789", "N1009", 10))
print(new_inventory.get_inventory_stock())
print(new_inventory.get_inventory_items())
print(new_inventory.expiration_date("123", "4/15/2022"))
print(new_inventory.expiration_date_approaching_alert("4/17/2022"))
print(new_inventory.shelf_life_remaining("4/17/2022"))