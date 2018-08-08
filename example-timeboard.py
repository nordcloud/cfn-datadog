from cfn_datadog import TimeBoard
from troposphere import Parameter, Template, Join, ImportValue, Sub

t = Template()

datadog_lambda_stackname = t.add_parameter(Parameter(
    "DatadogLambdaStackname",
    Type="String",
    Description="Datadog lambda stackname"
))

t.add_resource(TimeBoard(
    'Example TimeBoard',
    ServiceToken=ImportValue(Sub("${DatadogLambdaStackname}"))
))