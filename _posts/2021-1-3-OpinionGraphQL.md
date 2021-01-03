---
layout: post
categories: APIConnect
date: 2020-11-30 00:14:00
title: API Gateway what's the difference -  V5c, Native and V5e
draft: true
---
What I did on my Xmas Holidays - GraphQL ? An Opinion Piece


I have been an Integration SME for the majority of my career. I was cynical when I first saw GraphQL come around. As I have seen more and more people declare they want to use it I decided to spend some time over Christmas not just learning it but actually applying it to an application used by a few hundred people. **This is not going to be another introduction to graphql or even graphql with IBM software, rather my initial impressions of it.**

<!--more-->

## TLDR
GraphQL is a great tool in your toolbox, but use it for the right purpose and dont assume it can be your only API Strategy.

## Background
Outside of work I founded and run a free to enter 220 person tournament for a card came called KeyForge. This game is a physical card game that I started playing and often play on my travels to customers around the world. I started this event to encourage people I played with around the world to face off against each other. There is an online platform call https://theCrucible.online that allows people to play with their real decks online. (Yes its like Magic The Gathering and has the same creator)

## Background tech
In order to run this website I store all of my data in google sheets (for my sins) and over the course of Christmas I rewrote my application as a microservice "ish"  implementation. When I say Microservice I mean I split it into a handful core applications that each has its own role and responsibility.   I also took this opportunity to learn Svelte as frontend framework.

There are six core applications
* KOTE-DataSource-Sheets
* KOTE-Directory
* KOTE-Draw
* KOTE-Left
* KOTE-Jam
* KOTE-Search

INSERT DIAGRAM FOR THE ABOVE

### Rules of engagement
I started with these guiding principles
* DataSource-Sheets is  only exposed as graphQl
* Each Front End page must not call more then two endpoints to render its information
* No page must take longer then 2 seconds to load
* No state is stored in the application itself, the Data-source will reload itself every 15mins to pick up the latest results. (All data is inputted with google forms)


## What I actually did

The KOTE-DataSource-Sheets (SOR) pulls all of the data in from google sheets, and proceses it into a centralised model. This model is used by other components. The model is then exposed via GraphQL.

The KOTE-Directory (front end) was originally designed to be call the GraphLQ endpoint on the KOTE-DataSource-Sheet and render the information.  I quickly discovered that I needed to do a lot of processing of the data I am getting from GraphQL in order to make it renderable.  As GraphQL has no join facility today (as far as I can see) it would be multiple calls worsening the user experience. To get around this I added the KOTE-Jam layer between the KOTE-Directory and KOTE-DataSource-Sheets, allowing this post processing to occur on the server side.

The KOTE-Jam layer makes GraphQL calls to the KOTE DataSources-Sheets then does post process and joining of the data so it can serve up  the required data in a single call.  

The KOTE-Search uses fuse (Thanks Ritchie) to provide a fuzzy logic search on data that is populated via GraphQL from the DataSource.

The KOTE-Left calls KOTE-Jam to simply analyses the results and reports to discord the games that are not yet complete.

THe KOTE-Draw calls the GraphQL endpoint and simplifies the round pairing


## So what did I think
My opinion of the usefulness of GraphQL has changed multiple times in the two weeks I have been using it. GraphQL does what it says it does. It simplifies data exposure to consuming applications. However it does not make APIs easier to consumer, just expose. As I have written for a public API approach to be successful it must be easy to consume, usually this means exposing APIs to achieve a use cases with minimal calls and minimal knowledge of the expansive data model. ([https://chrisphillips-cminion.github.io/api/2019/05/28/APIFlavours.html](https://chrisphillips-cminion.github.io/api/2019/05/28/APIFlavours.html)) I would say GraphQL is not an API but rather a completely different beast to simplify the separation of responsibilities in estates..

If challenged I would do this again. GraphQL provided me a way to cleanly separate out the data processing logic for the front end way from the the data source itself. I believe this allowed for a much quicker and better quality application and it  forced me to work in a standard patterns when accessing the data.  In addition if I needed to add any additional functions  I can do it with minimal risk as I will not need to change the existing components, rather adding new components to provide the need.

## Bottom Line
GraphQL is a great tool in your toolbox, but use it for the right purpose and dont assume it can be your only API Strategy.
