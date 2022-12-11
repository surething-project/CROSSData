#!/bin/bash

usage() {
  cat <<EOF
Usage: gen-openapi.sh -i {required_import_files} -o {objects_that_need_schema} -c {oneof_objects} -f {fields_to_change_schema} -s {correct_schemas} -O {objects_to_switch} -S {new_schemas} -P {new_property_names} -p {proto_files}
EOF
}

# Handle input flags
while getopts i:o:c:p:f:s:O:S:P: flag; do
  case "${flag}" in
  i) imports=${OPTARG} ;;
  o) objects=${OPTARG} ;;
  c) convertables=${OPTARG} ;;
  f) fields=${OPTARG} ;;
  s) schemas=${OPTARG} ;;
  p) protos=${OPTARG} ;;
  O) objectsToSwitch=${OPTARG} ;;
  S) schemasForSwitch=${OPTARG} ;;
  P) properties=${OPTARG} ;;
  esac
done

python3 gen-spoof-proto.py -i $imports -o $objects

cd ../proto

protoc ${protos//","/" "} Test.proto -I. -I../../SureThing_Core_Data/data-types/proto/. --openapi_out=.

mv ./openapi.yaml ../openapi/

rm Test.proto

cd ../openapi/

python3 gen-oneof.py $convertables

python3 del-endpoint.py $objects

python3 change-schema.py -f $fields -s $schemas

python3 switch-oneof.py -O $objectsToSwitch -S $schemasForSwitch -P $properties

sed -i 's/application\/json/application\/x-protobuf/g' ./openapi.yaml

python3 swagger-yaml-to-html.py <./openapi.yaml >openapi.html
