---
title: Django Template Components Without React
description: A small component pattern for Django templates using two custom tags and no frontend build step.
summary: Django templates can get a useful component primitive with define/render tags, props, and children.
date: 2026-05-03
---

# Django Template Components Without React

Sometimes the problem is not that a project needs React. The problem is that the templates need a local abstraction.

Django templates already have includes, inheritance, blocks, filters, and custom tags. That is enough for a lot of server-rendered applications. But there is one small pattern I keep wanting when a page starts to repeat UI: define a component once, pass it props, and put markup inside it as children.

That was the idea behind an old gist: [React-style components for Django templates](https://gist.github.com/mariocesar/0ad5bfbee43690e5123e9db2307f6db4).

The usage is intentionally boring:

```django
{% load component_tags %}

{% define "button" %}
  <button class="{{ props.class }}" type="{{ props.type|default:'button' }}">
    {{ props.children }}
  </button>
{% enddefine %}

{% render "button" with class="primary" %}
  Submit
{% endrender %}
```

The implementation is just two template tags:

- `define` stores a template node list under a name.
- `render` resolves props, renders the body, and exposes that body as `props.children`.

There is no bundler, no hydration boundary, no client-side router, and no second rendering model. The abstraction stays inside Django's template system.

The useful part is not that this imitates React. The useful part is that it gives a name to markup that already exists. A card, button, alert, empty state, table cell, or repeated layout row can become a local component without creating a Python inclusion tag for every small variation.

The tradeoff is real: this is not a design system. There is no type checker, no import graph, no editor that understands props. If components become global and heavily nested, you can recreate the same problems people complain about in frontend frameworks.

But for small and medium Django apps, that tradeoff is often fine. The code stays close to the HTML. The server still renders the page. The component is just enough structure to keep templates from turning into copy-pasted walls.

The lesson I keep coming back to: before adding a frontend architecture, try adding the missing primitive to the system you already have.
