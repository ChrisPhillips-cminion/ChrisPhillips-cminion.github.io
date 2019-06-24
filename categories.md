---
layout: default
---
<div class="wrap">
<div class="tags-expo">
  <div class="tags-expo-list">
    <h2>Categories</h2>
    {% for tag in site.categories %}
    <li><a href="#{{ tag[0] | slugify }}" class="post-tag">{{ tag[0] }}</a></li>
    {% endfor %}
    <br>
  </div>
  <hr/>
  <div class="tags-expo-section">
    {% for tag in site.categories %}
    <h2 id="{{ tag[0] | slugify }}">{{ tag[0] }}</h2>
    <table>

      {% for post in tag[1] %}
      <tr><td><a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></td><td width="100px" >{{ post.date | date_to_string }}</td></tr>

      {% endfor %}

</table>
    {% endfor %}
  </div>
</div>
</div>
