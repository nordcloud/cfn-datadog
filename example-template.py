from cfn_datadog import MetricAlert, MetricAlertOptions
from troposphere import Parameter, Template, Join, ImportValue, Sub

t = Template()

datadog_lambda_stackname = t.add_parameter(Parameter(
    "DatadogLambdaStackname",
    Type="String",
    Description="Datadog lambda stackname",
))

t.add_resource(MetricAlert(
    'Alert2',
    query=Join("", ["avg(last_1h):avg:system.net.bytes_rcvd{host:", "bla", "} < 40"]),
    ServiceToken=ImportValue(
        Sub("${DatadogLambdaStackname}-MonitorDatadogLambdaArn")),
    name="Bytes received on mytesthost",
    message="bla msg222 @richard.vanbeers",
    tags=["tag1", "tag2"],
    options=MetricAlertOptions(
        notify_no_data=True,
        no_data_timeframe=50
    )
))

print(t.to_json())
