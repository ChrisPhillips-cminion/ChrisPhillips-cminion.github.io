---
layout: post
date: 2026-02-18 10:00:00
categories: APIConnect
title: "Custom Request Body Validation with GatewayScript in API Connect"
author: [ "ChrisPhillips", "SimonKapadia" ]
draft: true
---

When building APIs, robust input validation is critical for security, data integrity, and providing clear error messages to API consumers. While API Connect provides built-in validation through OpenAPI schemas, sometimes you need to explan why the validation failed to the consumers. This article demonstrates how to implement custom request body validation using GatewayScript that validates against a JSON schema and returns detailed error messages for each invalid field.

<!--more-->



## The Complete API Definition

Here's a complete OpenAPI 2.0 (Swagger) definition that implements a flexible validation API. The key difference from traditional validation is that both the payload and schema are sent in the request body, making this a reusable validation service:

*Note: the schema must be in both the spec and the gatewaysript*

```yaml
swagger: '2.0'
info:
  title: Body Validation API
  version: 1.0.0
  description: >-
    API that validates request body against a JSON schema and returns invalid
    fields
  x-ibm-name: body-validation-api
basePath: /validate
schemes:
  - https
consumes:
  - application/json
produces:
  - application/json
definitions:
  ValidationRequest:
    type: object
    required:
      - payload
      - schema
    properties:
      payload:
        type: object
        description: The data to be validated
      schema:
        type: object
        description: JSON Schema to validate the payload against
        properties:
          type:
            type: string
          required:
            type: array
            items:
              type: string
          properties:
            type: object
          additionalProperties:
            type: boolean
    additionalProperties: false

  ValidationSuccess:
    type: object
    properties:
      status:
        type: string
        example: success
      message:
        type: string
        example: Validation passed

  ValidationError:
    type: object
    properties:
      status:
        type: string
        example: error
      message:
        type: string
        example: Validation failed
      errors:
        type: array
        items:
          type: object
          properties:
            field:
              type: string
              description: The field that failed validation
            message:
              type: string
              description: Description of the validation error
            value:
              type: string
              description: The actual value that failed validation
paths:
  /user:
    post:
      summary: Validate user data
      description: Validates user data against a provided schema
      parameters:
        - name: body
          in: body
          required: true
          schema:
            $ref: '#/definitions/ValidationRequest'
      responses:
        '200':
          description: Validation successful
          schema:
            $ref: '#/definitions/ValidationSuccess'
        '400':
          description: Validation failed
          schema:
            $ref: '#/definitions/ValidationError'
x-ibm-configuration:
  enforced: true
  testable: true
  phase: realized
  cors:
    enabled: true
  gateway: datapower-api-gateway
  type: rest
  assembly:
    execute:
      - parse:
          version: 2.0.0
          title: Parse JSON Body
          parse-settings-reference:
            default: apic-default-parsesettings
      - gatewayscript:
          version: 2.0.0
          title: Handle Validation
          source: |
            // Get the parsed request body (already parsed by the parse policy)
            var requestBody = context.get('request.body');

            // Extract payload and schema from request
            var payload = requestBody.payload;
            var schema = requestBody.schema;

            // Validate that both payload and schema are present
            if (!payload) {
              context.set('message.status.code', 400);
              context.set('message.body', {
                status: 'error',
                message: 'Missing payload in request body',
                errors: [{
                  field: 'payload',
                  message: 'payload field is required',
                  value: 'undefined'
                }]
              });
              return;
            }

            if (!schema) {
              context.set('message.status.code', 400);
              context.set('message.body', {
                status: 'error',
                message: 'Missing schema in request body',
                errors: [{
                  field: 'schema',
                  message: 'schema field is required',
                  value: 'undefined'
                }]
              });
              return;
            }

            // Validation function
            function validateSchema(data, schema, path) {
              var errors = [];
              path = path || '';

              // Check required fields
              if (schema.required) {
                for (var i = 0; i < schema.required.length; i++) {
                  var requiredField = schema.required[i];
                  if (data[requiredField] === undefined || data[requiredField] === null) {
                    errors.push({
                      field: path + requiredField,
                      message: 'Required field is missing',
                      value: 'undefined'
                    });
                  }
                }
              }

              // Check properties
              if (schema.properties) {
                for (var prop in data) {
                  if (data.hasOwnProperty(prop)) {
                    var propSchema = schema.properties[prop];
                    var value = data[prop];
                    var fieldPath = path + prop;

                    if (!propSchema && schema.additionalProperties === false) {
                      errors.push({
                        field: fieldPath,
                        message: 'Additional property not allowed',
                        value: String(value)
                      });
                      continue;
                    }

                    if (propSchema) {
                      // Type validation
                      var actualType = Array.isArray(value) ? 'array' : typeof value;
                      if (actualType === 'object' && value === null) {
                        actualType = 'null';
                      }
                      
                      if (propSchema.type && actualType !== propSchema.type) {
                        errors.push({
                          field: fieldPath,
                          message: 'Invalid type. Expected ' + propSchema.type + ' but got ' + actualType,
                          value: String(value)
                        });
                        continue;
                      }

                      // String validations
                      if (propSchema.type === 'string' && typeof value === 'string') {
                        if (propSchema.minLength && value.length < propSchema.minLength) {
                          errors.push({
                            field: fieldPath,
                            message: 'String length must be at least ' + propSchema.minLength + ' characters',
                            value: value
                          });
                        }
                        if (propSchema.maxLength && value.length > propSchema.maxLength) {
                          errors.push({
                            field: fieldPath,
                            message: 'String length must not exceed ' + propSchema.maxLength + ' characters',
                            value: value
                          });
                        }
                        if (propSchema.pattern) {
                          var regex = new RegExp(propSchema.pattern);
                          if (!regex.test(value)) {
                            errors.push({
                              field: fieldPath,
                              message: 'String does not match required pattern',
                              value: value
                            });
                          }
                        }
                      }

                      // Number/Integer validations
                      if ((propSchema.type === 'number' || propSchema.type === 'integer') && typeof value === 'number') {
                        if (propSchema.minimum !== undefined && value < propSchema.minimum) {
                          errors.push({
                            field: fieldPath,
                            message: 'Value must be at least ' + propSchema.minimum,
                            value: String(value)
                          });
                        }
                        if (propSchema.maximum !== undefined && value > propSchema.maximum) {
                          errors.push({
                            field: fieldPath,
                            message: 'Value must not exceed ' + propSchema.maximum,
                            value: String(value)
                          });
                        }
                      }
                    }
                  }
                }
              }

              return errors;
            }

            // Perform validation using the provided schema
            var validationErrors = validateSchema(payload, schema, '');

            // Set response based on validation results
            if (validationErrors.length > 0) {
              context.set('message.status.code', 400);
              context.set('message.body', {
                status: 'error',
                message: 'Validation failed',
                errors: validationErrors
              });
            } else {
              context.set('message.status.code', 200);
              context.set('message.body', {
                status: 'success',
                message: 'Validation passed',
                data: payload
              });
            }
  activity-log:
    enabled: true
    success-content: activity
    error-content: payload
```

## Understanding the Implementation

### 1. Request Structure

This API uses a flexible approach where both the payload and schema are sent in the request body:

**Request Body Structure** (`ValidationRequest`):
```json
{
  "payload": {
    // The data to be validated
  },
  "schema": {
    // JSON Schema definition
    "type": "object",
    "required": ["field1", "field2"],
    "properties": {
      // Property definitions
    }
  }
}
```

**Key Benefits**:
- **Dynamic validation**: No need to redeploy the API for different schemas
- **Reusable service**: One API can validate any payload against any schema
- **Flexible**: Supports different validation requirements without code changes
- **Testable**: Easy to test different schemas and payloads


### 2. Assembly Flow

The API assembly consists of two policies:

1. **Parse Policy**: Parses the incoming JSON request body and makes it available to subsequent policies
2. **GatewayScript Policy**:
   - Extracts the `payload` and `schema` from the request body
   - Validates that both are present
   - Performs custom validation using the provided schema
   - Sets the appropriate response

### 3. Validation Logic

The `validateSchema` function performs comprehensive validation on the provided payload using the provided schema:

**Required Field Validation**:
```javascript
if (data[requiredField] === undefined || data[requiredField] === null) {
  errors.push({
    field: path + requiredField,
    message: 'Required field is missing',
    value: 'undefined'
  });
}
```

**Type Validation**:
```javascript
var actualType = Array.isArray(value) ? 'array' : typeof value;
if (propSchema.type && actualType !== propSchema.type) {
  errors.push({
    field: fieldPath,
    message: 'Invalid type. Expected ' + propSchema.type + ' but got ' + actualType,
    value: String(value)
  });
}
```

**String Constraints**:
- `minLength` / `maxLength`: Validates string length
- `pattern`: Validates against regular expressions

**Number Constraints**:
- `minimum` / `maximum`: Validates numeric ranges

**Additional Properties**:
- When `additionalProperties: false`, rejects any fields not in the schema

## Example Requests and Responses

### Valid Request

**Request**:
```bash
curl -X POST https://api.example.com/validate/user \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": 30
    },
    "schema": {
      "type": "object",
      "required": ["name", "email", "age"],
      "properties": {
        "name": {
          "type": "string",
          "minLength": 2,
          "maxLength": 50,
          "pattern": "^[a-zA-Z\\s]+$"
        },
        "email": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "age": {
          "type": "number",
          "minimum": 18,
          "maximum": 120
        }
      },
      "additionalProperties": false
    }
  }'
```

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Validation passed",
  "data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }
}
```

### Invalid Request - Missing Required Field

**Request**:
```bash
curl -X POST https://api.example.com/validate/user \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "name": "John Doe",
      "email": "john.doe@example.com"
    },
    "schema": {
      "type": "object",
      "required": ["name", "email", "age"],
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "age": {"type": "number"}
      }
    }
  }'
```

**Response** (400 Bad Request):
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "field": "age",
      "message": "Required field is missing",
      "value": "undefined"
    }
  ]
}
```

### Invalid Request - Multiple Validation Errors

**Request**:
```bash
curl -X POST https://api.example.com/validate/user \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "name": "J",
      "email": "invalid-email",
      "age": 15,
      "extraField": "not allowed"
    },
    "schema": {
      "type": "object",
      "required": ["name", "email", "age"],
      "properties": {
        "name": {
          "type": "string",
          "minLength": 2
        },
        "email": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        "age": {
          "type": "number",
          "minimum": 18
        }
      },
      "additionalProperties": false
    }
  }'
```

**Response** (400 Bad Request):
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "field": "name",
      "message": "String length must be at least 2 characters",
      "value": "J"
    },
    {
      "field": "email",
      "message": "String does not match required pattern",
      "value": "invalid-email"
    },
    {
      "field": "age",
      "message": "Value must be at least 18",
      "value": "15"
    },
    {
      "field": "extraField",
      "message": "Additional property not allowed",
      "value": "not allowed"
    }
  ]
}
```

### Invalid Request - Wrong Data Type

**Request**:
```bash
curl -X POST https://api.example.com/validate/user \
  -H "Content-Type: application/json" \
  -d '{
    "payload": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": "thirty"
    },
    "schema": {
      "type": "object",
      "required": ["name", "email", "age"],
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "age": {"type": "number"}
      }
    }
  }'
```

**Response** (400 Bad Request):
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "field": "age",
      "message": "Invalid type. Expected number but got string",
      "value": "thirty"
    }
  ]
}
```


## Additional Resources

- [IBM API Connect GatewayScript Documentation](https://www.ibm.com/docs/en/api-connect/10.0.x?topic=constructs-gatewayscript-api)
- [JSON Schema Specification](https://json-schema.org/)
- [DataPower GatewayScript Reference](https://www.ibm.com/docs/en/datapower-gateway)