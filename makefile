include etc/environment.sh

obs: obs.package obs.deploy
obs.build:
	sam build --profile ${PROFILE} --template ${OBS_TEMPLATE} --parameter-overrides ${OBS_PARAMS} --build-dir build --manifest requirements.txt --use-container
	sam package -t build/template.yaml --output-template-file ${OBS_OUTPUT} --s3-bucket ${S3BUCKET}
obs.package:
	sam package -t ${OBS_TEMPLATE} --output-template-file ${OBS_OUTPUT} --s3-bucket ${S3BUCKET}
obs.deploy:
	sam deploy -t ${OBS_OUTPUT} --stack-name ${OBS_STACK} --parameter-overrides ${OBS_PARAMS} --capabilities CAPABILITY_NAMED_IAM
obs.local.invoke:
	sam local invoke --profile ${PROFILE} -t ${OBS_TEMPLATE} --parameter-overrides ${OBS_PARAMS} --env-vars etc/environment.json -e etc/local.json FnProducer | jq
obs.invoke:
	aws --profile ${PROFILE} lambda invoke --function-name ${OUT_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode

layer.xray:
	pip install -r req_xray.txt --target=tmp/xray/python --upgrade
layer.redis:
	pip install -r req_redis.txt --target=tmp/redis/python --upgrade

redis: redis.package redis.deploy
redis.package:
	sam package -t ${REDIS_TEMPLATE} --output-template-file ${REDIS_OUTPUT} --s3-bucket ${S3BUCKET}
redis.deploy:
	sam deploy -t ${REDIS_OUTPUT} --stack-name ${REDIS_STACK} --parameter-overrides ${REDIS_PARAMS} --capabilities CAPABILITY_NAMED_IAM

describe.layer-xray-policy:
	aws lambda get-layer-version-policy --layer-name xray-python3 --version-number 1 | jq -r '.Policy' | jq

layer_only: layer_only.package layer_only.deploy
layer_only.package:
	sam package -t ${LAYER_TEMPLATE} --output-template-file ${LAYER_OUTPUT} --s3-bucket ${S3BUCKET} --s3-prefix ${LAYER_STACK}
layer_only.deploy:
	sam deploy -t ${LAYER_OUTPUT} --region ${LAYER_REGION} --stack-name ${LAYER_STACK} --parameter-overrides ${LAYER_PARAMS} --capabilities CAPABILITY_NAMED_IAM