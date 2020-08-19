# Lambda Observability
Sample code for demoing Lambda observability
* Manually setting retention for CloudWatch Log Groups
* Implementing X-ray tracing

## Execution Steps
```bash
./deploy_sam.sh -t iac/example.yaml -s logging -v deploy -b true
./describe -p 1527 -s logging

./deploy_sam.sh -t iac/example.yaml -s logging -v local -b false
sam local invoke -e etc/event.json -t build/template.yaml ExampleFunction
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
