---
layout: post
date: 2024-08-23 10:00:00
categories: APIConnect
title: "Runing Asynchronous code in API Connect Gatewayscript policy"
---

A client asked how they can make two invokes in API Connect asynchronous.  This is not possible with the invoke policies as they must always be synchronous. However it can be done with   JavaScript/GatewayScript.

<!--more-->

**Thanks to Steve Linn for pointing out how obvious this was.**

The code below is a very simple snippet. This gateway script has two Promises. The first sleeps for ten seconds and prints out a message to the log. The second sleeps for two seconds and prints out a message to the log.

Finally we have a `Promise.all()` that waits for both promises to complete.

```javascript
let promise1 = new Promise((res) => {
        setTimeout(()=>{
          console.error('done 1');  
          res()
        }, 10000);
})
let promise2 = new Promise((res) => {
        setTimeout(()=>{
          console.error('done 2');  
          res()
        }, 2000);
})

Promise.all([promise1, promise2])
  .then((responses) => {
      console.error('done');
  })
  .catch((error) => {
    console.error(`Failed: ${error}`);
  });
```

By taking the above code and replacing the `setTimeout()` with URL Opens we can meet the clients requirements to asynchronously call two downstream services.
