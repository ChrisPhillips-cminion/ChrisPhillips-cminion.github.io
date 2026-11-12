---
layout: post
date: 2026-09-24 09:00:00
categories: DataPower
title: "Using ms.callRuleWrapper() in DataPower GatewayScript"
author: ["ChrisPhillips"]
tags: [DataPower, GatewayScript, APIConnect, CustomPolicy, UDP]
draft: true
---

When building a User Defined Policy in API Connect, you often need to call a DataPower processing rule from GatewayScript — passing in the request body, getting back a response, and handling errors cleanly. `ms.callRuleWrapper()` does exactly that, with a single `options` object controlling input/output marshalling, body type coercion, header propagation, and callbacks.

<!--more-->

## What is callRuleWrapper?

`ms.callRuleWrapper()` is part of the DataPower multistep module. It calls a named processing rule and handles input/output marshalling, body type coercion, and header propagation, all driven by a single `options` object. Three optional callbacks let you hook in pre-call validation, post-call output handling, and custom error processing.

The companion function `ms.callRuleWrapperInit()` initialises the globals the wrapper needs. Inside an API gateway UDP it also reads the policy properties and resolves the default rule name automatically. Call it once before building your `options` object.

```javascript
const ms = require('multistep');
let options = {};
let debugObj = ms.callRuleWrapperInit(options);
```

If you skip it, the wrapper calls it internally — but calling it explicitly lets you use the returned `console` object and `verbose` flag for debug logging.

## The options schema

```json
{
  "ruleName": "my-processing-rule",
  "input": {
    "name": "message",
    "read_body": true,
    "body_type": "json",
    "headers": "set"
  },
  "output": {
    "name": "message",
    "read_body": true,
    "update_body": true,
    "body_type": "json",
    "headers": "merge"
  },
  "callbacks": {
    "pre_call": validateInput,
    "post_call": handleOutput,
    "post_error": null
  },
  "properties": {
    "myKey": "myValue"
  }
}
```

`ruleName` is the only field you must set outside a UDP context. Inside a UDP, `callRuleWrapperInit()` fills it in from the policy definition.

`input.body_type` and `output.body_type` drive which `readAs<Type>` function is called internally: `json`, `xml`, or `buffer` (default). Set `read_body: false` if you don't need the body at that stage.

`output.update_body` defaults to `true`, meaning the wrapper writes the called rule's output body back to the message context automatically. Set it to `false` when you want to handle that yourself inside `post_call`.

## Calling the wrapper

```javascript
const ms = require('multistep');

let options = {};
let debugObj = ms.callRuleWrapperInit(options);

if (debugObj.verbose) {
  debugObj.console.debug(`Calling rule: ${options.ruleName}`);
}

ms.callRuleWrapper(options, function(error) {
  if (error) {
    console.error(`${options.ruleName} failed: ${error.errorMessage}`);
  } else {
    console.info(`${options.ruleName} completed`);
  }
});
```

The asynchronous callback fires when the rule finishes. `error` is null on success.

## pre_call: validate before the rule runs

`pre_call` receives the options object, the input message context, the input header object, the called-rule header object, and the parsed body. Return `true` to proceed, `false` to abort.

```javascript
function validateInput(options, contextMsg, contextHdrs, calledRuleHdrs, inBody) {
  if (!inBody) return false;

  let contentType = contextHdrs.get('Content-Type');
  // API gateway context provides session._isAssemblyAction
  if (session._isAssemblyAction) {
    return context.isJSON(contentType);
  }
  // Traditional service — no isJSON helper available
  return contentType.includes('json');
}
```

If you omit `pre_call`, the wrapper assumes validation passes and calls the rule immediately.

## post_call: process the output

`post_call` receives the same five parameters but with the output message context and the rule's output body. Return `true` if the output is valid.

This is the right place to do output transformation when you've set `update_body: false`.

```javascript
function handleOutput(options, contextMsg, contextHdrs, calledRuleHdrs, outBody) {
  if (!options.output.name) return true;
  if (!outBody) return false;

  if (debugObj.verbose) {
    debugObj.console.info(`${options.ruleName} output: ${XML.stringify(outBody)}`);
  }

  if (session._isAssemblyAction) {
    contextMsg.body.write(outBody);
  } else {
    contextMsg.write(outBody);
  }

  contextHdrs.set('Content-Type', 'application/xml');
  return true;
}
```

## post_error: custom error handling

When the called rule fails, `post_error` lets you map DataPower error subcodes to specific HTTP responses. Return `true` to reject the transaction.

```javascript
function handleError(options, error, errorCode, errorSubcode) {
  switch (errorSubcode) {
  case '0x01d30002':
    error.errorStatusCode = 401;
    error.errorPhrase = 'Unauthorized';
    error.errorName = 'UnauthorizedError';
    break;
  default:
    error.errorStatusCode = 500;
    error.errorPhrase = 'Internal Server Error';
    error.errorName = 'RuntimeError';
    break;
  }
  return true;
}
```

Passing `null` for `post_error` leaves the default error behaviour in place.

## Inside a UDP

When your GatewayScript runs inside an API Connect User Defined Policy, `callRuleWrapperInit()` does the following automatically:

- Reads the policy properties defined in the UDP manifest and merges them into `options.properties`
- Resolves the name of the default processing rule and sets `options.ruleName`

This means your script needs no hard-coded rule name or property keys — the policy author controls them through the UDP definition. The IBM Community blog post by Thomas Burke has several working UDP samples that use this pattern: [https://community.ibm.com/community/user/blogs/thomas-burke/2024/08/14/api-connect-more-new-sample-policies-for-the-api-g](https://community.ibm.com/community/user/blogs/thomas-burke/2024/08/14/api-connect-more-new-sample-policies-for-the-api-g)

## Putting it all together

```javascript
const ms = require('multistep');

let options = {};
let debugObj = ms.callRuleWrapperInit(options);

function validateInput(options, contextMsg, contextHdrs, calledRuleHdrs, inBody) {
  if (!inBody) return false;
  let ct = contextHdrs.get('Content-Type');
  return session._isAssemblyAction ? context.isJSON(ct) : ct.includes('json');
}

function handleOutput(options, contextMsg, contextHdrs, calledRuleHdrs, outBody) {
  if (!options.output.name) return true;
  if (!outBody) return false;
  if (session._isAssemblyAction) {
    contextMsg.body.write(outBody);
  } else {
    contextMsg.write(outBody);
  }
  contextHdrs.set('Content-Type', 'application/xml');
  return true;
}

options.input  = { name: 'message', read_body: true, body_type: 'json', headers: 'set' };
options.output = { name: 'message', read_body: true, update_body: false, body_type: 'xml', headers: 'merge' };
options.callbacks = { pre_call: validateInput, post_call: handleOutput, post_error: null };

ms.callRuleWrapper(options, function(error) {
  if (error) {
    console.error(`${options.ruleName}: ${error.errorMessage}`);
  }
});
```

## Summary

`ms.callRuleWrapper()` replaces the manual boilerplate of `ms.callRule()`. Use `callRuleWrapperInit()` to pick up UDP policy properties and rule name automatically. Wire up `pre_call` and `post_call` for the validation and transformation work specific to your policy. Leave `post_error` null unless you need to map DataPower error subcodes to specific HTTP responses.

**References**
- [IBM Docs: Multistep module — ms.callRuleWrapper()](https://www.ibm.com/docs/en/datapower-gateway/10.6.0?topic=apis-multistep-module#mulitstep_js__callRuleWrapper__title__1)
- [Thomas Burke: More sample policies for the API Gateway](https://community.ibm.com/community/user/blogs/thomas-burke/2024/08/14/api-connect-more-new-sample-policies-for-the-api-g)
