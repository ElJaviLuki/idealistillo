import json

from api import IdealistaClient, USER, PASSWORD
from builder import SearchFilterBuilder
from data_cleaning import clean_data
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
               .set_shape_from_json(shape))
    pr = [result for result in ic.search_with_paginated_results(builder)]
    result = clean_data(pr)
    result['properties'].to_csv('properties.csv', index=False)
    result['videos'].to_csv('videos.csv', index=False)
    result['images'].to_csv('images.csv', index=False)
    result['virtual3DTours'].to_csv('virtual3DTours.csv', index=False)
    result['agencies'].to_csv('agencies.csv', index=False)
    print(pr)
