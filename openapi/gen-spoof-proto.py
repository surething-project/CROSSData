"""
Usage:
    python gen-spoof-proto.py -i <imports> -o <objects>
"""
import getopt
import sys

def main(argv):
    imports = []
    objects = []
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["imports=", "objects="])
    except getopt.GetoptError:
        print('gen-spoof-proto.py -i <imports> -o <objects>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('gen-spoof-proto.py -i <imports> -o <objects>')
            sys.exit()
        elif opt in ("-i", "--imports"):
            imports = arg.split(',')
        elif opt in ("-o", "--objects"):
            objects = arg.split(',')

    f = open("../proto/Test.proto", "w")

    f.write("""syntax = "proto3";
package pt.ulisboa.tecnico.cross.contract;

option go_package = "pt.ulisboa.tecnico.cross.contract/v2";

import "google/api/annotations.proto";

""")

    for imp in imports:
        f.write('import "%s";\n' % (imp))

    service_string = """\nservice FakeService {"""

    for i in range(0, len(objects)):
        service_string += """\n    rpc Fake%i(%s) returns (%s) {
        option (google.api.http) = {
            post: "/v2/test/%i",
            body: "*"
        };
    }""" % (i, objects[i], objects[i], i)

    f.write(service_string + """
}""")

    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
