from django import template
import logging

logger = logging.getLogger(__name__)

register = template.Library()

@register.filter
def get_item(dictionary, key):
    logger.debug(f"Accessing key: {key} in dictionary: {dictionary}")
    return dictionary.get(key)
