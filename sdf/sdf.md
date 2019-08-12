# A Simple Definition Format for One Data Model definitions

## Introduction

The Simple Definition Format is a format for domain experts to use in the creation and maintenance of OneDM definitions.

OneDM tools convert this format to database formats and other serializations as needed.

This document describes definitions of OneDM Objects and their associated Events, Actions, Properties, and Data types.

The JSON format of an SDF definition is described in this document.

## Example Definition:
```
{
  "info": {
    "title": "Example file for ODM Simple JSON Definition Format",
    "version": "20190424",
    "copyright": "Copyright 2019 Example Corp. All rights reserved.",
    "license": "http://example.com/license"
  },
  "namespace": {
    "st": "http://example.com/capability/odm"
  },
  "defaultNamespace": "st",
  "odmObject": {
    "Switch": {
      "id":0,
      "odmProperty": {
        "value": {
        "id":1,
          "type": "string"
          "enum": [
            { "on":1 },
            { "off":0 }
          ]
        }
      },
      "odmAction": {
        "on": {"id":3},
        "off": {"id":4}
      }
    }
  }
}
```

## SDF structure

A SDF definition file has two sections, the information block and the definitions section.

### Information block
The information block contains generic meta data for the file itself and all included definitions.

The keyword that defines an information block is "info". It contains a set of key-value pairs that represent qualities that apply to the included definition.

Qualities of the information block are shown in the following table.

| Quality | Type | Required | Description |
|---|---|---|---|
|title|string| yes|A short summary to be displayed in search results, etc.|
|version|string| yes|The incremental version of the definition, format TBD|
|copyright|string|yes|Link to text or embedded text containing a copyright notice|
|license|string|yes|Link to text or embedded text containing license terms|

### Definitions block

The Definitions block contains the namespace and default namespace declarations along with one or more type definitions according to the class name keywords for type definitions (object, property, action, event, data).

The namespace declaration is a map containing one or more definitions of short names for URIs.

The defaultnamespace declaration defines one of the short names in the namespace map to be the default namespace.

| Quality | Type | Required | Description |
|---|---|---|---|
|namespace|map|no|Defines short names mapped to namespace URIs, to be used as identifier prefixes|
|defaultnamespace|string|no|Identifies one of the prefixes in the namespace map to be used as a default in resolving identifiers|

The following example declares a set of namespaces and defines `st` as the default namespace.
```
"namespace": {
  "st": "http://example.com/capability/odm",
  "zcl": "http://example.com/zcl/odm"
},
"defaultnamespace": "st",
```

Each class may have zero or more type definitions associated with it. Each defined identifier creates a new type and term in the target namespace, and has a scope of the current definition block.

A definition consists of a map entry using the newly defined term as a JSON key, with a value consisting of a map of Qualities and their values.

A definition may in turn contain other definitions. Each definition consists of the newly defined identifier and a set of key-value pairs that represent the defined qualities and contained type definitions.

For example, an Object definition looks like this:

```
"odmObject": {
  "foo": {
    "id": 3001,
    "odmProperty": {
      "bar": {
        "type": "boolean"
        "id": 5150
      }
    }
  }
}
```
An Object "foo" is defined in the default namespace, with an ID of 3001, containing a property "foo.bar", with an ID of 5150 and of type boolean.

## Identifier name resolution
### $ref and JSON Pointer
Name references in SDF are resolved using JSON Pointer. That is, every name reference is the value of a "$ref" statement and includes a JSON Pointer reference. For example, this reference :
```
"temperatureProperty": {
  "$ref": "#/odmData/temperatureData"
}
```
### Namespace Prefix

Compact URI, or CURI, notation may be used to refer to definitions in another namespace. Names are resolved by expanding the prefix using the value for that prefix which is defined in the "namespace" section. For example, if a namespace prefix is defined:
```
"namespace": {
  "foo": "https://example.com/#"
}
```
Then a reference to that namespace:
```
"foo:temperatureData"
```
Would be expanded into:
```
"https://example.com/#temperatureData"
```

### Target namespace

The target namespace is the namespace into which the defined terms are added. The target namespace is defined by the default namespace, or by an explicit prefix on the identifier using a colon ":".

For example if the default namespace in the example above is "foo", then you could use "temperatureData" to refer to the property defined at the URI:
```
https://example.com/#temperatureData
```

## Keywords for type definitions

The following SDF keywords are used to create type definitions in the target namespace.

### odmObject

The odmObject keyword denotes zero or more Object definitions. A object may contain or include definitions of events, actions, properties, and data types.

- Qualities of odmObject

| Quality | Type | Required | Description | Default |
|---|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |  N/A |
|name|string|no|human readable name| N/A |
|description|string|no|human readable description| N/A |
|title|string|no|human readable title to display| N/A |
|include|array|no|list of references to definitions to be included| N/A |
| odmType|object|no|reference to a definition to be used as a template for a new definition|N/A |
| required | array | no | list of required items in a valid definition | N/A |

- odmTypes Object may define or contain

|odmType|
|---|
|odmProperty|
|odmAction|
|odmEvent|
|odmData|


### odmProperty

The odmProperty keyword denotes zero or more property definitions.

Properties are used to model elements of state.

- Qualities of odmProperty

| Quality | Type | Required | Description | Default |
|---|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition | N/A |
|name|string|no|human readable name| N/A |
|description|string|no|human readable description| N/A |
|title|string|no|human readable title to display| N/A |
| required | array | no | list of required items in a valid definition | N/A |
|include|array|no|reference to definitions to be included|
|odmType|object|no|reference to a definition to be used as a template for a new definition| N/A |
|readOnly|boolean|no|Only reads are allowed| false |
|writeOnly|boolean|no|Only writes are allowed| false |
|observable|boolean|no| flag to indicate asynchronous notification is available| true |
|contentFormat|string|no|IANA media type string| N/A |
|subtype|string|no|subtype enumeration|N/A|
|widthInBits|integer|no|hint for protocol binding| N/A|
|units|string|no|[SenML unit][] code| N/A |
|nullable|boolean|no|indicates a null value is available for this type| true |
|scaleMinimum|number|no|lower limit of value in units| N/A |
|scaleMaximum|number| no|upper limit of value in units| N/A |
|type|string, enum|no|JSON data type| N/A |
|minimum|number|no|lower limit of value in the representation format| N/A |
|maximum|number|no|upper limit of value in the representation format| N/A |
|multipleOf|number|no|indicates the resolution of the number in representation format| N/A |
|enum|array|no|enumeration constraint| N/A |
|pattern|string|no|regular expression to constrain a string pattern| N/A |
|format|string|no|JSON Schema formats| N/A|
|minLength|integer|no|shortest length string in octets| N/A |
|maxLength|integer|no|longest length string in octets| N/A |
|default|number, boolean, string|no|specifies the default value for initialization| N/A |
|const|number, boolean, string|no|specifies a constant value for a data item or property| N/A |


- odmTypes Property may define or contain

|odmType|
|---|
|odmData|

### odmAction

The odmAction keyword denotes zero or more Action definitions.

Actions are used to model commands and methods which are invoked. Actions have parameter data that are supplied upon invocation.

- Qualities of odmAction

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|array|no|reference to definitions to be included|
|odmType|object|no|reference to a definition to be used as a template for a new definition|

- odmTypes Action may define or contain

|odmType|
|---|
|odmData|


### odmEvent

The odmEvent keyword denotes zero or more Event definitions.

Events are used to model asynchronous occurrences that may be communicated proactively. Events have data elements which are communicated upon the occurrence of the event.

- Qualities of odmEvent

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|array|no|reference to definitions to be included|
|odmType|object|no|reference to a definition to be used as a template for a new definition|

- odmTypes Event may define or contain

|odmType|
|---|
|odmData|


### odmData

The odmData keyword denotes zero or more Data type definitions.

An odmData definition provides a semantic identifier for a data item and describes the constraints on the defined data item.

odmData is used for Action parameters, for Event data, and for reusable constraints in property definitions

- Qualities of odmData

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|array|no|reference to definitions to be included|
|type|object|no|reference to a definition to be used as a template for a new definition|
|subtype|string|no|subtype enumeration|N/A|
|widthInBits|integer|no|hint for protocol binding| N/A|
|units|string|no|[SenML unit][] code|
|nullable|boolean|no|indicates a null value is available for this type|
|scaleMinimum|number|no|lower limit of value in units|
|scaleMaximum|number|no|upper limit of value in units|
|type|string, enum|yes|JSON data type|
|minimum|number|no|lower limit of value in the representation format|
|maximum|number|no|upper limit of value in the representation format|
|multipleOf|number|no|indicates the resolution of the number in representation format|
|enum|array of map containing {string:number}|no|enumeration constraint|
|pattern|string|no|regular expression to constrain a string pattern|
|format|string|no|JSON Schema formats| N/A|
|minLength|integer|no|shortest length string in octets|
|maxLength|integer|no|longest length string in octets|
|default|number, boolean, string|no|specifies the default value for initialization|
|const|number, boolean, string|no|specifies a constant value for a data item or property|

- odmTypes Data may define or contain

|odmType|
|---|
|(JSON Schema Types with numeric constraint extensions)|


## Example Simple Object Definition:
```
{
  "info": {
    "title": "Example file for ODM Simple JSON Definition Format",
    "version": "20190424",
    "copyright": "Copyright 2019 Example Corp. All rights reserved.",
    "license": "http://example.com/license"
  },
  "namespace": {
    "st": "http://example.com/capability/odm"
  },
  "defaultNamespace": "st",
  "odmObject": {
    "Switch": {
      "id":0,
      "odmProperty": {
        "value": {
        "id":1,
          "type": "string"
          "enum": [
            { "on":1 },
            { "off":0 }
          ]
        }
      },
      "odmAction": {
        "on": {"id":3},
        "off": {"id":4}
      }
    }
  }
}
```
## High Level Composition

The requirements for high level composition include the following:

- The ability to represent products, standardized product types, and modular products while maintaining the atomicity of Objects.

- The ability to compose a reusable definition block from objects, for example a single plug unit of an outlet strip with on/off control, energy monitor, and optional dimmer objects, while retaining the atomicity of the individual objects.

- The ability to compose objects and other definition blocks into a higher level thing that represents a product, while retaining the atomicity of objects.

- The ability to enrich and refine a base definition to have product-specific qualities and quality values, e.g. unit, range, and scale settings.

- The ability to reference items in one part of a complex definition from another part of the same definition, for example to summarize the energy readings from all plugs in an outlet strip.

### Paths in the model namespaces

The model namespace is organized according to terms that are defined in the definition files that are present in the namespace. For example, definitions that originate from an organization or vendor are expected to be in a namespace that is specific to that organization or vendor. There is expecred to be an ODM namespace for common ODM definitions.

The structure of a path in a namespace is defined by the JSON Pointers to the definitions in the files in that namespace. For example, if there is a file defining an object "Switch" with an action "on", then the reference to the action would be "ns:/odmObject/Switch/odmAction/on" where ns is the short name for the namespace prefix.

### Modular Composition
Modular composition of definitions enables an existing definition (could be in the same file or another file) to become part of a new definition by including a reference to the existing definition within the model namespace. 

#### Use of the "odmType" keyword to re-use a definition
An existing definition may be used as a template for a new definition, that is, a new definition is created in the target namespace which uses the defined qualities of some existing definition. This pattern will use the keyword "odmType" as a quality of a new definition with a value consisting of a reference to the existing definition that is to be used as a template. Optionally, new qualities may be added and values of optional qualities and quality values may be defined.

#### The "include" keyword
An existing definition may be used, with its name and its path in the model namespace, as virtual element in a new definition. This has the effect of linking to an instance when the model is deployed as run time. This pattern is useful to link properties, actions, and events from one object to another object, or to link objects together in a complex thing definition. This, aling with named views, supports modeling of the OCF "interface type" feature denoted by the "if" query parameter.

### odmView

The odmView element provides a composed type that defines a named view, and which uses the include keyword to populate the view with one or more instances of odmThing, odmObject, odmProperty, odmEvent, or odmAction. 

- Qualities of odmView

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|array|no|reference to definitions to be included in the view|


- odmTypes odmView may define or contain

|odmType|
|---|
|odmThing|
|odmObject|
|odmProperty|
|odmAction|
|odmEvent|


### odmThing

An odmThing is a potentially reusable composition of objects that is part of a more complex model. For example, the objects that make up the definition of a single plug of an outlet strip could be encapsulated by a component.

Thing definitions work much like Object definitions, except that a Thing is composed of Objects. Thing definitions may use include for Object definitions from elsewhere, or Thing definitions may include their own Object definitions, as well as reusable Property, Action, and Event definitions that can be used to extend or complete the Object definitions.

Thing definitions carry semantic meaning, such as a defined refrigerator compartment and a defined freezer compartment, making up a combination refer-freezer product.

- Qualities of odmThing

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|array|no|reference to definitions to be included|
|odmType|object|no|reference to a definition to be used as a template for a new definition|

- odmTypes odmThing may define or contain

|odmType|
|---|
|odmView|
|odmThing|
|odmObject|

### odmProduct

An odmProduct provides the level of abstraction for representing a unique product or a profile for a standardized type of product, for example a "device type" definition with required minimum functionality.

Products may be composed of Objects and Things at the high level, and may contain their own definitions of Properties, Actions, and Events that can be used to extend or complete the included Object definitions.

Product definitions may set optional defaults and constant values for specific use cases, for example units, range, and scale settings for properties, or available parameters for Actions.

- Qualities of odmProduct

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer | yes | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|
|title|string|no|human readable title to display|
| required | array | no | list of required items in a valid definition | none |
|include|string|no|reference to a definition to be included|


- odmTypes odmProduct may define or contain

|odmType|
|---|
|odmThing|
|odmView|
|odmObject|
|odmProperty|
|odmAction|
|odmEvent|
|odmData|


[SenML unit]: https://www.iana.org/assignments/senml/senml.xhtml#senml-units
