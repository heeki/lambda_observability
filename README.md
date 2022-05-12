# Lambda Observability
Sample code for demoing Lambda observability
* Manually setting retention for CloudWatch Log Groups
* Implementing X-ray tracing

## Execution Steps
Execution of all commands can be done via the provided `makefile`. An `etc/environment.sh` file should be configured prior to execution of the make directives, which can be copied from `etc/environment.template`.

```bash
S3BUCKET=your-s3-bucket-for-deployments
S3BUCKET_EUS1=your-s3-bucket-for-deployments-eu-south-1
PROFILE=your-aws-cli-profile-name

P_APISTAGE=your-desired-api-stage
P_VPCID=your-vpc-id
P_SUBNETIDS=your-comma-separated-subnet-id-list
P_INGRESS_SG=your-security-group-id
P_REDIS_ENABLED=true
P_REDIS_ENDPOINT=your-redis-endpoint-fqdn

OBS_STACK=lambda-observability
OBS_TEMPLATE=iac/lambda.yaml
OBS_OUTPUT=iac/lambda_output.yaml
OBS_PARAMS="ParameterKey=pApiStage,ParameterValue=${P_APISTAGE} ParameterKey=pVpcId,ParameterValue=${P_VPCID} ParameterKey=pSubnetIds,ParameterValue=${P_SUBNETIDS} ParameterKey=pRedisEnabled,ParameterValue=${P_REDIS_ENABLED} ParameterKey=pRedisEndpoint,ParameterValue=${P_REDIS_ENDPOINT}"

OUT_FN=your-deployed-fn-name

REDIS_STACK=lambda-redis
REDIS_TEMPLATE=iac/redis.yaml
REDIS_OUTPUT=iac/redis_output.yaml
REDIS_PARAMS="ParameterKey=pVpcId,ParameterValue=${P_VPCID} ParameterKey=pSubnetIds,ParameterValue=${P_SUBNETIDS} ParameterKey=pIngressSG,ParameterValue=${P_INGRESS_SG}"

LAYER_REGION=eu-south-1
LAYER_STACK=lambda-observability-layers
LAYER_TEMPLATE=iac/layers.yaml
LAYER_OUTPUT=iac/layers_output.yaml
LAYER_PARAMS="ParameterKey=pApiStage,ParameterValue=${P_APISTAGE}"
```

## Issues and Errors
Found that when testing locally with `sam local invoke` the `!Ref ExampleQueue` was only returning the CloudFormation resource id rather than the actual queue URL. This works properly when actually deployed.

Found that `sam build` doesn't work with certain Python dependencies that require c bindings on Mac (wrapt has c code). To resolve this, need to use the `--use-container` flag.
```
Building function 'ExampleLambda'
Running PythonPipBuilder:ResolveDependencies

Build Failed
Error: PythonPipBuilder:ResolveDependencies - {future==0.18.2(sdist), wrapt==1.12.1(sdist)}
```
