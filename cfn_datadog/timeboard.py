from . import DatadogBase, CustomProperty
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
        'definition': (Definition, True),
        'title': (baseString, False)
    }


class TemplateVariable(AWSProperty):
    props = {
        'name': (baseString, True),
        'prefix': (baseString, True),
        'default': (baseString, True)
    }


class TimeBoard(DatadogBase):
    """
       A Python class for our custom resource.  It is also possible to use cloudformation.CustomResource Class but then
       There is no validation required parameters and the resource type will be AWS::CloudFormation::CustomResource
    """
    resource_type = "Custom::DataDogTimeBoard"
    props = {
        'ServiceToken': (baseString, True),
        'title': (baseString, False),
        'description': (baseString, True),
        'graphs': ([Graph], True),
        'template_variables': ([TemplateVariable], False),
        'read_only': (bool, True)
    }

    # title = "My Timeboard"
    # description = "An informative timeboard."
    # graphs = [{
    #     "definition": {
    #         "events": [],
    #         "requests": [
    #             {"q": "avg:system.mem.free{*}"}
    #         ],
    #         "viz": "timeseries"
    #     },
    #     "title": "Average Memory Free"
    # }]
    #
    # template_variables = [{
    #     "name": "host1",
    #     "prefix": "host",
    #     "default": "host:my-host"
    # }]
    #
    # read_only = True
    # api.Timeboard.create(title=title,
    #                      description=description,
    #                      graphs=graphs,
    #                      template_variables=template_variables,
    #                      read_only=read_only)
