#!/bin/bash

while getopts p:t:s:v:b: flag
do
    case "${flag}" in
        p) PROFILE=${OPTARG};;
        t) TEMPLATE=${OPTARG};;
        s) STACK=${OPTARG};;
        v) VERB=${OPTARG};;
        b) BUILD=${OPTARG};;
    esac
done

function usage {
    echo "deploy.sh -p [profile] -t [template_file] -s [stack_name] -v [deploy|local] -b [true|false]" && exit 1
}

if [ -z "$PROFILE" ]; then usage; fi
if [ -z "$TEMPLATE" ]; then usage; fi
if [ -z "$STACK" ]; then usage; fi
if [ -z "$VERB" ]; then usage; fi

PARAMS="ParameterKey=ParamEnv1,ParameterValue=$ENV1"
PARAMS="$PARAMS ParameterKey=ParamEnv2,ParameterValue=$ENV2"
BASENAME=`basename $TEMPLATE .yaml`

echo
if [[ $BUILD == "true" ]]; then
sam build --profile $PROFILE --build-dir build --manifest requirements.txt --template $TEMPLATE --parameter-overrides $PARAMS --use-container 
fi

if [[ $VERB == "deploy" ]]; then
sam package --template-file build/template.yaml --output-template-file iac/${BASENAME}_output.yaml --s3-bucket $S3BUCKET
sam deploy --template-file iac/${BASENAME}_output.yaml --stack-name $STACK --parameter-overrides $PARAMS --capabilities CAPABILITY_NAMED_IAM
elif [[ $VERB == "local" ]]; then
sam local invoke -e etc/event.json -t build/template.yaml ExampleFunction
fi