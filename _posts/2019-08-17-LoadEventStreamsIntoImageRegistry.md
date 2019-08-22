---
layout: post
date: 2019-08-17 12:00:00
categories: EventStreams
title: "NodeJS to IBM Event Streams - 101"
draft: true
---

_"IBM Event Streams is a high-throughput message bus built with Apache Kafka. It is optimized for event ingestion into IBM Cloud and event stream distribution between your services and applications"_ Taken from [https://cloud.ibm.com/catalog/services/event-streams](https://cloud.ibm.com/catalog/services/event-streams)

<!--more-->

This guide shows how to write your first NodeJS application to be a producer or consumer. This article is based on the official sample provided here [https://github.com/ibm-messaging/event-streams-samples/tree/master/kafka-NodeJS-console-sample](https://github.com/ibm-messaging/event-streams-samples/tree/master/kafka-NodeJS-console-sample) i.e. all the sample code is from there.

# Register a client

First of all we need to register a client with IBM Event Streams to get the APIKey and SSL Certificate.

1.  Log into IBM Event Streams
2.  Click on Connect to this cluster.
3.  Make a note of the Bootstrap Server
4.  Download the PEM Certificate
5.  Enter a name for the Application
6.  Select which permissions the NodeJS application requires
7.  Select which topics the NodeJS application is allowed to connect to.
8.  Click Generate API Key
9.  Make a note of the API Key, if you do not do this here you will need to reset it.

# Starting the NodeJS Application

This article is built around the `node-rdkafka` npm library.

1.  `mkdir ibm-es-nodejs`
2.  `npm init`
3.  `npm i --save node-rdkafka`
4.  create `index.js`

# Common Code

Starting off with the global code we need for both Producer and Consuming.

```javascript
var Kafka = require('node-rdkafka');
var driver_options = {
    //'debug': 'all',
    'metadata.broker.list': '<Bootstrap Sever address>',
    'security.protocol': 'sasl_ssl',
    'ssl.ca.location': '<Path to the PEM certificate downloaded>',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'token',
    'sasl.password': '<API Key>',
    'broker.version.fallback': '0.10.0',
    'log.connection.close' : false,
    'client.id': 'Es-NodeJS-101'
};
var topicName = "<Topic Name>"
```

## Producer

Connecting as a Producer

```javascript
var producerTopicOpts = {
    'request.required.acks': -1,
    'produce.offset.report': true
};
producer = new Kafka.Producer(producer_opts, producerTopicOpts);
producer.setPollInterval(100);
// Register listener for debug information; only invoked if debug option set in driver_options
producer.on('event.log', function(log) {
    console.log(log);
});
// Register error listener
producer.on('event.error', function(err) {
    console.error('Error from producer:' + JSON.stringify(err));
});

// Register delivery report listener
producer.on('delivery-report', function(err, dr) {
    if (err) {
        console.error('Delivery report: Failed sending message ' + dr.value);
        console.error(err);
        // We could retry sending the message
    } else {
        console.log('Message produced, partition: ' + dr.partition + ' offset: ' + dr.offset);
    }
});


// Register callback invoked when producer has connected
producer.on('ready', function() {
    console.log('The producer has connected.');

    // request metadata for all topics
    producer.getMetadata({
        timeout: 10000
    },
    function(err, metadata) {
        if (err) {
            console.error('Error getting metadata: ' + JSON.stringify(err));
            shutdown(-1);
        } else {
            console.log('Producer obtained metadata: ' + JSON.stringify(metadata));
            var topicsByName = metadata.topics.filter(function(t) {
                return t.name === topicName;
            });
            if (topicsByName.length === 0) {
                console.error('ERROR - Topic ' + topicName + ' does not exist. Exiting');
                shutdown(-1);
            }
        }
    });
    var counter = 0;
});

producer.connect()
```

 Send a message

```javascript
var message = new Buffer('Message I want to send');
var key = 'Key';
var partition = 0
// Short sleep for flow control in this sample app
// to make the output easily understandable
try {
    producer.produce(topicName, partition, message, key);
} catch (err) {
    console.error('Failed sending message ' + message);
    console.error(err);
}
```

## Consumer

```javascript
var topicOpts = {
    'auto.offset.reset': 'latest'
};

consumer = new Kafka.KafkaConsumer(consumer_opts, topicOpts);

// Register listener for debug information; only invoked if debug option set in driver_options
consumer.on('event.log', function(log) {
    console.log(log);
});

// Register error listener
consumer.on('event.error', function(err) {
    console.error('Error from consumer:' + JSON.stringify(err));
});

var consumedMessages = []
// Register callback to be invoked when consumer has connected
consumer.on('ready', function() {
    console.log('The consumer has connected.');

    // request metadata for one topic
    consumer.getMetadata({
        topic: topicName,
        timeout: 10000
    },
    function(err, metadata) {
        if (err) {
            console.error('Error getting metadata: ' + JSON.stringify(err));
            shutdown(-1);
        } else {
            console.log('Consumer obtained metadata: ' + JSON.stringify(metadata));
            if (metadata.topics[0].partitions.length === 0) {
                console.error('ERROR - Topic ' + topicName + ' does not exist. Exiting');
                shutdown(-1);
            }
        }
    });

    consumer.subscribe([topicName]);

    consumerLoop = setInterval(function () {
        if (consumer.isConnected()) {
            // The consume(num, cb) method can take a callback to process messages.
            // In this sample code we use the ".on('data')" event listener instead,
            // for illustrative purposes.
            consumer.consume(10);
        }    

        if (consumedMessages.length === 0) {
            console.log('No messages consumed');
        } else {
            for (var i = 0; i < consumedMessages.length; i++) {
                var m = consumedMessages[i];
                console.log('Message consumed: topic=' + m.topic + ', partition=' + m.partition + ', offset=' + m.offset + ', key=' + m.key + ', value=' + m.value.toString());
            }
            consumedMessages = [];
        }
    }, 2000);
});

// Register a listener to process received messages
consumer.on('data', function(m) {
    consumedMessages.push(m);
});]
consumer.connect()
```





**All Code taken from [https://github.com/ibm-messaging/event-streams-samples/tree/master/kafka-NodeJS-console-sample](https://github.com/ibm-messaging/event-streams-samples/tree/master/kafka-NodeJS-console-sample)**
