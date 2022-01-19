# -*- coding: utf-8 -*-
"""
Make '_' a no-op so we can scrape strings
"""
import logging
from importlib import import_module

from django.conf import settings

log = logging.getLogger(__name__)


def _(text):
    """
    :return text
    """
    return text


def resolve_custom_parameter_template(xblock, template):
    """
    Return the value processed according to the template processor.
    The template processor must return a string object.
    :param xblock: LTI consumer xblock.
    :param template: processor key.
    """
    try:
        module_name, func_name = settings.LTI_CUSTOM_PARAM_TEMPLATES.get(
            template[2:len(template) - 1],
            ':',
        ).split(':', 1)
        template_value = getattr(
            import_module(module_name),
            func_name,
        )(xblock)

        if not isinstance(template_value, str):
            log.error('The \'%s\' processor must return a string object.', func_name)
            return template
    except ValueError:
        log.error(
            'Error while processing \'%s\' value. Reason: The template processor definition must be wrong.',
            template,
        )
        return template
    except (AttributeError, ImportError) as ex:
        log.error('Error while processing \'%s\' value. Reason: %s', template, str(ex))
        return template

    return template_value
