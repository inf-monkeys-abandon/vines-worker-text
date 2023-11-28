import sys

from vines_worker_sdk.conductor import ConductorClient
from vines_worker_sdk.oss import OSSClient
from vines_worker_sdk.utils.files import ensure_directory_exists
from block_def import block_def, block_name
import threading
import time
import signal
import os
from dotenv import load_dotenv
import uuid
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    Language,
    MarkdownHeaderTextSplitter,
    TokenTextSplitter,
)

load_dotenv()

SERVICE_REGISTRATION_URL = os.environ.get("SERVICE_REGISTRATION_URL")
SERVICE_REGISTRATION_TOKEN = os.environ.get("SERVICE_REGISTRATION_TOKEN")
CONDUCTOR_BASE_URL = os.environ.get("CONDUCTOR_BASE_URL")
CONDUCTOR_USERNAME = os.environ.get("CONDUCTOR_USERNAME")
CONDUCTOR_PASSWORD = os.environ.get("CONDUCTOR_PASSWORD")
WORKER_ID = os.environ.get("WORKER_ID")


conductor_client = ConductorClient(
    service_registration_url=SERVICE_REGISTRATION_URL,
    service_registration_token=SERVICE_REGISTRATION_TOKEN,
    conductor_base_url=CONDUCTOR_BASE_URL,
    worker_id=WORKER_ID,
    authentication_settings={
        "username": CONDUCTOR_USERNAME,
        "password": CONDUCTOR_PASSWORD,
    },
)

S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION_NAME = os.environ.get("S3_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BASE_URL = os.environ.get("S3_BASE_URL")
oss_client = OSSClient(
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    endpoint_url=S3_ENDPOINT_URL,
    region_name=S3_REGION_NAME,
    bucket_name=S3_BUCKET_NAME,
    base_url=S3_BASE_URL,
)


def signal_handler(signum, frame):
    print("SIGTERM or SIGINT signal received.")
    print("开始标记所有 task 为失败状态 ...")

    conductor_client.set_all_tasks_to_failed_state()
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def start_mock_result_thread(task):
    def handler():
        time.sleep(5)
        conductor_client.update_task_result(
            workflow_instance_id=task.get("workflowInstanceId"),
            task_id=task.get("taskId"),
            status="COMPLETED",
            output_data={"success": True},
        )

    t = threading.Thread(target=handler)
    t.start()


def test_handler(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}")

    input_data = task.get("inputData")
    chunk_size = input_data.get("chunkSize")
    chunk_overlap = input_data.get("chunkOverlap")
    language = input_data.get("language")
    txt_url = input_data.get("txtUrl")
    separator = input_data.get("separator")
    split_type = input_data.get("splitType")

    if not txt_url or not split_type or not chunk_size or not chunk_overlap:
        raise Exception("参数错误")

    tmp_file_folder = ensure_directory_exists("./download")
    txt_file_name = oss_client.download_file(txt_url, tmp_file_folder)

    with open(txt_file_name, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = None
    if split_type == "splitByCharacter":
        splitter = CharacterTextSplitter(
            separator=separator,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    elif split_type == "splitCode":
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    elif split_type == "markdown":
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    elif split_type == "recursivelySplitByCharacter":
        splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap)
    elif split_type == "splitByToken":
        splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
    else:
        raise Exception(f"split_type 参数错误")

    segments = splitter.split_text(text)
    print("转换完成")
    return {"results": segments}


if __name__ == "__main__":
    conductor_client.register_block(block_def)
    conductor_client.register_handler(block_name, test_handler)
    conductor_client.start_polling()
