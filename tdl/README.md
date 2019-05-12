## tdl2json

Convert a file in TDL (thing definition) text format to JSON for ODM definitions

TDL is a text language that is essentially JSON with most of the punctuation
stripped out and replaced with whitespace, except for 3 classes of block delimiters:

- quoted strings using DQUOTE ""
- arrays using []
- objects using {}

an example text definition:

```
info {
  title
      "Example file for ODM Simple JSON Definition Format"
  version
      "20190424"
  copyright
      "Copyright 2019 Example Corp.
        All rights reserved."
  license
      http://example.com/license
}
namespace {
  st http://example.com/capability/odm
}
defaultnamespace st
odmObject {
  Switch {
    odmProperty {
      value {
        type string
        enum [on off]
      }
    }
    odmAction {
      on {}
      off {}
    }
  }
}
```

when converted to JSON becomes:

```
{
  "info": {
    "title": "Example file for ODM Simple JSON Definition Format",
    "version": "20190424",
    "copyright": "Copyright 2019 Example Corp.\n        All rights reserved.",
    "license": "http://example.com/license"
  },
  "namespace": {
    "st": "http://example.com/capability/odm"
  },
  "defaultnamespace": "st",
  "odmObject": {
    "Switch": {
      "odmProperty": {
        "value": {
          "type": "string",
          "enum": [
            "on",
            "off"
          ]
        }
      },
      "odmAction": {
        "on": {},
        "off": {}
      }
    }
  }
}
```
usage:

```
python tdl2json.py <input filename (text format)> <output file name (json format)>
```
