#!/bin/bash

while getopts p:t:s:v: flag
do
    case "${flag}" in
        p) PROFILE=${OPTARG};;
        t) TEMPLATE=${OPTARG};;
        s) STACK=${OPTARG};;
        v) VERB=${OPTARG};;
    esac
done

function usage {
    echo "deploy.sh -p [profile] -t [template_file] -s [stack_name] -v [create|update]" && exit 1
}

if [ -z "$PROFILE" ]; then usage; fi
if [ -z "$TEMPLATE" ]; then usage; fi
if [ -z "$STACK" ]; then usage; fi
if [ -z "$VERB" ]; then usage; fi

PARAMS="ParameterKey=ParamFunctionName,ParameterValue=$LAMBDA_ID"

aws --profile $PROFILE cloudformation ${VERB}-stack \
--stack-name $STACK \
--template-body file://$TEMPLATE \
--parameters $PARAMS \
--capabilities CAPABILITY_IAM
