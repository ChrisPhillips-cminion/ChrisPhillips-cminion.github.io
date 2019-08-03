---
title:  MQ in Docker, removing the tie to the QMGR Process - Docker Staying Alive
layout: post
date:   2017-07-17 00:00:00
categories: APIConnect
---
<!--more-->

So recently Aiden Gallagher (Another IBM Intergration SME) and I were
trying to do API Connect in BM integration with an MQ Docker instance
also running in BM, with SSL.

I am by no means an MQ expert and we found that when ever we restarted
the MQ QMGR it would kill the docker container. This was because the
container was written in such a way that when the QMGR process ends the
container shuts down.

Now there are a number of good reasons for this however it is
infuritating at times!

So I forked the IBM MQ Docker and made some minor changes. You can see
my fork here.


[**ChrisPhillips-cminion/mq-docker**\
*mq-docker - Sample Docker image for IBM®
MQ*github.com](https://github.com/ChrisPhillips-cminion/mq-docker "https://github.com/ChrisPhillips-cminion/mq-docker")[](https://github.com/ChrisPhillips-cminion/mq-docker)


The key things I changed.

1.  [I added a keep alive function. This is runs mq.sh that monitors the
    QM t then runs a while 1 loop to ensure the process does not
    end.]

```
#!/bin/bash
```

```
mq.sh
while true; do
  echo "sleeping for 100000s"
  sleep 100000
done
```

2\. I modified mq-monitor-qmgr.sh to remove the checks to wait for the
process to end. I.e. I commented line 38 onwards out.

3\. I modified the DockerFile to run keepalive.sh not mq.sh i.e. i
changed the last line to the following

```
ENTRYPOINT ["keepalive.sh"]
```

4\. (Optional) I created a run.sh that would clean up, build, start and
tail the logs of a container.

```
docker rm -f $(docker ps -qa)
docker build -t cminion/mq .
docker run \
  --env LICENSE=accept \
  --env MQ_QMGR_NAME=QM1 \
  --publish 1414:1414 \
  --publish 9443:9443 \
  --detach \
  --name mq cminion/mq
docker logs -f mq
```

Thats it! Now just to work out how to enable SSL!





By [Chris Phillips](https://medium.com/@cminion) on
[July 17, 2017](https://medium.com/p/9197ca0fafc3).

[Canonical
link](https://medium.com/@cminion/mq-in-docker-removing-the-tie-to-the-qmgr-process-docker-staying-alive-9197ca0fafc3)

Exported from [Medium](https://medium.com) on April 6, 2019.
