#!/bin/bash

docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  sweagent/swe-agent-run:latest \
  python run.py \
  --image_name=sweagent/swe-agent:latest \
  --model_name ollama:llama2 \
  --host_url localhost:11434\
  --data_path https://github.com/pvlib/pvlib-python/issues/1603 \
  --config_file config/default_from_url.yaml \
  --skip_existing=False
