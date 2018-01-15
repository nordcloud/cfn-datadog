from troposphere import AWSProperty
from . import shared_options, DatadogBase
try:
    unicode = unicode
except NameError:
    str = str
    basestring = (str, bytes)
    unicode = str
    bytes = str


class CompositeOptions(AWSProperty):
    props = shared_options


class Composite(DatadogBase):
    """
    A Python class for our custom resource.  It is also possible to use cloudformation.CustomResource Class but then
    There is no validation required parameters and the resource type will be AWS::CloudFormation::CustomResource
    """
    resource_type = "Custom::Composite"
    props = {
        'ServiceToken': (basestring, True),
        'query': (basestring, True),
        'name': (basestring, False),
        'message': (basestring, False),
        'tags': ([basestring], False),
        'options': (CompositeOptions, False)
    }
