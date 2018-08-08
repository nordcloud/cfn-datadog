from troposphere import (
    Template, iam, GetAtt, Join, Ref, logs, Select, Export, Output, Parameter, awslambda, Base64, ImportValue, Sub
)
from awacs.aws import Policy, Allow, Statement, Principal, Action
from cfn_encrypt import Encrypt

t = Template()

datadog_api_key = t.add_parameter(Parameter(
    "DatadogApiKey",
    Type="String",
    Description="Datadog api key",
    NoEcho=True
))

datadog_application_key = t.add_parameter(Parameter(
    "DatadogApplicationKey",
    Type="String",
    Description="Datadog application key",
    NoEcho=True
))

encrypt_lambda_stack = t.add_parameter(Parameter(
    "EncryptLambdaStack",
    Type="String",
    Description="Stack name of the encryption lambda"
))

lambda_package = t.add_parameter(Parameter(
    "LambdaPackage",
    Type="CommaDelimitedList",
    Description="Location of lambda zip file. ie: mybucket,datadog_lambda.zip"
))

log_level = t.add_resource(Parameter(
    "LogLevel",
    Type="String",
    AllowedValues=[
        "DEBUG",
        "INFO",
        "WARN",
        "ERROR",
        "CRITICAL"
    ],
    Default="INFO"
))

# Create loggroup
log_group = t.add_resource(logs.LogGroup(
    "LogGroup",
    LogGroupName=Join("", ["/aws/lambda/", Join("-", ["datadoglambda", Ref("AWS::StackName")])]),
    RetentionInDays=14
))


kms_key_arn = ImportValue(Sub("${EncryptLambdaStack}-KmsKeyArn"))
lambda_arn = ImportValue(Sub("${EncryptLambdaStack}-LambdaArn"))

datadog_lambda_role = t.add_resource(iam.Role(
    "DatadogLambdaRole",
    AssumeRolePolicyDocument=Policy(
        Version="2012-10-17",
        Statement=[
            Statement(
                Effect=Allow,
                Principal=Principal("Service", "lambda.amazonaws.com"),
                Action=[Action("sts", "AssumeRole")]
            )
        ]),
    Path="/",
    ManagedPolicyArns=["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"],
    Policies=[
        iam.Policy(
            PolicyName="decrypt",
            PolicyDocument=Policy(
                Version="2012-10-17",
                Statement=[
                    Statement(
                        Effect=Allow,
                        Action=[
                            Action("kms", "Decrypt"),
                        ],
                        Resource=[kms_key_arn]
                    )
                ],
            )
        )
    ]
))

api_key = t.add_resource(Encrypt(
    "ApiKey",
    ServiceToken=lambda_arn,
    Base64Data=Base64(Ref(datadog_api_key)),
    KmsKeyArn=kms_key_arn
))

application_key = t.add_resource(Encrypt(
    "ApplicationKey",
    ServiceToken=lambda_arn,
    Base64Data=Base64(Ref(datadog_application_key)),
    KmsKeyArn=kms_key_arn
))

datadog_monitor_lambda = t.add_resource(awslambda.Function(
    "datadogmonitorlambda",
    DependsOn=["LogGroup"],  # log_group.title would also work
    Code=awslambda.Code(
        S3Bucket=Select(0, Ref(lambda_package)),
        S3Key=Select(1, Ref(lambda_package))
    ),
    Handler="index.handler",
    FunctionName=Join("-", ["datadogmonitorlambda", Ref("AWS::StackName")]),
    Role=GetAtt(datadog_lambda_role, "Arn"),
    Runtime="python2.7",
    Timeout=300,
    MemorySize=1536,
    KmsKeyArn=kms_key_arn,
    Environment=awslambda.Environment(
        Variables={
            'api_key': GetAtt(api_key, "CiphertextBase64"),
            'application_key': GetAtt(application_key, "CiphertextBase64"),
            "LOG_LEVEL": Ref(log_level)
        }
    )
))

datadog_timeboard_lambda = t.add_resource(awslambda.Function(
    "datadogtimeboardlambda",
    DependsOn=["LogGroup"],  # log_group.title would also work
    Code=awslambda.Code(
        S3Bucket=Select(0, Ref(lambda_package)),
        S3Key=Select(1, Ref(lambda_package))
    ),
    Handler="timeboard_index.handler",
    FunctionName=Join("-", ["datadogtimeboardlambda", Ref("AWS::StackName")]),
    Role=GetAtt(datadog_lambda_role, "Arn"),
    Runtime="python2.7",
    Timeout=300,
    MemorySize=1536,
    KmsKeyArn=kms_key_arn,
    Environment=awslambda.Environment(
        Variables={
            'api_key': GetAtt(api_key, "CiphertextBase64"),
            'application_key': GetAtt(application_key, "CiphertextBase64"),
            "LOG_LEVEL": Ref(log_level)
        }
    )
))

t.add_output(Output(
    "MonitorDatadogLambdaArn",
    Description="Monitor lambda arn",
    Value=GetAtt(datadog_monitor_lambda, "Arn"),
    Export=Export(
        Sub(
            "${AWS::StackName}-LambdaArn"
        )
    )
))

t.add_output(Output(
    "TimeBoardDatadogLambdaArn",
    Description="Timeboard lamdba arn",
    Value=GetAtt(datadog_timeboard_lambda, "Arn"),
    Export=Export(
        Sub(
            "${AWS::StackName}-LambdaArn"
        )
    )
))

print(t.to_json())
