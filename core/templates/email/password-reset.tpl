{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account Activation
{% endblock %}

{% block html %}
To reset your password, please click the link below:
<br><br>
<a href="http://localhost:8000/accounts/api/v1/reset-password/confirm/{{token}}">
    Reset Password
</a>
<br><br>
If you did not request this, please ignore it. Your account will remain unchanged.
<br><br>
Thank you for using our service!
<br><br>
Best regards,
<br>
The Backend Team
{% endblock %}