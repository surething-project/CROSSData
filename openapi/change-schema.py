"""
Usage:
    python change-schema.py -f [FIELDS_TO_CHANGE_SCHEMA] -s [CORRECT_SCHEMA]
"""
import ruamel.yaml
import sys
from ruamel.yaml.comments import CommentedMap as OrderedDict

import getopt
import sys

def main(argv):
    fields = []
    schemas = []
    try:
        opts, args = getopt.getopt(argv, "hf:s:", ["fields=", "schemas="])
    except getopt.GetoptError:
        print('change-schema.py -f [FIELDS_TO_CHANGE_SCHEMA] -s [CORRECT_SCHEMA]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('change-schema.py -f [FIELDS_TO_CHANGE_SCHEMA] -s [CORRECT_SCHEMA]')
            sys.exit()
        elif opt in ("-f", "--fields"):
            fields = arg.split(',')
        elif opt in ("-s", "--schemas"):
            schemas = arg.split(',')

    yaml = ruamel.yaml.YAML()
    # yaml.preserve_quotes = True
    with open('openapi.yaml') as fp:
        data = yaml.load(fp)

    for i in range(0, len(fields)):
        object = fields[i].split("/")[0]
        property = fields[i].split("/")[1]
        schema = schemas[i]
        if schema not in data['components']['schemas']:
            print(schema + " schema is not present in components schemas of the OpenAPI Specification.")
            continue

        if object not in data['components']['schemas']:
            print(object + " object is not present in components schemas of the OpenAPI Specification.")
            continue

        if property not in data['components']['schemas'][object]['properties']:
            print(object + " object is not present in components schemas properties of the OpenAPI Specification.")
            continue

        data['components']['schemas'][object]['properties'][property]['$ref'] = '#/components/schemas/' + schemas[i]

    with open("openapi.yaml", "w") as f:
        yaml.dump(data, f)
    

if __name__ == "__main__":
    main(sys.argv[1:])
