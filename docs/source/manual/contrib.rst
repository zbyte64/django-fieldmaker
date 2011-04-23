Contrib
=======

``fieldmaker.contrib`` contains additional django apps that extend the functionality of django fieldmaker.


Recaptcha
---------

``fieldmaker.contrib.recaptcha`` adds a Recaptcha field (http://www.google.com/recaptcha). Add this to your ``INSTALLED_APPS`` and the RecaptchaField will be made available to the form definition. The field itself will validate the user input and will invalidate the form until the proper response is entered.

