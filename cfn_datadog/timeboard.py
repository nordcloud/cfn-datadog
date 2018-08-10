from . import DatadogBase
from troposphere import AWSProperty

try:
    unicode = unicode
except NameError:
    str = str
    baseString = (str, bytes)
    unicode = str
    bytes = str


class Request(AWSProperty):
    props = {
        'q': (baseString, True)
    }


class Definition(AWSProperty):
    props = {
        'events': ([baseString], True),
        'requests': ([Request], True),
        'viz': (baseString, True)
    }


class Graph(AWSProperty):
    props = {
        'GraphTitle': (baseString, True),
        'definition': (Definition, True)
    }


class TemplateVariable(AWSProperty):
    props = {
        'name': (baseString, True),
        'prefix': (baseString, True),
        'default': (baseString, True)
    }


class Timeboard(DatadogBase):
    """
       A Python class for our custom resource.  It is also possible to use cloudformation.CustomResource Class but then
       There is no validation required parameters and the resource type will be AWS::CloudFormation::CustomResource
    """
    resource_type = "Custom::DataDogTimeBoard"
    props = {
        'ServiceToken': (baseString, True),
        'TimeboardTitle': (baseString, False),
        'description': (baseString, True),
        'graphs': ([Graph], True),
        'template_variables': ([TemplateVariable], False),
        'read_only': (bool, True)
    }