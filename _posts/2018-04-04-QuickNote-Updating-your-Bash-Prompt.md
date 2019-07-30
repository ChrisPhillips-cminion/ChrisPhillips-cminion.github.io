---
layout: post
date: 2018-04-04  00:00:00
categories: APIConnect
title: 'QuickNote: Updating your Bash Prompt'
---

There are a million guides out there but as I always googled this I
thought I would post the answer here.

Simple set the PS1 environmental variable in to .bashrc
or .bash\_profile

```
PS1=’#[\D\] $(whoami)\e[0m \e[1m$PWD$/ \e[0m >>> ‘
```

this gives me

> \#\[2018--04--04 08:45:21\] cminion /home/cminion\$/ \>\>\>

Where

```
\D\ -  provides the date
$PWD$ - provides the pwd output
whoami - provides the current user
```

Note: that if you use commands like date or pwd in there it will take
the first value when the PS1 is set (i.e. when a new bash prompt is
opened).





By [Chris Phillips](https://medium.com/@cminion) on
[April 4, 2018](https://medium.com/p/74f93e3ec04).

[Canonical
link](https://medium.com/@cminion/quicknote-updating-your-bash-prompt-74f93e3ec04)

Exported from [Medium](https://medium.com) on April 6, 2019.
