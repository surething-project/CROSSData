"""
Usage:
    python del-endpoint.py [OBJECTS-WITH-PATHS-TO-BE-DELETED]
"""
import ruamel.yaml
import sys

yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open('openapi.yaml') as fp:
    data = yaml.load(fp)
    objects = sys.argv[1].split(',')

for i in range(0, len(objects)):
    del data['paths']['/v2/test/%i' % (i)]

fakeTag = None

for tag in data['tags']:
    if tag['name'] == 'FakeService':
        fakeTag = tag
        break

if fakeTag is not None:
    data['tags'].remove(tag)

with open("openapi.yaml", "w") as f:
    yaml.dump(data, f)
