"""Example views. Feel free to delete this app."""

import logging

from django.shortcuts import render

import bleach
import commonware
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf

from django.core.context_processors import csrf
log = commonware.log.getLogger('playdoh')


@mobile_template('scanner/{mobile/}home.html')
def home(request, template=None):
    """Home main view"""
    data = {}  # You'd add data here that you're sending to the template.
    return render(request, template, data)

@mobile_template('scanner/{mobile/}newscan.html')
def newscan(request, template=None):
    #Page has been POSTED to
    if request.method == 'POST':
        url_entered = request.POST["new_scan_url_input"]
        data = {"url_entered":url_entered}
        return render(request, template, data)
    #Page has not been posted to
    else:
        data = {}  # You'd add data here that you're sending to the template.
        return render(request, template, data)

@anonymous_csrf
def bleach_test(request):
    """A view outlining bleach's HTML sanitization."""
    allowed_tags = ('strong', 'em')

    data = {}

    if request.method == 'POST':
        bleachme = request.POST.get('bleachme', None)
        data['bleachme'] = bleachme
        if bleachme:
            data['bleached'] = bleach.clean(bleachme, tags=allowed_tags)

        # CEF logging: Log user input that needed to be "bleached".
        if data['bleached'] != bleachme:
            log_cef('Bleach Alert', logging.INFO, request,
                    username='anonymous', signature='BLEACHED',
                    msg='User data needed to be bleached: %s' % bleachme)

    return render(request, 'scanner/bleach.html', data)