---
layout: post
date: 2019-06-09 10:00:00
categories: Home Dashboard
title: 'Home Dashboard Part 1 - My Location'
---
I travel a lot for work, rough 75% of weeks I am away, often out of the country.

My kids always want to know where I am and my wife wanted a home dashboard so we can quickly check useful things.

I will do another post on the dashboard aims, objectives and architecture but today I wanted to find a way to get my location data and share it.

I have an Iphone and I found a brilliant wrapper for node js module [find-my-iphone](https://www.npmjs.com/package/find-my-iphone).

This lets you take a username and password and then you can query for your location data. My sample code is below.

```
var icloud = require("find-my-iphone").findmyphone;
var sleep = require("sleep");
var mqtt = require('mqtt')
console.log("Connecting")
var client  = mqtt.connect('mqtt://10.200.0.7:1883')

icloud.apple_id = "<username>"
icloud.password = "<password>";
icloud.getDevices(function(error, devices) {

        var device;
        if (error) {
                throw error;
        }
        console.log("devices")
        //pick a device with location and findMyPhone enabled
        devices.forEach(function(d) {
                var pl = {}
                pl.name = d.name
                pl.battery = d.batteryLevel

                if (d.location) {
                        pl.lat = d.location.latitude
                        pl.lng= d.location.longitude
                }
                console.log(pl)
                client.publish('location', JSON.stringify(pl), { retain: true });

        });
        client.end()
});
```

I wanted to send the location to MQTT as my dashboard will pick up all info from there. This puts the following message on to MQTT.

```
{ name: 'McRandomette',
  battery: 0.33000001311302185,
  lat: 123.05935783402577, //changed so as not to show my location
  lng: 123.05935783402577  //changed so as not to show my location
}
```

### Working around the annoyances

If you have tested this you may realise that every time the script is invoked it sends an alert to the iCloud account you are logging in with. This is not suitable if i want the script to run every ten minutes.

To get around this you must create a new iCloud account and add it to the same iCloud family. The new account will now be able to query all devices in the family.  As this is a benign account the notifications are ignored.

### Next Steps
* Dockerise this script and turn it into a kuberentes job
* Build my dashboard
