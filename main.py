import json

from api import IdealistaClient, USER, PASSWORD
from builder import SearchFilterBuilder
from model import *
from service import IdealistaService

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
ic = IdealistaService()
s = ic.start()
e = ic.exists(USER)

if e:
    l = ic.login(USER, PASSWORD)

    # load sample_shapes/downtown_madrid.json
    with open('sample_shapes/downtown_madrid.json') as f:
        shape = json.load(f)

    builder = (SearchFilterBuilder()
               .set_operation(Operation.RENT)
               .set_property_type(PropertyType.HOMES)
               .set_price_range(0, 1500)
               .set_shape_from_json(shape))
    for result in ic.search_with_paginated_results(builder):
        pass
