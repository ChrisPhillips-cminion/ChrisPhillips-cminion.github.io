---
layout: post
date: 2019-07-26 01:00:00
categories: IBMCloud
title: "ASCIINEMA - How to use it!"
draft: true
---
In a few articles I have used Asciinema. I am not affiliated anyway with this tool just a big fan.

_It is the youtube of the command prompt._

The service is free (As far as I have found). It allows you to record a terminal/bash session and upload it to their website. What it uploads is much smaller then a regular video.

### Installing the Application
It is in all good Package repositories. On a Mac with brew installed I simply ran
```brew install asciinema```

### Recording a session
The most common way method I use is the following.
```asciinema rec -t TITLE``` This will record the commands and their out put in the termianl session. Then, when you exit the session with `ctl+d` it gives  the option of uploading to their server where you can link to it. `TITLE` should replaced with the title of the video.

### Playing a session
After you have uploaded a video two URLs are provided. The first is a link to the video. The second is a link to take ownership of the video. If the video is not assinged to a user account it is removed after seven days.

If you do not want to watch the video from the website but instead watch it locally in your terminal run the following command.

```asciinema play <URL to asci cinema>```


### Emebedding the videon into markdown

This sample markdown code allows you to embeded a screenshot of the video which is a link to the video on ASCIINEMA. There is no way (as far as i know) to allow it to play on your webpage.
```markdown
[![asciicast](https://asciinema.org/a/zSkEqXvfHSN8I6Sb2UgHI0LwW.svg)](https://asciinema.org/a/zSkEqXvfHSN8I6Sb2UgHI0LwW)
```

Replace zSkEqXvfHSN8I6Sb2UgHI0LwW with the unique id given to your video


<hr>


For detailed information on the instructions and more visit their website and (https://asciinema.org)[https://asciinema.org]
