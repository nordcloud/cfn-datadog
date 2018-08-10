from cfn_datadog import Timeboard, Graph, TemplateVariable, Definition, Request
from troposphere import Parameter, Template, Join, ImportValue, Sub

t = Template()

datadog_lambda_stackname = t.add_parameter(Parameter(
    "DatadogLambdaStackname",
    Type="String",
    Description="Stack name of cfn-datadog"
))

time_board_arn = ImportValue(Sub("${DatadogLambdaStackname}-TimeboardDatadogLambdaArn"))

t.add_resource(Timeboard(
    'ExampleTimeBoard',
    ServiceToken=time_board_arn,
    TimeboardTitle="Automated Datadog Test Board",
    description="Automated Datadog timeboard created through Cloudformation",
    graphs=[Graph(
        GraphTitle="Example graph",
        definition=Definition(
            events=[],
            requests=[Request(
                q="avg:system.mem.free{*}"
            )],
            viz="timeseries"
        )
    ), Graph(
        GraphTitle="Example graph 2",
        definition=Definition(
            events=[],
            requests=[Request(
                q="avg:system.mem.free{*}"
            )],
            viz="timeseries"
        )
    ),
    ],
    template_variables=[TemplateVariable(
        name="host1",
        prefix="host",
        default="host:my-host"
    )],
    read_only=True
))

print(t.to_json())
