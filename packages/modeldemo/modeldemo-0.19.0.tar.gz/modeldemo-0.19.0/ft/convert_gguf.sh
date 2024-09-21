MODEL_DIR=./artifacts/runs/

git clone git@github.com:OpenBMB/llama.cpp.git
cd llama.cpp
git checkout minicpmv-main

python ./examples/llava/minicpmv-surgery.py -m $MODEL_DIR
python ./examples/llava/minicpmv-convert-image-encoder-to-gguf.py -m $MODEL_DIR --minicpmv-projector $MODEL_DIR/minicpmv.projector --output-dir $MODEL_DIR --image-mean 0.5 0.5 0.5 --image-std 0.5 0.5 0.5 --minicpmv_version 3
python ./convert_hf_to_gguf.py $MODEL_DIR/model

# quantize int4 version
./llama-quantize $MODEL_DIR/model/ggml-model-f16.gguf $MODEL_DIR/model/ggml-model-Q4_K_M.gguf Q4_K_M
