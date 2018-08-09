from cfn_datadog import TimeBoard, Graph, TemplateVariable, Definition, Request
from troposphere import Parameter, Template, Join, ImportValue, Sub

t = Template()

datadog_lambda_stackname = t.add_parameter(Parameter(
    "DatadogLambdaStackname",
    Type="String",
    Description="Datadog lambda stackname"
))

t.add_resource(TimeBoard(
    'ExampleTimeBoard',
    ServiceToken=ImportValue(Sub("${DatadogLambdaStackname}-LambdaArn")),
    title="testboard",
    description="ffff",
    graphs=[Graph(
        definition=Definition(
            events=[],
            requests=[Request(
                q="avg:system.mem.free{*}"
            )],
            viz="timeseries"
        ),
        # title="AverageMemoryFree2"
    )],
    template_variables=[TemplateVariable(
        name="host1",
        prefix="host",
        default="host:my-host"
    )],
    read_only=True
))


print(t.to_json())

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