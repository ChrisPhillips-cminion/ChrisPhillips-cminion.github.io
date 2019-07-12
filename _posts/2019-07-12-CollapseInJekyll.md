---
layout: post
date: 2019-07-12 12:00:00
categories: Jekyll
title: "Hiding blocks while using Jekyll"
---

I was wanting to hide sample code in my posts so  the meat of the information could be more easily seen.

I went to W3Schools  and they provided me with the sample I needed. However it does not work in Jekyll because of how it generates html from markdown.


[https://www.w3schools.com/howto/howto_js_collapsible.asp](https://www.w3schools.com/howto/howto_js_collapsible.asp)

In order to allow this to work in Jekyll, make the CSS changes as recommended in the w3 article.  Once that is done you need to do things slightly differently to their sapmle code.



<button class="collapsible" id="html">Click here for the code.</button>

<div class="content" id="htmldata" markdown="1">
```html

<button class="collapsible" id="yaml">Click here for the code.</button>

<div class="content" id="yamldata" markdown="1">
  CONTENT
</div>

```
</div>

The id tag needs to be set on both the button and the corresponding div. The div id tag must be the same as the button id with `data` postfixed. In addition you should have `markdown="1"`  as a final tag to ensure that jekyll process the inside of the div.

<button class="collapsible" id="js">Click here for the code.</button>

<div class="content" id="jsdata" markdown="1">

```javascript
<!-- Start Collapse.html -->
<script>
var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = document.getElementById(this.id+"data");
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
</script>
<!-- End Collapse.html -->
```
</div>
In the code I modified  `var content = document.getElementById(this.id+"data");` so that it referenced the content div directly, and did not just assume it was the next element. I put this code into an include called collpase.html and then referenced it from my footer. {% raw %}`{%- include collapse.html -%}` {% endraw %}
