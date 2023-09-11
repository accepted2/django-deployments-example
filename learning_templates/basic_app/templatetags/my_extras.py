from django import template

register= template.Library()

# @register.filter(name="cut_replace")
def cut_replace(value,arg):
    """

    this cuts all values of "arg" from the string!

    """
    return value.replace(arg,'Hello')

register.filter('cut_replace',cut_replace)