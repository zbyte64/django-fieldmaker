"""
An easy-to-use Django forms integration of the reCaptcha service.
v1.0.1
"""
import httplib
import urllib

from django import forms
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.utils import simplejson

class RecaptchaWidget(forms.Widget):
    def __init__(self, public_key=None, theme=None, tabindex=None, lang=None, **kwargs):
        """
        From http://recaptcha.net/apidocs/captcha/client.html#look-n-feel::

            theme:      'red' | 'white' | 'blackglass' | 'clean'

                Defines which theme to use for reCAPTCHA.

            tabindex:   any integer

                Sets a tabindex for the reCAPTCHA text box. If other elements
                in the form use a tabindex, this should be set so that
                navigation is easier for the user.
            
            lang:   en | nl | fr | de | pt | re| es | tr
        """
        options = {}
        if theme:
            options['theme'] = theme
        if tabindex:
            options['tabindex'] = tabindex
        if lang:
            options['lang'] = lang
        self.options = options
        self.public_key = public_key
        super(RecaptchaWidget, self).__init__(**kwargs)

    def render(self, name, value, attrs=None):
        params = {'k':self.public_key}
        return render_to_string('recaptcha/code.html', {
            'options': simplejson.dumps(self.options),
            'params': urllib.urlencode(params)
        })

    def value_from_datadict(self, data, files, name):
        challenge = data.get('recaptcha_challenge_field')
        response = data.get('recaptcha_response_field')
        return (challenge, response)

    def id_for_label(self, id_):
        return None


class RecaptchaField(forms.Field):
    widget = RecaptchaWidget
    default_error_messages = {
        'required': u'Please enter the CAPTCHA solution.',
        'invalid': u'An incorrect CAPTCHA solution was entered.',
        'no-remote-ip': u'CAPTCHA failed due to no visible IP address.',
        'challenge-error': u'An error occurred with the CAPTCHA service - try refreshing.',
        'unknown-error': u'The CAPTCHA service returned the following error: %(code)s.',
    }

    def __init__(self, private_key, public_key, *args, **kwargs):
        """
        The optional ``private_key`` argument can be used to override the
        default use of the project-wide ``RECAPTCHA_SECRET_KEY`` setting.
        """
        self.remote_ip = None
        self.private_key = private_key
        self.public_key = public_key
        super(RecaptchaField, self).__init__(*args, **kwargs)
        self.widget.public_key = public_key
    
    def clean(self, value):
        #if not self.remote_ip:
        #    raise forms.ValidationError(self.error_messages['no-remote-ip'])
        value = super(RecaptchaField, self).clean(value)
        challenge, response = value
        if not challenge:
            raise forms.ValidationError(self.error_messages['challenge-error'])
        if not response:
            raise forms.ValidationError(self.error_messages['required'])
        try:
            value = validate_recaptcha(self.remote_ip, challenge, response, self.private_key)
        except RecaptchaError, e:
            if e.code == 'incorrect-captcha-sol':
                raise forms.ValidationError(self.error_messages['invalid'])
            raise forms.ValidationError(self.error_messages['unknown-error'] % {'code': e.code})
        return value

class RecaptchaError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code


def validate_recaptcha(remote_ip, challenge, response, private_key):
    assert challenge, 'No challenge was provided for reCaptcha validation'
    # Request validation from recaptcha.net
    params = {'privatekey':private_key,
              'remoteip':remote_ip,
              'challenge':challenge,
              'response':response,}
    params = urlencode(params)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = httplib.HTTPConnection('www.google.com')
    conn.request('POST', '/recaptcha/api/verify', params, headers)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
    else:
        data = ''
    conn.close()
    # Validate based on response data
    result = data.startswith('true')
    if not result:
        bits = data.split('\n', 2)
        error_code = ''
        if len(bits) > 1:
            error_code = bits[1]
        raise RecaptchaError(error_code)
    # Return dictionary
    return result

