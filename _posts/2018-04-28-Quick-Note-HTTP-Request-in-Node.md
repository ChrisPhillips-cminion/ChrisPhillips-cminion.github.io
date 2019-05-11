---
layout: post
date: 2018-04-28  00:00:00
categories: APIConnect
title: Quick Note HTTP Request in Node
---

Quick Note HTTP Request in Node 
===============================

 
I am only posting this because every time i need to do one I end up
googling it.


 
 
 

------------------------------------------------------------------------


 
 
### Quick Note HTTP Request in Node 

I am only posting this because every time i need to do one I end up
googling it.

``` 
var request = require('request');

var options = {
  url: 'https://api.github.com/repos/request/request',
  headers: {
    'User-Agent': 'request'
  }
};

function callback(error, response, body) {
  if (!error && response.statusCode == 200) {
    var info = JSON.parse(body);
    console.log(info.stargazers_count + " Stars");
    console.log(info.forks_count + " Forks");
  }
}

request(options, callback);
```

Taken from <https://github.com/request/request>





By [Chris Phillips](https://medium.com/@cminion) on
[April 28, 2018](https://medium.com/p/b7879d7b2d2e).

[Canonical
link](https://medium.com/@cminion/quick-note-http-request-in-node-b7879d7b2d2e)

Exported from [Medium](https://medium.com) on April 6, 2019.
