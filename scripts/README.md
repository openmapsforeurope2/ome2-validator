# Scripts

This directory contains utility scripts.

## JSON_file_to_classes

This script can take a data model definition,
[such as this file](https://github.com/openmapsforeurope2/data-tools/blob/main/config/mcd.json),
and generate source files.
Running the script will report changes to the standard output
and generate text files in the specified output directory.
The contents of the text files can be inspected
and manually copied to the tool's source code.

### Example usage

```sh
cd scripts/

python3 -m JSON_file_to_classes --input ../json/mcd.json --output ../json/generated/ --specs ../validation_specs/dv1/
```
