#!/bin/bash

while getopts p:s: flag
do
    case "${flag}" in
        p) PROFILE=${OPTARG};;
        s) STACK=${OPTARG};;
    esac
done

function usage {
    echo "describe.sh -p [profile] -s [stack]" && exit 1
}

if [ -z "$PROFILE" ]; then usage; fi
if [ -z "$STACK" ]; then usage; fi

# if [ $STACK == "logging" ]; then
OUTPUT=$(aws --profile $PROFILE cloudformation describe-stacks --stack-name $STACK)
LAMBDA_ID=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutExampleFunction") | .OutputValue')
LAMBDA_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutExampleFunctionArn") | .OutputValue')
QUEUE_ARN=$(echo $OUTPUT | jq -r -c '.["Stacks"][]["Outputs"][]  | select(.OutputKey == "OutExampleQueueArn") | .OutputValue')
for var in {LAMBDA_ID,LAMBDA_ARN,QUEUE_ARN}; do echo "$var=${!var}"; done
# fi
