---
layout: post
date: 2019-06-26 01:00:00
categories: Jekyll
title: "Pagination in Jekyll"
image: "/images/2019-06-28-paginationb.png"
---

This post is just a rehash of [https://jekyllrb.com/docs/pagination/](https://jekyllrb.com/docs/pagination/), but as it took me a few attempts I thought I would try and post a consise list of instructions.

![](/images/2019-06-28-paginationb.png)

To enable pagination in your Jekyll Blog

1 - Add `jekyll-paginate` plugin in the `_config.yaml` similar to the below

```
plugins:
  - jekyll-paginate
  - jekyll-feed
  - jekyll-sitemap
```

2 - Add the following two lines to `_config.yaml`

```
paginate: 10
paginate_path: "/page:num/"
```

3 - Add `jekyll-paginate` to the `Gemfile` in the `jekyll_plugins` section like below

<pre><code>group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.6"
  gem "jekyll-sitemap"
  gem "jekyll-paginate"
end
</code></pre>

4 - In your layout page for the front page replace `for post in site.posts ` with `for post in paginator.posts`

5 - Add the following snippet to after the post list in your layout page. This adds the page links at the bottom of the page.

{% raw %}
```
{% if paginator.total_pages > 1 %}
<div class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}">&laquo; Prev</a>
  {% else %}
    <span>&laquo; Prev</span>
  {% endif %}

  {% for page in (1..paginator.total_pages) %}
    {% if page == paginator.page %}
      <em>{{ page }}</em>
    {% elsif page == 1 %}
      <a href="/">{{ page }}</a>
    {% else %}
      <a href="{{ site.paginate_path | relative_url | replace: ':num', page }}">{{ page }}</a>
    {% endif %}
  {% endfor %}

  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}">Next &raquo;</a>
  {% else %}
    <span>Next &raquo;</span>
  {% endif %}
</div>
{% endif %}
```
{% endraw %}

Now when you deploy your site  you will see the pagintion at the bottom

![](/images/2019-06-28-paginationb.png)
