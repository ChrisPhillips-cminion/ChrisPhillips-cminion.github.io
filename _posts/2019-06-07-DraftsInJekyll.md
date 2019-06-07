---
layout: post
date: 2019-06-07 11:00:00
categories: Jekyll
title: 'How I do Drafts in Jekyll'
image: '/images/2019-06-07-jekylldraft.png'
---

Like many people I  write a load of blog posts that never will be published. This is because they don't get finished or because my proof readers explain to me what I am writing is rubbish.  One of the challenges I have head is how to share an article before it s published in a simple way. I have tried sharing the mark down but that doesn't show the images. I have tried setting the date to the past so it is at the bottom of the list, however that does not hide the article.


![](/images/2019-06-07-jekylldraft.png)

In the end I decided to play around with Jekyll to see what I could do. I do not mind the world having access to my drafts but i did not want them on my home page.

I modified the `home.html` file to include this line ` if  post.draft != true  ` and an endif below. Now if i set the drafts variable in the page header to true it wont appear on the home page.  A sample header is below
```
---
layout: post
date: 2019-06-08 12:00:00
categories: Jekyll
title: 'Drafts in Jekyll'
draft: true
---
```

I then created a drafts.html page in layout that was copied from the home.html I was using.  I modified the line I added to be `if  post.draft  ` so that it only showed draft entries. I then created a drafts.md file in the root directory with the following content.
```
---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: drafts
---
```

Now I can view all my draft content at https://chrisphillips-cminion.github.io/drafts.html and when I am ready to publish I just remove the `draft: true`  from the header.

Feel free to poke around my source [here](https://github.com/chrisPhillips-cminion/ChrisPhillips-cminion.github.io).
