from simple_textpublisher import SimpleText
from decorators import HTMLDecorator, UpperCaseDecorator

msg = SimpleText("Hello world")
print(msg.publish())

html_msg = HTMLDecorator(msg)
print(html_msg.publish())

upper_encoded = UpperCaseDecorator(html_msg)
print(upper_encoded.publish())
