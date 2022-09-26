from django import template
import markdown

register = template.Library()

@register.filter
def penniesToDollars(pennies):
    pennies = str(pennies)
    dollar = "$" + pennies[:-2] + "." + pennies[-2:]
    return dollar

@register.filter
def markdownify(text):
    md = markdown.markdown(text, extensions=["extra"], safe_mode="escape")
    return md

def GetMarkdownObject():
    # https://python-markdown.github.io/extensions/
    md = markdown.Markdown(extensions=["extra"], safe_mode="escape")
    return md