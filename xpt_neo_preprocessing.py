import json
import os
from argparse import ArgumentParser

from transformers import AutoTokenizer

from multilingual.data.preprocess.preprocessor import DatasetPreprocessor

parser = ArgumentParser()
parser.add_argument("--config", "-c", type=str, required=True)
config = json.load(open(parser.parse_args().config))

tokenizer = AutoTokenizer.from_pretrained(config["tokenizer_name"])
os.environ["TOKENIZERS_PARALLELISM"] = "true"

preprocessor = DatasetPreprocessor(
    tokenizer=tokenizer,
    binarization_impl=config["datasets"]["params"]["binarization_impl"],
    eod_token_id=tokenizer.eos_token_id,
    append_eod=config["datasets"]["params"]["append_eod"],
)

# for dataset in config["datasets"]["names"]:
#     preprocessor.preprocess(
#         open(dataset["name"] + ".txt"),
#         save_file_name=dataset["name"],
#         log_interval=config["datasets"]["params"]["log_interval"],
#     )

for dataset in config["datasets"]["names"]:
    data_list = os.listdir(dataset["name"])
    for data in data_list :
        preprocessor.preprocess(
            preprocessor.open_jsonl(os.path.join(dataset["name"],data),"text"),
            #open(dataset["name"]),
            save_file_name=os.path.join(dataset["name"],data),
            log_interval=config["datasets"]["params"]["log_interval"],
        )
