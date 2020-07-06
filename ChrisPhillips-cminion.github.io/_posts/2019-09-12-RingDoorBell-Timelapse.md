---
layout: post
date: 2019-09-12 01:00:00
categories: Home
title: "Timelapse and Taking Snapshots with a Ring Doorbell"
---

I recently bit the bullet and bought a ring doorbell pro. I have always wanted to do a timelapse over the year but something always got in the way. I did my research before deciding between NEST and RING and decided on RING simply because of the `ring-client-api` npm module.


<!--more-->

The first thing I did after installing it was to write a script to take a picture.

I used the great examples based here [https://www.npmjs.com/package/ring-client-api](https://www.npmjs.com/package/ring-client-api) as my starting point.

The following script saves a picture into the local directory when it is run.

<button class="collapsible" id="yaml2">Click here for the typescript.</button>

<div class="content" id="yaml2data" markdown="1">

```javascript
import * as fs from 'fs';
import * as Date from 'Date';
import 'dotenv/config'
import { RingApi } from 'ring-client-api'
import * as path from 'path'

async function snapshot() {
  const ringApi = new RingApi({
    // Replace with your ring email/password
    email: "email",
    password: "password",
    debug: true
  }),
    [camera] = await ringApi.getCameras()

  if (!camera) {
    console.log('No cameras found')
    return
  }

  console.log('Snapping a shot...')
  camera.getSnapshot(false).then(function(result) {

    fs.writeFile(Date.now()+'.png', result, (err) => {
      if (err) throw err;
      console.log('Lyric saved!');
    });

  })
}
snapshot()
```
</div>

Now this code was in place I needed to work out how to turn it into a timelapse generator.

I created a new container on my proxmox estate. Copied the code and set a cronjob to run every ten minutes

```cronjob
*/10 * * * *  cd ringPicture && node ../ring/index.js
```


This morning I ran the following commands to assemble a few seconds of video.

```sh
ls *png | sed -e s/^/files\ / > files.txt
ffmpeg -f concat -i files.txt output.mpeg
```
