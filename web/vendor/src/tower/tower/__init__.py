import copy
import gettext
import re

import django
from django.conf import settings
from django.utils.functional import lazy
from django.utils.importlib import import_module
from django.utils.translation import (trans_real as django_trans,
                                      ugettext as django_ugettext,
                                      ungettext as django_nugettext)


def ugettext(message, context=None):
    """Always return a stripped string, localized if possible"""
    stripped = strip_whitespace(message)

    message = add_context(context, stripped) if context else stripped

    ret = django_ugettext(message)

    # If the context isn't found, we need to return the string without it
    return stripped if ret == message else ret


def ungettext(singular, plural, number, context=None):
    """Always return a stripped string, localized if possible"""
    singular_stripped = strip_whitespace(singular)
    plural_stripped = strip_whitespace(plural)

    if context:
        singular = add_context(context, singular_stripped)
        plural = add_context(context, plural_stripped)
    else:
        singular = singular_stripped
        plural = plural_stripped

    ret = django_nugettext(singular, plural, number)

    # If the context isn't found, the string is returned as it came
    if ret == singular:
        return singular_stripped
    elif ret == plural:
        return plural_stripped
    return ret

ugettext_lazy = lazy(ugettext, unicode)
ungettext_lazy = lazy(ungettext, unicode)


def add_context(context, message):
    # \x04 is a magic gettext number.
    return u"%s\x04%s" % (context, message)


def split_context(message):
    # \x04 is a magic gettext number.
    ret = message.split(u"\x04")
    if len(ret) == 1:
        ret.insert(0, "")
    return ret


def strip_whitespace(message):
    return re.compile(r'\s+', re.UNICODE).sub(' ', message).strip()


def activate(locale):
    """
    Override django's utils.translation.activate().  Django forces files
    to be named django.mo (http://code.djangoproject.com/ticket/6376).  Since
    that's dumb and we want to be able to load different files depending on
    what part of the site the user is in, we'll make our own function here.
    """

    class Translation(object):
        """
        We pass this object to jinja so it can find our gettext implementation.
        If we pass the GNUTranslation object directly, it won't have our
        context and whitespace stripping action.
        """
        ugettext = staticmethod(ugettext)
        ungettext = staticmethod(ungettext)

    import jingo
    jingo.env.install_gettext_translations(Translation)

    if django.VERSION >= (1, 3):
        django_trans._active.value = _activate(locale)
    else:
        from django.utils.thread_support import currentThread
        django_trans._active[currentThread()] = _activate(locale)


def _activate(locale):
    # XXX TODO: When it comes time to load .mo files on the fly and merge
    # them, this is the place to do it.  We'll also need to implement our own
    # caching since the _translations stuff is built on a per locale basis,
    # not per locale + some key
    locale = django_trans.to_locale(locale)

    # Django caches the translation objects here
    t = django_trans._translations.get(locale, None)
    if t is not None:
        return t

    # Django's activate() simply calls translation() and adds it to a global.
    # We'll do the same here, first calling django's translation() so it can
    # do everything it needs to do, and then calling gettext directly to
    # load the rest.  We make a deepcopy because Django will return the en-US
    # catalog if it doesn't have a locale (but we do).  We don't want to merge
    # our foreign catalog into en-US.  Since Django stuck the en-US catalog
    # into its cache for this locale, we have to update that too.
    t = copy.deepcopy(django_trans.translation(locale))
    t.set_language(locale)
    try:
        """When trying to load css, js, and images through the Django server
        gettext() throws an exception saying it can't find the .mo files.  I
        suspect this has something to do with Django trying not to load
        extra stuff for requests that won't need it.  I do know that I don't
        want to try to debug it.  This is what Django does in their function
        also.
        """
        #If you've got extra .mo files to load, this is the place.
        path = import_module(settings.SETTINGS_MODULE).path
        domain = getattr(settings, 'TEXT_DOMAIN', 'messages')
        bonus = gettext.translation(domain, path('locale'), [locale],
                                    django_trans.DjangoTranslation)
        t.merge(bonus)

        # Overwrite t (defaults to en-US) with our real locale's plural form
        t.plural = bonus.plural

    except IOError:
        pass

    django_trans._translations[locale] = t
    return t


def deactivate_all():
    """ Override django's utils.translation.deactivate_all().  Django continues
    to cache a catalog even if you call their deactivate_all().
    """
    django_trans.deactivate_all()
    django_trans._translations = {}
