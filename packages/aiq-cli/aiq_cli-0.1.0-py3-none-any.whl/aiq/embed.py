import sys
import select
from abc import ABC, abstractmethod
from typing import Literal, Union, Optional
import json
import numpy as np
import onnxruntime as ort
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer
import rich
from rich.console import Console
from rich.status import Status
import contextlib
from onnx_embedding_models import EmbeddingModel

def embed(
    input_field: str = "text",
    output_field: str = "embedding",
    model_name: str = "snowflake-xs",
    skip_errors: bool = False,
    progress: bool = False, # do not turn on if piping to another process, they'll interfere
    file: Optional[str] = None
):
    model = EmbeddingModel.from_registry(model_name)
    console = Console(file=sys.stderr)
    stdout = Console(file=sys.stdout)
    examples_read = 0
    # with Status("", console=console) if  as status:
    # if show progress, then use status otherwise contextlib.nullcontext
    if file is None:
        file_handle = sys.stdin
    else:
        file_handle = open(file, "r")

    with (
        Status("", console=console, spinner_style=rich.style.Style(color="purple")) if progress else contextlib.nullcontext()
    ) as status:
        for line in file_handle:
            if not line:
                # End of file reached
                break
            try:
                input_json = json.loads(line)
                input_text = input_json[input_field]
                embedding = model.encode([input_text], show_progress=False)[0]
                stdout.print(json.dumps({
                    **input_json,
                    output_field: embedding.tolist()
                }), markup=False, soft_wrap=True)
                examples_read += 1
                if progress and status is not None:
                    status.update(f"Embedded {examples_read} examples...")
            except Exception as e:
                if not skip_errors:
                    raise RuntimeError(f"Error processing line: {line}. Error: {str(e)}") from e
