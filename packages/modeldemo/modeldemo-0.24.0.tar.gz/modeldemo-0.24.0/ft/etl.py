"""Data pre-processing using parent model for label generation."""

import os
from pathlib import Path

import modal
import torch
from datasets import load_dataset
from tqdm import tqdm

from src.modeldemo.utils import (
    ARTIFACT_PATH,
    CPU,
    DATA_VOLUME,
    IMAGE,
    PREFIX_PATH,
    PROMPT,
    SEED,
    TIMEOUT,
    TORCH_DTYPE,
    VOLUME_CONFIG,
    clean_output,
    download_model,
    transform_img,
)

# extract
DATASET_NAME = "rootsautomation/ScreenSpot"  # ~1300 samples
DATA_SPLIT = "test"
DATA_DIR = "screenspot"

# transform
PARENT_MODEL_PATH = "OpenGVLab/InternVL2-8B"  # "OpenGVLab/InternVL2-Llama3-76B"
MAX_NUM = 12
MAX_NEW_TOKENS = 256
DO_SAMPLE = True
SAMPLE_BS = 1  # 8
VAL_SPLIT = 0.1


def gen_labels(is_local: bool = False) -> None:
    DEVICE = "cpu"
    if torch.cuda.is_available():
        DEVICE = "cuda"
    # TODO: not supported by Internvl2
    # elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    #     DEVICE = "mps"
    WORLD_SIZE = torch.cuda.device_count() if torch.cuda.is_available() else 0

    ds = load_dataset(DATASET_NAME, trust_remote_code=True, num_proc=max(1, os.cpu_count() // 2))[DATA_SPLIT]
    _, tokenizer, model = download_model(PARENT_MODEL_PATH, WORLD_SIZE, DEVICE, is_local)

    responses = [""] * len(ds)
    for i in tqdm(range(0, len(ds), SAMPLE_BS), desc="Processing batches"):
        batch = ds[i : i + SAMPLE_BS]
        pixel_vals = [transform_img(image).to(TORCH_DTYPE).to(DEVICE) for image in batch["image"]]
        num_patches_list = [pixel_vals[i].size(0) for i in range(len(pixel_vals))]
        pixel_values = torch.cat(pixel_vals, dim=0)

        generation_config = {"max_new_tokens": MAX_NEW_TOKENS, "do_sample": DO_SAMPLE}
        questions = [f"<image>\n{PROMPT}"] * len(num_patches_list)
        with torch.no_grad():
            batch_out = model.batch_chat(
                tokenizer,
                pixel_values,
                num_patches_list=num_patches_list,
                questions=questions,
                generation_config=generation_config,
            )

        for j, out in enumerate(batch_out):
            out = clean_output(out)
            responses[i + j] = out

    ds = ds.add_column("response", responses)
    if is_local:
        data_root = ARTIFACT_PATH / "data" / DATA_DIR
    else:
        data_root = Path("/") / DATA_VOLUME / DATA_DIR

    ds = ds.train_test_split(test_size=VAL_SPLIT, seed=SEED)
    ds.save_to_disk(data_root)


if __name__ == "__main__":
    gen_labels(is_local=True)


# Modal
GPU_TYPE = "H100"
GPU_COUNT = 3  # min for InternVL2-Llama3-76B
GPU_SIZE = None  # options = None (40GB), "80GB"
GPU_CONFIG = f"{GPU_TYPE}:{GPU_COUNT}"
if GPU_TYPE.lower() == "a100":
    GPU_CONFIG = modal.gpu.A100(count=GPU_COUNT, size=GPU_SIZE)

APP_NAME = "label_data"
app = modal.App(name=APP_NAME)

## Modify image to install specific version of transformers
IMAGE = IMAGE.pip_install("transformers==4.37.2")


@app.function(
    image=IMAGE,
    secrets=[modal.Secret.from_dotenv(path=PREFIX_PATH)],
    gpu=GPU_CONFIG,
    volumes=VOLUME_CONFIG,
    timeout=TIMEOUT,
    cpu=CPU,
)
def run():
    gen_labels()


@app.local_entrypoint()
def main():
    run.remote()
