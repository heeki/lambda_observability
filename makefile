include etc/environment.sh

sam: sam.package sam.deploy
sam.build:
	sam build --profile ${PROFILE} --template ${SAM_TEMPLATE} --parameter-overrides ${SAM_PARAMS} --build-dir build --manifest requirements.txt --use-container
	sam package -t build/template.yaml --output-template-file ${SAM_OUTPUT} --s3-bucket ${S3BUCKET}
sam.package:
	sam package -t ${SAM_TEMPLATE} --output-template-file ${SAM_OUTPUT} --s3-bucket ${S3BUCKET}
sam.deploy:
	sam deploy -t ${SAM_OUTPUT} --stack-name ${SAM_STACK} --parameter-overrides ${SAM_PARAMS} --capabilities CAPABILITY_NAMED_IAM
sam.local.invoke:
	sam local invoke --profile ${PROFILE} -t ${SAM_TEMPLATE} --parameter-overrides ${SAM_PARAMS} --env-vars etc/environment.json -e etc/local.json FnProducer | jq
sam.invoke:
	aws --profile ${PROFILE} lambda invoke --function-name ${OUT_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode

layer.xray:
	pip install -r req_xray.txt --target=tmp/xray/python --upgrade
layer.redis:
	pip install -r req_redis.txt --target=tmp/redis/python --upgrade
