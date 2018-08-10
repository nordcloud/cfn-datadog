# README #



### What is this repository for? ###

* To setup datadog monitoring via cloudformation

### What does it do? ###

It setups a lambda function that communicate with the monitors and timeboard resource
on the datadog api

https://docs.datadoghq.com/api/#monitors
https://docs.datadoghq.com/api/#timeboards

The lambda is invoked via cloudformation custom resource. This repo
supplies custom resource classes for all the 4 Monitor types.
Custom resources have the same exact data structure as the DD api

It uses https://github.com/nordcloud/cfn-encrypt to securely store
datadog api credentials

This repository makes use of [Troposphere](https://github.com/cloudtools/troposphere)

### How do I get set up? ###

* clone this repo
~~~~
git clone git@github.com.org:nordcloud/cfn-datadog.git
~~~~

* Build the lambda package
~~~~
chmod +x create_zip.sh && ./create_zip.sh
~~~~

* upload `datadog_lambda.zip` to an s3 bucket
* get your api and application keys from Datadog
* generate the lambda template
~~~~
python lambda-template.py > /tmp/lambda.template
~~~~
* If you have not already set up your encrypt stack do that now ( https://github.com/nordcloud/cfn-encrypt )
* create a stack from your `lambda.template` file
* The lambda is now set up and ready to use.


### How do i use it to monitor resources created in other stacks? ###

Install the cfn_datadog library
~~~~
pip install cfn-encrypt
~~~~

Import the custom resource classes you want to use
~~~~
from cfn_datadog import (
    MetricAlert, MetricAlertOptions, Composite, CompositeOptions,
    EventAlert, EvenAlertOptions, ServiceCheck, ServiceCheckOptions,
    Timeboard
)
~~~~

Add a parameter so that you can reference your lambda stack
~~~~
datadog_lambda_stackname = t.add_parameter(Parameter(
    "DatadogLambdaStackname",
    Type="String",
    Description="Datadog lambda stackname",
))
~~~~

Add the custom resource to the template: For documentation see datadog api

##### Example MetricAlert
~~~~
t.add_resource(MetricAlert(
    'Alert2',
    query=Join("",["avg(last_1h):avg:system.net.bytes_rcvd{host:",Ref(my_instance),"} < 40"]),
    ServiceToken=ImportValue(
    Sub("${DatadogLambdaStackname}-LambdaArn")),
    name="Bytes received on mytesthost",
    message="Some Message @MyDDHandle",
    tags=["tag1", "tag2"],
    options=MetricAlertOptions(
        notify_no_data= True,
        no_data_timeframe=50
    )
))
~~~~

##### Example Timeboard

~~~~
t.add_resource(Timeboard(
    'ExampleTimeBoard',
    ServiceToken=ImportValue(Sub("${DatadogLambdaStackname}-TimeboardLambdaArn")),
    TimeboardTitle="testboard",
    description="Sample testboard",
    graphs=[Graph(
        definition=Definition(
            events=[],
            requests=[Request(
                q="avg:system.mem.free{*}"
            )],
            viz="timeseries"
        ),
        title="Average Memory Free"
    )],
    template_variables=[TemplateVariable(
        name="host1",
        prefix="host",
        default="host:my-host"
    )],
    read_only=True
))
~~~~

