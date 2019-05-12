---
title: Teaching my 7yo Daughter to Code
layout: post
date:   2017-07-07 00:00:00
categories: APIConnect
---
# Teaching my 7yo Daughter to Code

This evening I sat down with my daughter and showed her some basic
coding. Nothing complex, just print out commands and incrementing
numbers.

So I started with JavaScript.... showed how to print out questions to
the end user

```
console.log("How many dogs does the Queen have?")
```

She was impressed with her self, i typed in the console.log but she
handled the rest.

Nest we added a couple more questions and a title.

```
console.log("Queen quiz - by Jessica")
console.log("")
console.log("How many dogs does the Queen have?")
console.log("")
console.log("How many grandchildren does the Queen have?") console.log("")
console.log(How many castles does the Queen have?");
```

She asked how we can change colours so i quickly installed

```
npm install colors
```

and I let her choose the colours for each line and add some more
questions..

```
var color = require('colors');

console.log("Queen quiz - by Jessica".bold)
console.log("")
console.log("How many dogs does the Queen have?".yellow)
console.log("")
console.log("How many grandchildren does the Queen have?");
console.log("")
console.log("How many castles does the Queen have?".magenta);
console.log("")
console.log("How many princesses does the Queen have?".blue);
console.log("How many types of dogs does the Queen have?".green);
console.log("")
console.log("How many princes deos the Queen have?".cyan);
console.log("")
console.log("Who is the Queen's Great Great Grandmother?".magenta);
console.log("")
console.log("Who is the Queen's Great Grandmother?");
console.log("")
console.log("How old is the Queen?".rainbow.bold);
console.log("")
console.log("Who is the Queen Mother?".magenta);
console.log("")
```

Finally we discussed how to put a number at the start of each question.

I showed her what j++ did and set j=1 and some basic string
concatenation.

```
var color = require('colors');
j=1
console.log("Queen quiz - by Jessica".bold)
console.log("")
console.log("How many dogs does the Queen have?".yellow)
console.log("")
console.log(j++ + "\tHow many grandchildren does the Queen have?");
console.log("")
console.log(j++ + "\tHow many castles does the Queen have?".magenta);
console.log("")
console.log(j++ + "\tHow many princesses does the Queen have?".blue);
console.log("")
console.log(j++ + "\tHow many types of dogs does the Queen have?".green);
console.log("")
console.log(j++ + "\tHow many princes deos the Queen have?".cyan);
console.log("")
console.log(j++ + "\tWho is the Queen's Great Great Grandmother?".magenta);
console.log("")
console.log(j++ + "\tWho is the Queen's Great Grandmother?");
console.log("")
console.log(j++ + "\tHow old is the Queen?".rainbow.bold);
console.log("")
console.log(j++ + "\tWho is the Queen Mother?".magenta);
console.log("")
```

As you can see nothing majorly complex but tomorrow I think we may try
and make an OXO game.

End Result.

```
Queen quiz - by Jessica
1 How many dogs does the Queen have?
2 How many grandchildren does the Queen have?
3 How many castles does the Queen have?
4 How many princesses does the Queen have?
5 How many types of dogs does the Queen have?
6 How many princes deos the Queen have?
7 Who is the Queen's Great Great Grandmother?
8 Who is the Queen's Great Grandmother?
9 How old is the Queen?
10 Who is the Queen Mother?
```





By [Chris Phillips](https://medium.com/@cminion) on
[July 7, 2017](https://medium.com/p/981856347c14).

[Canonical
link](https://medium.com/@cminion/teaching-my-7yo-daughter-to-code-981856347c14)

Exported from [Medium](https://medium.com) on April 6, 2019.
