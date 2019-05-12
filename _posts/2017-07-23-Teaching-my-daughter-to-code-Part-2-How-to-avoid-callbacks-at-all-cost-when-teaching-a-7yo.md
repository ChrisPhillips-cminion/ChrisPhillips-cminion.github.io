---
layout: post
date: 2017-07-23  00:00:00
categories: APIConnect
title: |
    Teaching my daughter to code Part 2 --- How to avoid callbacks at all
    cost when teaching a 7yo
---
# Teaching my daughter to code Part 2 --- How to avoid callbacks at all cost when teaching a 7yo

So Jessica finally persudaded that we should do some more work on her
quiz. She wanted ot make it interactive so that people could answer the
questions.

*As any half decent coder will say, thats simple!*

*As any decent coder will say, hang on she is 7 and this is Node JS!*

The rules I set myself for this were as follows

```
Rule 1 - Don't mention callbacks
Rule 2 - If she gets bored let her go and do something else.
```

Every time I have done user input at the CLI I have used the *great*
inquirer package
([https://www.npmjs.com/package/inquirer)](https://www.npmjs.com/package/inquirer), even writing an extension when it wouldnt do what i
wanted (<https://www.npmjs.com/package/inquirer-orderedcheckbox> with 12
whole downloads!).

This time I used the simple read package
(<https://www.npmjs.com/package/read>). This allowed us to a very basic
prompt.

```
read({
  prompt: "??"
}, function(err, answer) {
  if (answer == "Prince Philip") {
    console.log("Correct!");
  } else {
    console.log("Wrong");
  }
})
```

So we would console.log to ask the question then run read with a '??' to
prompt for the answer. This would give the following

```
1    How many dogs does the Queen have?

?? ANSWER GOES HERE
```

However to ensure that the questions do not get asked at the same time
(damn Async) we must ensure that each question is asked in the same
callback as we process the answer, ARGH Remember Rule 1. The solution to
this was to not talk about the close braces until we had answered all
the questions.

Once we managed to add the close braces we installed atom-beautify and
Jessica used the magic beautify funciton to make code easier to read.
The final code is in Git
(<https://github.com/ChrisPhillips-cminion/JessicasQuiz>) and below.

Jessica asked a question why do we need a ; at the end of each line. The
only reason I came up with was *"To Stop Jack moaning at me", but she
seemed to accept this.*

**\*\*We make no promises that the answers to the questions are
correct!\*\***

```
var sleep = require('sleep').sleep
var color = require('colors');
var read = require('read');
j = 1
totalAnswers = 0
console.log("Queen quiz - by Jessica".bold)
sleep(2)
read({
  prompt: "What is your name?"
}, function(err, answer) {
  console.log("Hello " + answer)
  console.log("")
  console.log(j++ + "\tHow many dogs does the Queen have?".yellow)
  console.log("")
  read({
    prompt: "??"
  }, function(err, answer) {
    if (answer == "30") {
      console.log("Correct!");
    } else {
      console.log("Wrong");
    }
    console.log(j++ + "\tHow many grandchildren does the Queen have?");
    console.log("")
    read({
      prompt: "??"
    }, function(err, answer) {
      if (answer == "8") {
        console.log("Correct!");
      } else {
        console.log("Wrong");
      }
      console.log(j++ + "\tHow many castles does the Queen have?".magenta);
      console.log("")
      read({
        prompt: "??"
      }, function(err, answer) {
        if (answer == "8") {
          console.log("Correct!");
        } else {
          console.log("Wrong");
        }
console.log(j++ + "\tHow many princesses does the Queen have?".blue);
        console.log("")
        read({
          prompt: "??"
        }, function(err, answer) {
          if (answer == "4") {
            console.log("Correct!");
          } else {
            console.log("Wrong");
          }
console.log(j++ + "\tHow many types of dogs does the Queen have?".green);
          console.log("")
          read({
            prompt: "??"
          }, function(err, answer) {
            if (answer == "6") {
              console.log("Correct!");
            } else {
              console.log("Wrong");
            }
console.log(j++ + "\tHow many princes deos the Queen have?".cyan);
            console.log("")
            read({
              prompt: "??"
            }, function(err, answer) {
              if (answer == "5") {
                console.log("Correct!");
              } else {
                console.log("Wrong");
              }
console.log(j++ + "\tWho is the Queen's Great Great Grandmother?".magenta);
              console.log("")
              read({
                prompt: "??"
              }, function(err, answer) {
                if (answer == "Victoria") {
                  console.log("Correct!");
                } else {
                  console.log("Wrong");
                }
                console.log(j++ + "\tWho is the Queen's Great Grandmother?");
                console.log("")
                read({
                  prompt: "??"
                }, function(err, answer) {
                  if (answer == "Alexandra") {
                    console.log("Correct!");
                  } else {
                    console.log("Wrong");
                  }
                  console.log(j++ + "\tHow old is the Queen?".rainbow.bold);
                  console.log("")
                  read({
                    prompt: "??"
                  }, function(err, answer) {
                    if (answer == "91") {
                      console.log("Correct!");
                    } else {
                      console.log("Wrong");
                    }
                    console.log(j++ + "\thow old was the Queen when she became Queen?".magenta);
                    console.log("")
                    read({
                      prompt: "??"
                    }, function(err, answer) {
                      if (answer == "25") {
                        console.log("Correct!");
                      } else {
                        console.log("Wrong");
                      }
                      console.log(j++ + "\tHow many countries does the Queen rule?".rainbow.bold);
                      console.log("")
                      read({
                        prompt: "??"
                      }, function(err, answer) {
                        if (answer == "16") {
                          console.log("Correct!");
                        } else {
                          console.log("Wrong");
                        }
                        console.log("")
console.log(j++ + "\tHow many sister does the Queen have?".magenta);
read({
                          prompt: "??"
                        }, function(err, answer) {
                          if (answer == "1") {
                            console.log("Correct!");
                          } else {
                            console.log("Wrong");
                          }
                          console.log(j++ + "\tWho is the Duke of Edinburgh?".magenta);
                          console.log("")
                          read({
                            prompt: "??"
                          }, function(err, answer) {
                            if (answer == "Prince Philip") {
                              console.log("Correct!");
                            } else {
                              console.log("Wrong");
                            }
                            console.log(j++ + "\tHow old was the Queen in May 1926?".magenta);
                            console.log("")
                            read({
                              prompt: "??"
                            }, function(err, answer) {
                              if (answer == "0") {
                                console.log("Correct!");
                              } else {
                                console.log("Wrong");
                              }
                              console.log(j++ + "\tDid George VI like to knit?".magenta);
                              console.log("")
                              read({
                                prompt: "??"
                              }, function(err, answer) {
                                if (answer == "yes") {
                                  console.log("Correct!");
                                } else {
                                  console.log("Wrong");
                                }
                                console.log(j++ + "\tWho did the Queen marry?".magenta);
                                console.log("")
                                read({
                                  prompt: "??"
                                }, function(err, answer) {
                                  if (answer == "Prince Philip") {
                                    console.log("Correct!");
                                  } else {
                                    console.log("Wrong");
                                  }
                                })
                              })
                            })
                          })
                        })
                      })
                    })
                  })
                })
              })
            })
          })
        })
      })
    })
  })
})
```

So whats left

1.  [Validating the questions]
2.  [Functions]
3.  [Better callback practise]
4.  [Documenting Code as we go!]





By [Chris Phillips](https://medium.com/@cminion) on
[July 23, 2017](https://medium.com/p/29cc999e0383).

[Canonical
link](https://medium.com/@cminion/teaching-my-daughter-to-code-part-2-how-to-avoid-callbacks-at-all-cost-when-teaching-a-7yo-29cc999e0383)

Exported from [Medium](https://medium.com) on April 6, 2019.
