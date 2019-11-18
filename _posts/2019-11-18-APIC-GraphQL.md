---
layout: post
date: 2019-11-18 00:01:00
categories: APIConnect
title: "API Connect 2018 and GraphQL"
author: ["IvanPryanichnikov"]
---
I’m often asked whether IBM API Connect supports GraphQL APIs. The short answer is “yes” but let’s have a deeper look at the topic.

<!--more-->

First, some theory about GraphQL.

GraphQL is a data query language for APIs developed by Facebook in back 2012 and released publicly in 2015. This allows clients to write queries that precisely control which resources to retrieve from or to write to the server.

Basically GraphQL allows to replace multiple (sometimes tens or even hundreds) REST API methods or calls with just one endpoint that would allow you to get all information you need from the server.

See [here](https://developer.ibm.comopenprojectsopenapi-to-graphql) and [here](https://graphql.org) for more information about GraphQL.

IBM API Connect supports GraphQL queries via the Loopback [OpenAPI-to-GraphQL](http://v4.loopback.iooasgraph.html)package. The package allows to easily create a GraphQL wrapper for your existing REST endpoints and then manipulate data using the GraphQL queries.

![](/images/graphql1.png)

API Connect then used for API Management purposes for the backend interfaces:


In the example below I'll be using the Loopback Family Tree [application](https:////github.comstronglooploopback4-example-family-tree#openapi-to-graphql) running in a VM in my sandbox environment exposed via API Connect v2018.x.

I've already exposed the API on the API Gateway using IBM API Connect:

![](/images/graphql2.png)

First let's invoke it using REST providing my Client ID in the request header for identification on the API Gateway:

![](/images/graphql3.png)

![](/images/graphql4.png)

Now let's add a GraphQL server to the picture so I can use queries instead of REST requests to get data from the server:

![](/images/graphql5.png)

My GraphQL server is running on the same host with my FamilyTree application. In order to point the GraphQL wrapper to my gateway endpoint (instead of the _localhost_ one used by default) it's required to update my application's JSON file providing the gateway IP and port:

![](/images/graphql6.png)

And restart the library pointing it to the updated file:

```
mbp-ivan-2:~ ivanpran$ _openapi-to-graphql ivanpranapicgraphqlfamilytreeapp.json_
```

Now GraphQL server will send queries to the endpoint exposed from the API Gateway instead of _localhost_.

Since APIs exposed from the gateway use https scheme and I'm using self-signed certificates in my sandbox, I want first to allow connections to untrusted servers by using the following commands:

```
mbp-ivan-2:~ ivanpran$ export NODE\_TLS\_REJECT\_UNAUTHORIZED=0
mbp-ivan-2:~ ivanpran$ echo $NODE\_TLS\_REJECT\_UNAUTHORIZED
0
mbp-ivan-2:~ ivanpran$
```

and restart my GraphQL server.

Now, I'm finally ready to send a GraphQL query to the REST API exposed using IBM API Connect

![](/images/graphql7.png)

And here is the API Connect Analytics view:

![](/images/graphql8.png)

If your target endpoint requires additional headers eg. X-IBM-Client-Id you can use the [OpenAPI-to-GraphQL CLI](https:////github.comIBMopenapi-to-graphqltreemasterpackagesopenapi-to-graphql-cli#usage) to pass them using the -H option.

In the example above, we used the Loopback [OpenAPI-to-GraphQL](http://v4.loopback.iooasgraph.html)package to create a GraphQL wrapper for the REST API exposed via IBM API Connect.

Due to the nature of GraphQL and depending on the structure of the GraphQL interface, it's important to have an API Management solution that understands GraphQL and is able to limit access to the endpoints based on the complexity of a query.
