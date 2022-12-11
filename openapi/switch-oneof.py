"""
Usage:
    python switch-oneof.py -O <objects-to-switch> -S <new-schemas> -P <new-property-names>
"""
import ruamel.yaml
import sys
from ruamel.yaml.comments import CommentedMap as OrderedDict

import getopt
import sys

def main(argv):
    objects = []
    schemas = []
    properties = []
    try:
        opts, args = getopt.getopt(argv, "hO:S:P:", ["objects=", "schemas=", "properties="])
    except getopt.GetoptError:
        print('switch-oneof.py -o <objects-to-switch> -s <new-schemas> -p <new-property-names>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('switch-oneof.py -o <objects-to-switch> -s <new-schemas> -p <new-property-names>')
            sys.exit()
        elif opt in ("-O", "--objects"):
            objects = arg.split(',')
        elif opt in ("-S", "--schemas"):
            schemas = arg.split(',')
        elif opt in ("-P", "--properties"):
            properties = arg.split(',')    

    if len(objects) != len(schemas) != len(properties):
        print('Arguments must be of the same size!')
        sys.exit()

    yaml = ruamel.yaml.YAML()
    # yaml.preserve_quotes = True
    with open('openapi.yaml') as fp:
        data = yaml.load(fp)

    for i in range(0, len(objects)):
        object = objects[i]
        schema = schemas[i]
        property = properties[i]

        if object not in data['components']['schemas'] or schema not in data['components']['schemas']:
            print(object + " object or " + schema + " schema is not present in components schemas of the OpenAPI Specification.")
            continue

        newProps = OrderedDict()
        newProps['type'] = 'object'
        newProps['properties'] = OrderedDict()

        newProps['properties'][property] = OrderedDict([
            ('$ref', "#/components/schemas/" + schema)
        ])

        data['components']['schemas'][object] = newProps

    with open("openapi.yaml", "w") as f:
        yaml.dump(data, f)

if __name__ == "__main__":
    main(sys.argv[1:])
