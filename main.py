from api import IdealistaClient, USER, PASSWORD
from builder import SearchFilterBuilder
from model import *

texto = '''
      ███       ████                       █████    ██               ███      ███ █████ ██████          
            ████                         ███                     ███            ███   ████          
█████   ████████   █████      █████      ███ █████    ███████ ████████ ██████   ███   ████   █████  
█████ ██████████ █████████    ███████    ███ █████  █████████  ███████ ██████   ███   ████ █████████
  ███ ███   ████ █████████    ███████    ███    ██  ███████      ███      ███   ███   ████ ███   ███
  ███ ███   ████ █████████    ███████    ███    ██    █████      ███      ███   ███   ████ ███   ███
  ███ ███   ████ ███        ███   ███    ███    ██        ███    ███      ███   ███   ████ ███   ███
  ███   ████████   █████      ███████    ███    ██  ███████        ███    ███   ███   ████   █████  '''

print(texto)

ic = IdealistaClient()
s = ic.start()
e = ic.exists(USER)
if e:
    l = ic.login(USER, PASSWORD)
    builder = SearchFilterBuilder().set_operation(Operation.RENT).set_property_type(PropertyType.HOMES).set_price_range(0,
                                                                                                                     1500).set_location_id(
        "0-EU-ES-28-07-001-079").set_location_name("Madrid, Madrid")
    element_list = []
    i = 1
    total_pages = 1
    while True:
        builder = builder.set_num_page(i)
        s = ic.search(builder.build())
        data = s.json()

        if i == 1:
            total_pages = data['totalPages']

        element_list.extend(data['elementList'])

        print(f"Page {i}/{total_pages}")
        if i >= total_pages:
            break

        i += 1

    # Example
    # print propertyCode, price, size, operation, address, rooms, bathrooms, neighborhood + district + municipality
    print('| Property Code | Price | Size | Operation | Address | Rooms | Bathrooms | Neighborhood, District, Municipality |')
    for element in element_list:
        print(f"| {element.get('propertyCode')} | {element.get('price')} | {element.get('size')} | {element.get('operation')} | {element.get('address')} | {element.get('rooms')} | {element.get('bathrooms')} | {element.get('neighborhood')}, {element.get('district')}, {element.get('municipality')} |")