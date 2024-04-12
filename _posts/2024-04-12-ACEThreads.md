---
layout: post
date: 2024-04-12 09:00:00
categories: ACE
title: "Additional Flow Instances in IBM ACE"
author: [ "BenCornwell" ]
---
*This was originally published on 3rd October 2022 on IBM Community. Republished with permission from author*


It is a common mistake to simply add more resources to a system to get more performance. For example, one might enlarge the thread pools and database connection pools, assuming more threads can do more work and therefore process more messages.   This can be true up to a point, but beyond that it may result in no performance increase, or even significantly reduced performance.  This article attempts to describe a situation where these two things can happen.

## Introduction to Flow Instances
IBM App Connect Enterprise (ACE) via the toolkit allows the developer to create message flows that contain nodes that process the message step by step, along with logical constructs.  The flow represents code, and a flow instance  runs this code.  A flow instance is single-threaded, so to gain multiple threads, the flow can be configured with additional instances.  These are an addition to the default one, so to configure ten simultaneous execution threads for a flow, additional instances should be set to 9.



Additional instances can be configured to be created when the integration server starts (using the “Create additional instances when flow starts” option under Workload Management); or on-demand.  If they are configured to be created on demand, then if the instances later become disused they will be destroyed and their resources freed (the only caveat is some memory used by an instance being destroyed is not handed back to the OS) .  When configured this way it can be thought of as similar to a thread pool that can grow and shrink, and the additional instances property is effectively the maximum pool size.



## Asynchronous Flows and Threading
### How many threads do I need?


**NB this description is simplified, but generally holds true.**

It is a common design for an ACE flow to be triggered by reading a message from a message queue .  This is asynchronous processing, because the message is not necessarily processed as soon as it is written to the queue, but perhaps some time later.  If the messages are written to the queue faster than they are read from it, messages will be queued up.  The number of messages waiting on the queue to be consumed will go up - or in other words, the queue depth will increase.

How fast messages are read from the queue depends on how fast the message flow reading it can process.  Consider the following flow:

![](/images/ben1.png)

The flow starts after the message is read from MQ.  Then some transformation is  done in memory, a CPU intensive operation, then the message is written to a database, in this case via a mapping node.  The message is sent over a network connection to the database and ACE waits for a response from the database before it can conclude the flow. Writing to the database within this node is a therefore a synchronous operation.  The thread running the flow will sit idle (or block) until a response is received from the database.

The operating system on which ACE is running will have many threads in existence at the same time, but most will be idle.  However, if the machine has one logical CPU it can only run one thread at a time.  If multiple threads are actively running (not idle or waiting), it will split its time between each thread.  Now, looking at the example flow above, let’s assume that the transformation takes 10ms and the database write also takes 10ms.  That means that one run of the flow would take 20ms but the CPU would be idle for half that time.  If there is one flow instance (which means one thread) then it would be picking up messages and processing them continuously but the CPU utilisation would show as 50%.  In this simple scenario, we don’t want to be paying for the CPU to be idle, so we can add an additional flow instance and run two flows at the same time.

If the transformation node  takes 10ms and the database call takes 10ms, that means a single flow instance can process 50 transactions per second.  But we have two flow instances, so that means 100 transactions per second for the single CPU (assuming the database can handle that level of traffic without slowing down).  This way we can process twice as many messages on a single CPU and the CPU utilisation will show as 100%.

NB: It should be pointed out that we may not want CPU to be at 100% on each CPU.  A traditional ACE installation might have two servers for redundancy, and each one might have say eight cores.  If the servers are running in an active/active configuration (two servers running all the time sharing the load) to provide redundancy then each server should only be running at around 50% load, so that if one fails the other can process all the messages.  Similarly, if three servers are running then each could be running at 66% load based on the assumption that only one server is likely to fail at once.  However, if ACE is running in Kubernetes and a pod fails there might only be a short disruption whilst the pod is restarted.  In an asynchronous application then the queue would simply back up for a short time and be drawn down again once the failed pod is back up.  In that context, running close to 100% might be suitable depending on how much processing delay is acceptable.

##  # What happens if we add even more flow instances?
Let’s assume that there are 66 transactions being placed on the queue every second.  Assuming we are running on Kubernetes then one pod with a single CPU is enough to handle the load and our queue depth will not grow.  What will happen if we add more flow instances?

 The answer is – nothing.  We will still process 66 transitions per second because that’s all that’s arriving; but we will have three threads, one of which will be idle for some of the time.  But as we said earlier, the flow instance still consumes memory and resources.

Now what happens if, in one second 100 transactions arrive?  Two flow instances can still only process 66 transactions per second, and in that second only 66 transactions will be processed leaving a queue depth of 34.  And if we go back to 66 transactions per second, the queue depth will still be 34.  It won’t be the same 34 transactions, of course, but each transaction will now be on the queue for slightly longer.  Throughput will stay at 66 TPS but the time taken for a transaction to go through the system will be greater (1.5 seconds instead of 1).

If we have three flow instances however, what happens in this case depends on what our CPU utilisation is.  If our pod was running at 100% CPU utilisation then an additional thread will not result in more messages being processed, because there are no more CPU resources to use.  However, if the pod CPU was 66% or lower, then the additional flow instance will be able to use that spare 34% and the que depth will drop back down – the backlog will be processed by the additional instance.

So in that case, adding a third flow instance will enable the system to handle temporary increases in incoming messages without the queue depth backing up, and the time each transaction spends waiting to be processed will be reduced.

### What happens if the database slows down?
Consider a different scenario in which the database slows down to the point where the database call now takes 20ms.  That means that each flow will take 30ms to complete.  But since the thread is idle whilst waiting for the database call to complete each thread is only busy and using CPU for 33% of the time.

In our previous example where the flow took 20ms of which 10ms was the database call, the maximum possible throughput was 100 transactions per second with 100% CPU utilisation.  Now if we have two flow instances, they will only be able to process at most 66 transactions per second because each thread has to wait longer; but even then, the CPU utilisation will only be 66%.  There is therefore room to ‘fit’ another thread in.  If we add a third instance, throughput will go back up to 100 TPS, and CPU utilisation will go up to 100%.  Adding a third instance now will increase throughput, the queue depth will stay low, and consequently latency will be kept low.

In this case it might be a good idea to create three flow instances anyway – that way, if the database does slow down the third flow instance will be able to start processing messages and keep the queue depth low; but if not, then the thread will sit idle, consuming some memory, but not affecting performance.

## Database Connections in ACE
It might seem like additional instances can be set to a high value without a problem, but this is not necessarily the case because of how database connectivity works in ACE.  Connections can be made two ways – ODBC or JDBC – depending on the node.

ODBC connections are tied to a flow instance. They can be opened when the flow instance is created (which in turn can be on-demand or when the integration server starts) in which case they stay open; or they can be opened when they are first used in a flow and will be closed when they have been idle for one minute (this is always the case on z/OS).
JDBC connections are managed by a connection pool. A connection pool opens a specified number of connections when the server starts (the initial pool size).  When a flow needs to make a database call it will obtain an existing connection from the pool, make the call, and then the connection is returned to the pool. If the pool does not contain enough connections for the threads that require them, it will create more; conversely if there are connections in the pool that remain unused for a specified time (the idle timeout), they will be closed.
The important thing to remember is that **opening a database connection is an expensive operation** in terms of resources on the database server; and the use of TLS can further increase the time and CPU resources needed.

When using ODBC, this means that if additional instances are set to be created on demand i.e. during operation, then ODBC connections will be created at the same time. So creating flow instances will take a relatively long time.

In the case of JDBC, if an additional instance is created on demand and uses a JDBC connection one will be obtained from the pool.  If the connection is no longer needed after some time, and the connection is idle beyond a defined idle timeout value, it will be destroyed.  This is a good idea in terms of saving memory on both the database server and the ACE integration server when load varies a lot over time; however care must be taken to understand how they will be re-opened.

## What Can Go Wrong?
### Large batches of messages
Let’s consider what happens when a large batch of messages is placed on the queue all at once.  In our example, when our single CPU is running at 100% or even 66% load, this is bad news as the large batch will not be cleared from the queue very quickly, or even at all.  We should size our integration server accordingly.

For the base load of 100 messages per second we would need two instances and at least one CPU.  But if we can expect 1000 messages to be dumped at once, we can provide more resources to process them. How many we need depends on how quickly we want the messages processed.  There are 1000 excess messages on top of the 100 per second normal load.  If our pod has two CPUs available and we allocate four instances, we can utilise both CPUs at 100% and the second CPU will take ten seconds to process all the messages.  If our pod has eight CPUs available, the backlog will still take ten seconds if four instances are available whilst the normal load is still being processed.  But then we could make sixteen instances available if we want, this would in theory clear the backlog in less than one second.  But remember, if we are using ODBC or a JDBC connection pool with default settings, this will need fourteen new database connections all opened at the same time.  This places a significant extra load on the database server, which will slow it down further.

## Database Slowdown
Another possibility is that our database slows down due to some other condition – another application executes a very large query, for example.  In this situation, our original two-flow instances would each pick up a message, send it to the database, and wait.  Whilst they are waiting, more messages are available, so the integration server creates another instance, which picks up a message, which then has to wait to complete, and so on.  The more flow instances that are created, the more connections are made to the already over-loaded database, which overloads it further.  This leads to a runaway condition that will continue overloading the database until the maximum possible threads are created.

## Too many instances
In both these scenarios, the creation of too many instances and their associated database connections creates a performance bottleneck.

The important question in this scenario is as follows: When a large batch of messages is received, how quickly do they need to be processed?  Remember that this is an asynchronous application, so being able to queue messages like this is a key benefit.  It is likely that the batch does not need to be processed straight away, and that four flow instances is enough. More do not offer any practical benefit, but they do add the risk of overloading the system.  If the additional instances property is set to a very high number, this could cause a significant pause in processing.  It will only ease when the maximum additional instances is reached.  The higher the number the greater the load on the database.

Whilst this pause is happening of course, more messages continue to arrive on the queue.  These messages would normally be processed in one second, but now they will have to wait for the database to start responding quickly again and then for the backlog to clear.  They could be delayed for a significant time.

# Good Practices
Additional flow instances can be configured to be created when the flow starts.  Generally speaking, for flows that have external resources, e.g. database connections, this should be selected so that all flows and their associated database connections are created.  Additionally, if using JDBC, the initial pool size should be the same as the total flow instances (additional instances plus one) and the connection timeout should be set to the maximum value of 100000000 seconds to ensure the connections remain open.

If transient peaks in load are expected, consider sizing the integration server to accommodate enough instances to process the peak load in a reasonable amount of time, and setting the flow instances to be created on startup.  For many batch applications, the allowable times to process the batches are quite generous and measured in hours.  If a batch arrives every hour, then it may only be necessary to ensure processing has completed in good time before the next batch arrives, so the integration server should be sized to process the batch in say 30 minutes.

If batches are infrequent – at random times or say, weekly – then it may be tempting to configure the instances to be created on demand (and by association destroyed when unused). But remember that memory can be released back to the integration server when not used by flow instances, but it cannot be released back to the OS.  That means that a Kubernetes pod will not reduce its RAM footprint.  In that situation, consider keeping the JDBC connection pool at the peak value by setting a high initial timeout and a maximum idle timeout, providing the database server can handle that many idle connections.  This avoids having to create large numbers of connections at times of peak load.

# Summary
Using more flow instances than the CPU can cope with does nothing except waste memory.
Setting high numbers of flow instances and not selecting ‘create flow instances on start-up’ can cause bottlenecks when large numbers of messages arrive because large numbers of flows are created all at once. If these flows need external resources e.g. database connections, this can overload that resource.
Unless you have good reasons not to, set JDBC connection timeout to the maximum value of 100000000. It is cheap to maintain idle DB connections but expensive to create them once destroyed.
Set the additional instances to the level that will process batches in the time you have available. Creating more instances will consume more CPU and memory, and there may not be any benefit to completing the batch quicker.
