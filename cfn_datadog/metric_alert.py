from troposphere import AWSProperty
from troposphere.validators import positive_integer
from . import shared_options, DatadogBase
try:
    unicode = unicode
except NameError:
    str = str
    basestring = (str, bytes)
    unicode = str
    bytes = str


class Thresholds(AWSProperty):
    props = {
        'critical': (positive_integer, False),
        'warning': (positive_integer, False)
    }


class MetricAlertOptions(AWSProperty):
    props = {
        'thresholds': (Thresholds, False),
        'evaluation_delay': (positive_integer, False)
    }
    props.update(
        shared_options
    )


class MetricAlert(DatadogBase):
    """
    A Python class for our custom resource.  It is also possible to use cloudformation.CustomResource Class but then
    There is no validation required parameters and the resource type will be AWS::CloudFormation::CustomResource
    """
    resource_type = "Custom::DataDogMetricAlert"
    props = {
        'ServiceToken': (basestring, True),
        'query': (basestring, True),
        'name': (basestring, False),
        'message': (basestring, False),
        'tags': ([basestring], False),
        'options': (MetricAlertOptions, False)
    }



