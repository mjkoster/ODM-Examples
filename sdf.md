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
      "odmProperty": {
        "value": {
          "type": "string",
          "enum": ["on", "off"]
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

## SDF structure

A SDF definition file has two sections, the information block and the definitions section.

### Information block
The information block contains generic meta data for the file itself and all included definitions.

The keyword that defines an information block is "info". It contains a set of key-value pairs that represent qualities that apply to the included definition.

Qualities of the information block are shown in the following table.

| Quality | Type | Optional | Description |
|---|---|---|---|
|title|string|no|A short summary to be displayed in search results, etc.|
|version|string|no|The incremental version of the definition, format TBD|
|copyright|string|no|Link to text or embedded text containing a copyright notice|
|license|string|no|Link to text or embedded text containing license terms|

### Definitions block

The Definitions block contains the namespace and default namespace declarations along with one or more type definitions according to the class name keywords for type definitions (object, property, action, event, data).

The namespace declaration is a map containing one or more definitions of short names for URIs.

The defaultnamespace declaration defines one of the short names in the namespace map to be the default namespace.

| Quality | Type | Optional | Description |
|---|---|---|---|
|namespace|map|yes|Defines short names mapped to namespace URIs, to be used as identifier prefixes|
|defaultnamespace|string|yes|Identifies one of the prefixes in the namespace map to be used as a default in resolving identifiers|

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

## Scope of Identifiers
### Namespace resolution order:
1. identifiers with an explicit namespace prefix
2. keywords and quality names in the ODM and JSON Schema namespaces, defined in
the JSON Schema for SDF
3. identifier defined in the same (local) block
4. identifier defined in the next closest enclosing block recursively
5. identifier defined in the file
6. identifier defined in the default namespace

### Identifier name expansion from JSON path

When a type is defined, the identifier is internally prefixed with the JSON path that locates the definition in the file.

Types defined at the top level in the file go into the namespace as they are.

Types defined within another definition are prefixed with the path to the enclosing definition. For example, if there is an Object "foo" defined, and a definition for "bar" with Object foo, the path to bar will be "foo.bar" within the default namespace. The Property name "foo.bar" can be used as a reference within some other definition, provided that the scope can be correctly resolved.

### Target namespace

The target namespace is the namespace into which the defined terms are added. The target namespace is defined by the default namespace, or by an explicit prefix on the identifier separated by a semicolon ":".

For example if the default namespace in the example above is "baz", then you could refer to "baz:foo.bar" to point to the property defined by the "bar" definition.

## Keywords for type definitions

The following SDF keywords are used to create type definitions in the target namespace.

### odmObject

The odmObject keyword denotes zero or more Object definitions. A object may contain or include definitions of events, actions, properties, and data types.

- Qualities of odmObject

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|

- Types Object may define or contain

|Type|
|---|
|odmProperty|
|odmAction|
|odmEvent|
|odmData|


### odmProperty

The odmProperty keyword denotes zero or more property definitions.

Properties are used to model elements of state.

- Qualities of odmProperty

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|
|readOnly|boolean|yes|Only reads are allowed|
|writeOnly|boolean|yes|Only writes are allowed|
|observable|boolean|yes| flag to indicate asynchronous notification is available|
|contentFormat|string|yes|IANA media type string|
|units|string|yes|[SenML unit][] code|
|nullable|boolean|yes|indicates a null value is available for this type|
|encoding|map|yes|applies additional constraints|
|scaleMinimum|number|yes|lower limit of value in units|
|scaleMaximum|number|yes|upper limit of value in units|
|type|string, enum|yes|JSON data type|
|minimum|number|yes|lower limit of value in the representation format|
|maximum|number|yes|upper limit of value in the representation format|
|multipleOf|number|yes|indicates the resolution of the number in representation format|
|enum|array|yes|enumeration constraint|
|pattern|string|yes|regular expression to constrain a string pattern|
|minLength|integer|yes|shortest length string in octets|
|maxLength|integer|yes|longest length string in octets|
|default|number, boolean, string|yes|specifies the default value for initialization|
|const|number, boolean, string|yes|specifies a constant value for a data item or property|


- Types Property may define or contain

|Type|
|---|
|odmData|

### odmAction

The odmAction keyword denotes zero or more Action definitions.

Actions are used to model commands and methods which are invoked. Actions have parameter data that are supplied upon invocation.

- Qualities of odmAction

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|

- Types Action may define or contain

|Type|
|---|
|odmData|


### odmEvent

The odmEvent keyword denotes zero or more Event definitions.

Events are used to model asynchronous occurrences that may be communicated proactively. Events have data elements which are communicated upon the occurrence of the event.

- Qualities of odmEvent

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|
 readable title to display|

- Types Event may define or contain

|Type|
|---|
|odmData|


### odmData

The odmData keyword denotes zero or more Data type definitions.

An odmData definition provides a semantic identifier for a data item and describes the constraints on the defined data item.

odmData is used for Action parameters, for Event data, and for reusable constraints in property definitions

- Qualities of odmData

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|
|units|string|yes|[SenML unit][] code|
|nullable|boolean|yes|indicates a null value is available for this type|
|encoding|map|yes|applies additional constraints|
|scaleMinimum|number|yes|lower limit of value in units|
|scaleMaximum|number|yes|upper limit of value in units|
|type|string, enum|yes|JSON data type|
|minimum|number|yes|lower limit of value in the representation format|
|maximum|number|yes|upper limit of value in the representation format|
|multipleOf|number|yes|indicates the resolution of the number in representation format|
|enum|array|yes|enumeration constraint|
|pattern|string|yes|regular expression to constrain a string pattern|
|minLength|integer|yes|shortest length string in octets|
|maxLength|integer|yes|longest length string in octets|
|default|number, boolean, string|yes|specifies the default value for initialization|
|const|number, boolean, string|yes|specifies a constant value for a data item or property|

- Types Data may define or contain

|Type|
|---|
|JSON Schema Types with numeric constraint extensions|


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
      "odmProperty": {
        "value": {
          "type": "string",
          "enum": ["on", "off"]
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
## High Level Composition

The requirements for high level composition include the following:

- The ability to represent products, standardized product types, and modular products while maintaining the atomicity of Objects.

- The ability to compose a reusable definition block from objects, for example a single plug unit of an outlet strip with on/off control, energy monitor, and optional dimmer objects, while retaining the atomicity of the individual objects.

- The ability to compose objects and other definition blocks into a higher level thing that represents a product, while retaining the atomicity of objects.

- The ability to enrich and refine a base definition to have product-specific qualities and quality values, e.g. unit, range, and scale settings.

- The ability to reference items in one part of a complex definition from another part of the same definition, for example to summarize the energy readings from all plugs in an outlet strip.

### Paths in the model namespaces

The model namespace is organized according to terms that are defined in the definition files that are loaded into the namespace. For example, definitions that originate from an organization or vendor are expected to be in a namespace that is specific to that organization or vendor.

In general, the structure of a path in a namespace is defined by the hierarchical relationship of the definitions in the file. For example, if there is a file defining an object "Switch" with an action "on", then the external reference to the action would be "Switch.on" (assuming for the moment the use of dot as a path segment separator).

A reference within the "Switch" object would simply use "on" according to the identifier resolution precedence rules.

### Re-use and Recursion
Re-use of definitions enables an existing definition (could be in the same file or another file) to become part of a new definition by including a reference to the existing definition within the model namespace. There are currently considered three cases for reuse of definitions. The semantics are similar to those of typed links.

#### The "extends" pattern
An existing definition can be used as a template for a new definition, that is, a new term is created in the namespace which uses the defined qualities of some existing definition. This pattern will use the keyword "extends" as a quality of a new definition with a value consisting of a reference to the existing definition that is to be used as a template. Optionally, new qualities may be added and values of defined qualities may be changed in the extended definition.

#### The "refines" pattern
An existing definition may be re-used with its name, that is, the name of some existing definition is re-used as an element in a new definition, along with its defined qualities. This pattern will use the keyword "refines" and will allow qualities in the new definition to override values from the source definition.

#### The "includes" pattern
An existing definition may be used, with its name and its path in the model namespace, as an element in a new definition. This has the effect of linking to an instance of the model in the deployment. This pattern will use the keyword "includes" and is useful to link properties, actions, and events from one object to another object, or to link objects together in a complex thing definition.

### odmComponent

An odmComponent is a potentially reusable composition of objects that is part of a more complex model. For example, the objects that make up the definition of a single plug of an outlet strip could be encapsulated by a component.

Component definitions work much like object definitions, except that a component is composed of objects. Components may use the "includes", "refines", or "extends" pattern, or may define objects within the component definition. Component definitions may include their own Object definitions, as well as reusable Property, Action, and Event definitions that can be used to extend or complete the included Object definitions.

Using the "includes" pattern enables a component to provide a specific "view" into the functionality of a complex device, for example a way to summarize the energy readings of all plugs in an outlet strip, or a way of including common functions, like power controls, in the definition of the sub-functions in a multifunction device like a printer + scanner product.

Components may carry semantic meaning, such as a defined refrigerator compartment and a defined freezer compartment, making up a combination refer-freezer product.

- Qualities of odmComponent

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|

- Types odmComponent may define or contain

|Type|
|---|
|odmObject|
|odmProperty|
|odmAction|
|odmEvent|
|odmData|


### odmThing

An odmThing provides the level of abstraction for representing a unique product or a profile for a standardized type of product, for example a "device type" definition with required minimum functionality.

Things may be composed of Objects and Components at the high level, and may contain their own definitions of Properties, Actions, and Events that can be used to extend or complete the included Object definitions.

Thing definitions may use the includes, refines, or extends pattern, and are expected to override defaults for specific use cases, for example units, range, and scale settings for properties, or available parameters for Actions.

- Qualities of odmThing

| Quality | Type | Optional | Description |
|---|---|---|---|
|id| integer, string | yes | internal unique identifier for the definition |
|name|string|yes|human readable name|
|description|string|yes|human readable description|
|title|string|yes|human readable title to display|
|optional| boolean|yes|defines whether this element is optional in an implementation|
|includes|string|yes|reference to a definition to be included|
|refines|string|yes|reference to a definition to be refined|
|extends|string|yes|reference to a definition to be extended|

- Types odmThing may define or contain

|Type|
|---|
|odmObject|
|odmComponent|
|odmProperty|
|odmAction|
|odmEvent|
|odmData|


[SenML unit]: https://www.iana.org/assignments/senml/senml.xhtml#senml-units
