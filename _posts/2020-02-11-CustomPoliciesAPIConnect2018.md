---
layout: post
date: 2020-02-11 00:01:00
categories: APIConnect
title: "User Defined Policies / Custom Policies in API Connect 2018  (MQ invoke Example)"
location: singapore
draft: true
---

User Defined Policies (aka Custom Policies) allow a customer bespoke piece of function to be exposed on a catalog. in this example I will explain the different pieces that  need to be constructed to build an MQ Invoke Policy. This article explains how to create them for the API Gateway.

<!--more-->

*This article is not going to include how to persist this config to DataPower running in Kubernetes or OpenShift. This will be covered in another article*

In order to produce a User Defined Policy a number of objects must be created in DataPower.



#### Assembly-Function-Call ->  Assembly-Function -> Assembly -> Api-Rule -> Action

### Assembly Function - Call
The Assembly  Function call  takes a list of  properties that are exposed to the  API Manager.  Along side the properties it links the Assembly-Function
```
assembly-function-call "mq-invoke"
 title "mq-invoke"
 function mq-invoke
 parameter
   name "qmgrobj"
 exit
 parameter
   name "qmgrobj"
 exit
 parameter
   name "queue"
 exit
 parameter
   name "boq"
 exit
 parameter
   name "timeout"
 exit
 parameter
   name "structureid"
 exit
 parameter
   name "version"
 exit
 parameter
   name "encoding"
 exit
 parameter
   name "codedcharsetid"
 exit
 parameter
   name "flags"
 exit
 parameter
   name "format"
 exit
 parameter
   name "ccsid"
 exit
exit
```


## Assembly-Function
The  Assembly function takes the details parameter information that will be rendered in the Assembly Tool in the API Designer.  This links to the Assembly Object
```
assembly-function "mq-invoke"
 title "mq-invoke"
 parameter
   name "qmgrobj"
   label "MQ QMGR Object"
   description "The MQ QM Object"
   value-type string
 exit
 parameter
   name "queue"
   label "Queue"
   description "The Queue to be used"
   value-type string
 exit
 parameter
   name "boq"
   label "Back Out Queue"
   description "Back Out Queue"
   value-type string
 exit
 parameter
   name "queue"
   label "Queue"
   description "The Queue to be used"
   value-type string
 exit
 parameter
   name "timeout"
   label "Timeout"
   description "Timeout"
   value-type string
 exit
 parameter
   name "structureid"
   label "StructureId"
   description "The structure Id"
   value-type string
   default "RFH"
 exit
 parameter
   name "version"
   label "Version"
   description "Version"
   value-type string
   default "MQRFH_VERSION_2"
 exit
 parameter
   name "encoding"
   label "Encoding"
   description "Encoding"
   value-type string
   default "MQENC_NATIVE"
 exit
 parameter
   name "codedcharsetid"
   label "CodedCharSetId"
   description "CodedCharSetId"
   value-type string
   default "MQCCSI_INHERIT"
 exit
 parameter
   name "flags"
   label "Flags"
   description "Flags"
   value-type string
   default "MQRFH_NONE"
 exit
 parameter
   name "format"
   label "Format"
   description "Format"
   value-type string
   default "MQSTR"
 exit
 parameter
   name "ccsid"
   label "Name Value CCSID"
   description "Name Value CCSID"
   value-type string
   default "1208"
 exit
 assembly mq-invoke
exit
```

## Assembly
The assembly links to the initial api-rule that is going to be executed.
```
assembly "mq-invoke"
 rule mq-invoke
exit
```

### API-Rule
The API Rule contains a series of sequential actions. In the example we are using we only have a single action which  is to  run some gatewayscript.
```
api-rule "mq-invoke"
 action mq-invoke
exit
```

### Action
There are  a  number of out of the box  actions that can be called here. Anything that is available as an object the Assembly pallet is an action.
In our example we are invoking some gateway script. The  gateway script file must be loaded into the DataPower manually and linked from the action.
```
assembly-gatewayscript "mq-invoke"
 title "MQ Invoke"
 gatewayscript-location "local://js/mq-invoke.js"
exit
```


Once these are created there are two steps that need to be completed.
1. Export the object from DataPower and put them in to each DataPower in the Gateway Service.
2. The API Gateway Service must be modified to include the UDP and then disabled and enabled to make it visible in the API Designer.

The example  CLI Commands to modify the gateway service are below
```
apic-gw-service
 user-defined-policies mq-invoke
exit
```

### Complete Example
<button class="collapsible" id="fullExample">Full Sample Config</button>

<div class="content" id="fullExampledata" markdown="1">
```
%if% available "assembly-function-call"

assembly-function-call "mq-invoke"
 title "mq-invoke"
 function mq-invoke
 parameter
   name "qmgrobj"
 exit
 parameter
   name "qmgrobj"
 exit
 parameter
   name "queue"
 exit
 parameter
   name "boq"
 exit
 parameter
   name "timeout"
 exit
 parameter
   name "structureid"
 exit
 parameter
   name "version"
 exit
 parameter
   name "encoding"
 exit
 parameter
   name "codedcharsetid"
 exit
 parameter
   name "flags"
 exit
 parameter
   name "format"
 exit
 parameter
   name "ccsid"
 exit
exit

%endif%

%if% available "assembly-gatewayscript"

assembly-gatewayscript "mq-invoke"
 title "MQ Invoke"
 gatewayscript-location "local://js/mq-invoke.js"
exit

%endif%


%if% available "api-rule"

api-rule "mq-invoke"
 action mq-invoke
exit

%endif%

%if% available "assembly"

assembly "mq-invoke"
 rule mq-invoke
exit

%endif%

%if% available "assembly-function"

assembly-function "mq-invoke"
 title "mq-invoke"
 parameter
   name "qmgrobj"
   label "MQ QMGR Object"
   description "The MQ QM Object"
   value-type string
 exit
 parameter
   name "queue"
   label "Queue"
   description "The Queue to be used"
   value-type string
 exit
 parameter
   name "boq"
   label "Back Out Queue"
   description "Back Out Queue"
   value-type string
 exit
 parameter
   name "queue"
   label "Queue"
   description "The Queue to be used"
   value-type string
 exit
 parameter
   name "timeout"
   label "Timeout"
   description "Timeout"
   value-type string
 exit
 parameter
   name "structureid"
   label "StructureId"
   description "The structure Id"
   value-type string
   default "RFH"
 exit
 parameter
   name "version"
   label "Version"
   description "Version"
   value-type string
   default "MQRFH_VERSION_2"
 exit
 parameter
   name "encoding"
   label "Encoding"
   description "Encoding"
   value-type string
   default "MQENC_NATIVE"
 exit
 parameter
   name "codedcharsetid"
   label "CodedCharSetId"
   description "CodedCharSetId"
   value-type string
   default "MQCCSI_INHERIT"
 exit
 parameter
   name "flags"
   label "Flags"
   description "Flags"
   value-type string
   default "MQRFH_NONE"
 exit
 parameter
   name "format"
   label "Format"
   description "Format"
   value-type string
   default "MQSTR"
 exit
 parameter
   name "ccsid"
   label "Name Value CCSID"
   description "Name Value CCSID"
   value-type string
   default "1208"
 exit
 assembly mq-invoke
exit

%endif%


%if% available "apic-gw-service"

apic-gw-service
 user-defined-policies mq-invoke
exit

%endif%
```
</div>
### Gateway Script for the sample

<button class="collapsible" id="fulloutput">Gateway Script for the sample</button>

<div class="content" id="fulloutputdata" markdown="1">
```javascript
/*
      Licensed Materials - Property of IBM
      © IBM Corp. 2019
*/
var urlopen = require('urlopen');


var counter = 0;

function APICMQErrorHelper(name, message, code) {

    if (!code) {
        code = 400;
    }
    context.set("message.status.code",code)
    context.set("mess age.status.reason",name)
    context.set("message.body",message)
}

function NoQueueFoundException(responseCode, queue) {
    return APICMQErrorHelper("NoQueueFoundException", "APICMQ001 : Response code '" + responseCode + "' was received when connecting to a either a request or response queue . Please check the Queue name is correct.", 404);
}

function NoQueueManagerFoundException(queueManagerObjectName) {
    return APICMQErrorHelper("NoQueueManagerFoundException", "APICMQ002 : API Connect was unable to find a QueueManager Object with the name '" + queueManagerObjectName + "'", 404);
}

function ResponseTimeOutException() {
    return APICMQErrorHelper("ResponseTimeOutException", "APICMQ004 : A response was not received in the given time. ", 408);
}

function InvalidSOAPResponse(SOAPResponse) {
    return APICMQErrorHelper("InvalidSOAPResponse", "APICMQ005 : Invalid SOAP Response  : Please check the BackOut Queue for the message", 400);
}

function InvalidRequest(SOAPResponse) {
    return APICMQErrorHelper("InvalidResponse", "APICMQ006 : Error occured when reading the input was the inputData XML or JSON", 400);
}

function NoBOQ() {
    return APICMQErrorHelper("NOBackOutQueue", "APICMQ007 : No Backout Queue Specified", 400);
}

function MessageOnBoQ(data, response) {

    if (boq == '') {
        NoBOQ();
    } else {
        var h = response.get({
            type: 'mq'
        }, 'MQMD')

        var newBOC = h.MQMD.BackoutCount.$ + 1
        h.MQMD.BackoutCount = {
            $: newBOC
        }
        var options = {
            target: boqURL,
            data: data,
            headers: {
                MQMD: h,
                MQRFH2: MQRFH2
            }
        }
        urlopen.open(options, function(connectError, res) {
            if (connectError) {
                APICMQErrorHelper("ErrorPuttingMessageOnBO", connectError, 400);
            }
            console.error(res.get({
                type: 'mq'
            }, 'MQMD'));
            console.error(res)
        });
    }
}


function process(options) {
    console.error(options);

    try {

        urlopen.open(options, function(connectError, res) {
            if (res) {
                console.error('Received MQ ' + res.statusCode + ' for target ' + options.target);
            }
            if (connectError) {
                NoQueueManagerFoundException(qm)
            } else if (res.statusCode === 0) {
                console.error("Message on Queue");
                console.error(options);
                if (respq == '') {
                    var mqmd = XML.parse(res.get('MQMD'));
                    console.debug(mqmd);
                    context.set("message.body",mqmd);
                } else {
                    res.readAsXML(function(readAsXMLError, xmlDom) {
                        if (readAsXMLError) {
                            res.readAsJSON(function(readAsJSONError, jsonObj) {
                                if (readAsJSONError) {
                                    res.readAsBuffer(function(readAsBufferError, buffer) {
                                        console.error("Unable to read response as XML or JSON");
                                        if (!readAsBufferError) {
                                            MessageOnBoQ(buffer, res);
                                            InvalidSOAPResponse();
                                        } else {
                                            InvalidSOAPResponse("Error : " + readAsBufferError);
                                        }
                                    });
                                } else {
                                    console.error(jsonObj);

                                    context.set("message.body",jsonObj);
                                }
                            });
                        } else {

                            context.set("message.body",xmlDom);
                        }
                    });
                }
            } else if (res.statusCode === 2085) {
                NoQueueFoundException(2085, reqq)
            } else if (res.statusCode === 2059) {
                NoQueueManagerFoundException(qm)
            } else if (res.statusCode === 2033) {
                ResponseTimeOutException()
            } else {
                if (counter > 4) {
                    res.readAsBuffer(function(readAsBufferError, buffer) {
                        console.error("Attempting to parse the response message to put on the BackOut Queue");
                        if (!readAsBufferError) {
                            MessageOnBoQ(buffer, res.headers);
                        }
                    });

                    var errorMessage = 'Thrown error on urlopen.open for target ' + options.target + ':   statusCode:' + res.statusCode
                    APICMQErrorHelper("Unknown Error", errorMessage, 400)
                } else {
                    counter++;
                    console.error('Failed to put message on to Queue Retry: ' + counter + ' of 5');
                    process(options);
                }
            }

        });
    } catch (error) {
        var errorMessage = 'Thrown error on urlopen.open for target ' + options.target + ': ' + error.message + ', error object errorCode=' + error.errorCode.toString();
        APICMQErrorHelper("Unknown Error", errorMessage, 400)
    }
}


var qm = context.get('local.parameter.qmgrobj')
var boq = context.get('local.parameter.boq')
var reqq = context.get('local.parameter.queue')
var respq = context.get('local.parameter.replyqueue')
var timeout = context.get('local.parameter.timeout')

// console.error("*******************")
// console.error(qm)
// console.error(boq)
// console.error(reqq)
// console.error(respq)
// console.error(timeout)
// console.error("*******************")

var mqURL = "unset"
var MsgType = -1;
var ReplyToQ = "";
if (respq == '') {
    MsgType = 8
    mqURL = 'dpmq://' + qm + '/?RequestQueue=' + reqq + ';timeout=' + timeout
} else {
    MsgType = 1
    ReplyToQ = respq
    mqURL = 'dpmq://' + qm + '/?RequestQueue=' + reqq + ';ReplyQueue=' + respq + ';timeout=' + timeout
}
var boqURL = 'dpmq://' + qm + '/?RequestQueue=' + boq + ';timeout=' + timeout

var MQMD = {
    MQMD: {
        MsgType: {
            "$": MsgType
        },
        ReplyToQ: {
            "$": ReplyToQ
        },
        Format: {
            "$": 'MQHRF2'
        }
    }
}
// '<MQMD>' +
//    '<StructId>MD</StructId>' +
//    '<Format>MQHRF2</Format>' +
//    '<MsgType>' + MsgType + '</MsgType>' +
//    '<Persistence>1</Persistence>' +
//    '<ReplyToQ>' + ReplyToQ + '</ReplyToQ>' +
//    '</MQMD>'
//


// var MQRFH2 = '<MQRFH2>' +
//     '<Version>' + props.vrsn + '</Version>' +
//     '<Format>' + props.format + '</Format>' +
//     '<StrucId>'+props.structid+'</StrucId>'+
//     '</MQRFH2>';
var MQRFH2 = {
    MQRFH2: {

        StrucId: {
            "$": context.get('local.parameter.structureid') || "RFH"
        },
        Version: {
            "$": context.get('local.parameter.version') || "MQRFH_VERSION_2"
        },
        Format: {
            "$": context.get('local.parameter.format') || "MQSTR"
        },
        Encoding: {
            "$": context.get('local.parameter.encoding') || "MQENC_NATIVE"
        },
        CodedCharSetId: {
            "$": context.get('local.parameter.codedcharsetid') || "MQCCSI_INHERIT"
        },
        Flags: {
            "$": context.get('local.parameter.flags')|| "MQRFH_NONE"
        },
        NameValueCCSID: {
            "$": context.get('local.parameter.ccsid')|| "1208"
        }
    }
}

var outputObject = {};

//Read the payload as XML

process({
    target: mqURL,
    data: context.get('message.body'),
    headers: {
        MQMD: MQMD,
        MQRFH2: MQRFH2

    }
})
```
</div>
