---
layout: post
date: 2020-9-28 00:14:00
categories: APIConnect
title: "Applying API Governance Part 3 –  Linting"
---
This is part three of a series on how to apply governance in API Connect.  Governance is sometimes considered a taboo topic because when people imagine governance, they see red tape that stifles progress. If governance is designed properly it can provide a single approach for all parts of the project with minimal impact on the development rate.

Linting is the process of validating files prior to deployment to catch the low hanging fruit. With APIs we would expect to link the OpenAPI Specification both syntactically as well as allowing for custom validation to be run to ensure governance standards are met.

<!--more-->

Every organization must have governance standards to follow, whether naming conventions, requirements for fields, self documenting, versioning or many others.

When these are applied all of the APIs will follow the same pattern and provide a joined up experience for consumers. If each API follows it's own strategy each consumer has to relearn the language and definitions for each API which makes consumption significantly harder. In addition it is easier to find an API that provides an existing function if there is a standard naming convention to follow.

The challenge has always been enforcing these.  Traditionally this has been validated manually but that does not work at scale or at speed.

IBM have an open source project called the openapi-validator ([https://github.com/IBM/openapi-validator](https://github.com/IBM/openapi-validator)). Out of the box the OpenAPI Validator will validate if an OpenAPI specification meets the specification. If the API does not meet the specification it provides alerts and warnings on the concerns.

# How to install

1. Install the npm module globally `npm install -g ibm-openapi-validator`
2. Create the initial config `lint-openapi init` - This creates a config file called `.validaterc`
3. Run `lint-openapi <path to openapi file> -s` (-s produces a table of results)

# Modifying the out of the box warnings

1. Edit `.validaterc` and modify the warnings and error lines to be either warning, error or off.

# Custom Validation Rules (Beta)
In the current release of the openapi-validator there is beta option to run a spectral config. This can be used to create custom rules.
1. create a file in the same directory as `.validaterc` called `.spectral.json` and paste in the following configuration
```json
{
	"extends": [["spectral:oas", "off"]],
	"formats": ["oas2", "oas3"],
	"functionsDir": "./src/spectral/functions",
	"functions": [
		"oasResponseHasExample"
	],
	"rules": {
    "check-produces-value-case-sensitive": {
			"description": "'produces' object should not contain the value 'application'",
			"type": "style",
			"given": "$.paths..produces.*",
			"severity": "error",
			"formats": ["oas2"],
			"message": "{{path}} contained a value with the invalid string '/produces/'",
			"then": {
				"function": "pattern",
				"functionOptions": {
					"notMatch": "/application/"
				}
			}
		},
		"validate-create-operation": {
			"description": "Operations with an operationID that starts with 'create' must have a valid 201 response.",
			"given": "$.paths.*[?(/^create/.test(@.operationId))]",
			"severity": "warn",
			"recommended": true,
			"type": "validation",
			"then": {
				"field": "responses.201",
				"function": "truthy"
			}
		},
		"validate-response-has-example": {
			"description": "Operation response bodies should have an example.",
			"given": "$.paths..responses..content.*",
			"severity": "warn",
			"recommended": false,
			"type": "validation",
			"then": {
				"function": "oasResponseHasExample",
				"functionOptions": {
				  "value": "test"
				}
			}
		}
	}
}
```
2. Inside the rules you may extend these rules with the required custom rules. These rules will walk down the tree in the OpenAPI specification and validate items as required.

# Sample

```
cminion@machine$ lint-openapi -s api-with-examples.yaml
Function 'oasResponseHasExample' could not be loaded: Not Found

errors

  Message :   #/paths/~1/get/produces/0 contained a value with the invalid string '/produces/'
  Path    :   paths./.get.produces.0
  Line    :   11

  Message :   #/paths/~1v2/get/produces/0 contained a value with the invalid string '/produces/'
  Path    :   paths./v2.get.produces.0
  Line    :   80

warnings

  Message :   operationIds must follow case convention: lower_snake_case
  Path    :   paths./.get.operationId
  Line    :   8

  Message :   operationIds must follow case convention: lower_snake_case
  Path    :   paths./v2.get.operationId
  Line    :   77

statistics

  Total number of errors   : 2
  Total number of warnings : 2

  errors
   1  (50%) : #/paths/~1/get/produces/0 contained a value with the invalid string '/produces/'
   1  (50%) : #/paths/~1v2/get/produces/0 contained a value with the invalid string '/produces/'

  warnings
   2 (100%) : operationIds must follow case convention
```
