"""
Usage:
    python gen-oneof.py [OBJECT-NAMES-TO-BE-CONVERTED]
"""
import ruamel.yaml
import sys
from ruamel.yaml.comments import CommentedMap as OrderedDict

yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open('openapi.yaml') as fp:
    data = yaml.load(fp)
    objects = sys.argv[1].split(',')

for object in objects:
    if object not in data['components']['schemas']:
        print(object + " object is not present in components schemas of the OpenAPI Specification.")
        continue

    oldProps = data['components']['schemas'][object]

    newProps = OrderedDict()
    newProps['type'] = 'array'
    newProps['items'] = OrderedDict()
    newProps['items']['oneOf'] = []
    if 'description' in oldProps['description']:
        newProps['description'] = oldProps['description']

    for property_key in oldProps['properties']:
        newProps['items']['oneOf'].append(OrderedDict([
            ('$ref', oldProps['properties'][property_key]['$ref'])
        ]))

    data['components']['schemas'][object] = newProps

with open("openapi.yaml", "w") as f:
    yaml.dump(data, f)
