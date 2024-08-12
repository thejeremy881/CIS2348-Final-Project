"""
Name: Jeremy Duong
Student ID: 2141236
"""

import csv
from datetime import datetime


# Defining InventoryItem class to represent a single item in the electronics inventory
class InventoryItem:
    def __init__(self, item_id, manufacturer_name, item_type, item_price, service_date, damaged_item=False):
      
        """
        Initializes an an electronic inventory item object with attributes like item id, manufacturer name, item type,
        item price, service date (which is converted to a datetime object using strptime()), and damage indicator.
        """
        self.item_id = item_id
        self.manufacturer_name = manufacturer_name
        self.item_type = item_type
        self.item_price = item_price
        self.service_date = datetime.strptime(service_date, '%m/%d/%Y')
        self.damaged_item = damaged_item

    def __repr__(self):

        """
        Provides useful string representation of the inventory items when debugging
        """
        return f'Inventory Item({self.item_id}, {self.manufacturer_name}, {self.item_type}, {self.item_price}, {self.service_date.date()}, {self.damaged_item})'


# Defining Inventory class to represent a collection of the electronic inventory item objects  
class Inventory:
    def __init__(self):
        self.items = []  # a list that stores all the electronic inventory items

    def load_inventory_data(self, manufacturer_file, price_file, serviceDate_file):
        
        """
        The data from the input CSV files is loaded, InventoryItem class objects created, and stored in the inventory items list.
        The manufacturer name, item type, item price, service date, damage indicator information is read and InventoryItem objects are thyen appended to the item list.
        """
        itemManufacturer_data = self.read_csv_file(manufacturer_file)
        itemPrice_data = self.read_csv_file(price_file)
        service_date_data = self.read_csv_file(serviceDate_file)

        for item_id in itemManufacturer_data:
            manufacturer_info = itemManufacturer_data[item_id]
            price_info = itemPrice_data.get(item_id, ['0'])
            service_date_info = service_date_data.get(item_id, None)
            damaged_electronic = len(manufacturer_info) > 3 and manufacturer_info[3].lower() == 'damaged'

            item = InventoryItem(item_id, manufacturer_info[1].strip(), manufacturer_info[2].strip(), price_info[1], service_date_info[1], damaged_electronic)
            self.items.append(item)

            # Debugging to check data is added correctly
            print(f"Added item successfully: {item}")

    def read_csv_file(self, file_name, key_index=0):

        """
        Input CSV files are read and the electronic inventory information is stored in a dictionary, where the key is the key_index
        and the value is the entire row specified by a list.
        """
        inventory_data = {}
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                key = row[key_index]
                inventory_data[key] = row
        return inventory_data
    
    def write_to_csv(self, file_name, items, attributes):

        """
        Writes/Outputs the electronics inventory data to a CSV file
        """
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            for item in items:
                row = [getattr(item, attr) if attr != 'service_date' else getattr(item, attr).strftime('%m/%d/%Y') for attr in attributes]
                writer.writerow(row)

            # Debugging to confirm data is outputted in the correct format to the output files
            print(f"Data written successfully to {file_name}")
    
    def full_inventory_report(self, output_file):

        """
        A full electronics inventory report is generated by sorting items by manufacturer name and writing the report to a CSV file.
        """
        sorted_inventory = sorted(self.items, key=lambda x: x.manufacturer_name)
        self.write_to_csv(output_file, sorted_inventory, ['item_id', 'manufacturer_name', 'item_type', 'item_price', 'service_date', 'damaged_item'])

    def item_type_inventory_report(self):

        """
        An inventory report by item type is generated and each report is written to a separate CSV file.
        """
        electronic_item_types = set(item.item_type for item in self.items)
        for electronic_item in electronic_item_types:
            eligible_items = [item for item in self.items if item.item_type == electronic_item]
            sorted_inventory = sorted(eligible_items, key=lambda x: x.item_id)
            self.write_to_csv(f'{electronic_item}Inventory.csv', sorted_inventory, ['item_id', 'manufacturer_name', 'item_type', 'item_price', 'service_date', 'damaged_item'])

    def past_service_inventory_report(self, output_file):

        """
        A report of items whose service dates have passed is generated and report is sorted by the service date,
        and then written to a CSV file.
        """
        current_service_date = datetime.now()
        eligible_items = [item for item in self.items if item.service_date < current_service_date]
        sorted_inventory = sorted(eligible_items, key=lambda x:x.service_date)
        self.write_to_csv(output_file, sorted_inventory, ['item_id', 'manufacturer_name', 'item_type', 'item_price', 'service_date', 'damaged_item'])

    def damaged_inventory_report(self, output_file):

        """
        A report of all damaged electronic items is generated and is sorted by price in descending order,
        and then written to a CSV file.
        """
        eligible_items = [item for item in self.items if item.damaged_item]
        sorted_inventory = sorted(eligible_items, key=lambda x:x.item_price, reverse=True)
        self.write_to_csv(output_file, sorted_inventory, ['item_id', 'manufacturer_name', 'item_type', 'item_price', 'service_date'])

#Testing
def main():

    electronic_inventory = Inventory()
    electronic_inventory.load_inventory_data('ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv')
    electronic_inventory.full_inventory_report('FullInventory.csv')
    electronic_inventory.item_type_inventory_report()
    electronic_inventory.past_service_inventory_report('PastServiceDateInventory.csv')
    electronic_inventory.damaged_inventory_report('DamagedInventory.csv')

if __name__ == "__main__":
    main()

