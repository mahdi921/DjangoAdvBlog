{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock %}

{% block html %}
This is an <strong>html</strong> message.
This is an image:
<img src="https://binaryfork.com/wp-content/uploads/2022/09/midjourney-the-beginning-of-a-parallel-universe.jpg" alt="Midjourney Image">
{% endblock %}