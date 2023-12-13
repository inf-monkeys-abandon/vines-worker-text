import sys

from vines_worker_sdk.conductor import ConductorClient
from vines_worker_sdk.oss import OSSClient
from vines_worker_sdk.utils.files import ensure_directory_exists
from block_def import (
    block_def,
    block_name,
    block_def_2,
    block_name_2,
    block_def_3,
    block_name_3,
    block_name_4,
    block_def_4,
    block_name_5,
    block_def_5,
)
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
import subprocess
from src.ocr_helper import OCRHelper
load_dotenv()

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


SERVICE_REGISTRATION_URL = os.environ.get("SERVICE_REGISTRATION_URL")
SERVICE_REGISTRATION_TOKEN = os.environ.get("SERVICE_REGISTRATION_TOKEN")
CONDUCTOR_BASE_URL = os.environ.get("CONDUCTOR_BASE_URL")
CONDUCTOR_USERNAME = os.environ.get("CONDUCTOR_USERNAME")
CONDUCTOR_PASSWORD = os.environ.get("CONDUCTOR_PASSWORD")
WORKER_ID = os.environ.get("WORKER_ID")


conductor_client = ConductorClient(
    poll_interval_ms=10,
    service_registration_url=SERVICE_REGISTRATION_URL,
    service_registration_token=SERVICE_REGISTRATION_TOKEN,
    conductor_base_url=CONDUCTOR_BASE_URL,
    worker_id=WORKER_ID,
    authentication_settings={
        "username": CONDUCTOR_USERNAME,
        "password": CONDUCTOR_PASSWORD,
    },
    external_storage=oss_client,
    task_output_payload_size_threshold_kb=1024 * 10
)


def signal_handler(signum, frame):
    print("SIGTERM or SIGINT signal received.")
    print("开始标记所有 task 为失败状态 ...")

    conductor_client.set_all_tasks_to_failed_state()
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def text_segment_handler(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    task_type = task.get('taskType')
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")

    input_data = task.get("inputData")
    chunk_size = input_data.get("chunkSize")
    chunk_overlap = input_data.get("chunkOverlap")
    language = input_data.get("language")
    txt_url = input_data.get("txtUrl")
    separator = input_data.get("separator")
    split_type = input_data.get("splitType")
    print(input_data)
    if not txt_url or not split_type or not chunk_size or not chunk_overlap:
        raise Exception("参数错误")

    tmp_file_folder = ensure_directory_exists("./download")
    txt_file_name = oss_client.download_file(txt_url, tmp_file_folder)

    text = ""
    try:
        with open(txt_file_name, "r", encoding="utf-8") as f:
            text = f.read()
    except:
        raise Exception("读取文件失败，请传入合法的 utf-8 格式的 txt 文件")

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
    return {"result": segments}


def text_replace_handler(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    task_type = task.get('taskType')
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")
    input_data = task.get("inputData")
    print(input_data)

    document_type = input_data.get("documentType")
    if document_type == "document":
        input_data.pop("documentUrl")
    elif document_type == "documentUrl":
        input_data.pop("document")

    text = input_data.get("searchText")
    replace_text = input_data.get("replaceText")
    document = input_data.get("document")
    document_url = input_data.get("documentUrl")
    if not text or (not document and not document_url):
        raise Exception("参数错误")

    if document:
        document = document.replace(text, replace_text)
        return {"result": document}
    elif document_url:
        tmp_file_folder = ensure_directory_exists("./download")
        file_name = oss_client.download_file(document_url, tmp_file_folder)
        with open(file_name, "r") as f:
            lines = f.readlines()
        lines = [line.replace(text, replace_text) for line in lines]
        with open(file_name, "w") as f:
            for line in lines:
                f.write(line)
        url = oss_client.upload_file_tos(file_name, f"workflow/artifact/{task_id}/result.txt")
        return {"result": url}


def text_combination_handler(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    task_type = task.get('taskType')
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")

    input_data = task.get("inputData")

    documents = input_data.get("documents")
    documents_url = input_data.get("documentsUrl")
    if isinstance(documents_url, str):
        documents_url = [documents_url]
    document_type = input_data.get("documentType")  # 支持 json，jsonl, txt

    if not documents and not documents_url:
        raise Exception("参数错误：未提供文档")
    if document_type not in ["json", "jsonl", "txt"]:
        raise Exception("参数错误：不支持的文档类型")

    folder = ensure_directory_exists(f"./download/text_combination/{task_id}")
    # 合并本地文件
    if len(documents) > 1:
        document_list = []
        for document in documents:
            if document_type == "json":
                document_list.append(json.load(document))
            elif document_type == "jsonl":
                for line in document.split("\n"):
                    document_list.append(json.loads(line))
            elif document_type == "txt":
                document_list.append(document)

        filename = f"{folder}/all.{document_type}"
        with open(filename, "w") as f:
            if document_type == "json":
                json.dump(document_list, f)
            elif document_type == "jsonl":
                for document in document_list:
                    f.write(json.dumps(document))
                    f.write("\n")
            elif document_type == "txt":
                for document in document_list:
                    f.write(f"{document}")
                    f.write("\n")
        url = oss_client.upload_file_tos(filename, f"workflow/artifact/{task_id}/result.txt")
        return {"result": url}
    else:
        # 下载需要合并的文件到本地
        for document_url in documents_url:
            oss_client.download_file(document_url, folder)
            print(f"{len(documents_url)}个文件下载完成，开始合并")
        all_document_file = os.listdir(folder)
        document_list = []
        document = documents[0]
        if document_type == "json":
            document_list.append(json.load(document))
        elif document_type == "jsonl":
            for line in document.split("\n"):
                document_list.append(json.loads(line))
        elif document_type == "txt":
            document_list.append(document)

        for document_file in all_document_file:
            file_ext = document_file.split(".")[-1]
            file_name = f"{folder}/{document_file}"
            if file_ext != document_type:
                raise Exception(f"配置的文档类型为 {document_type}，但是实际上文档类型为 {file_ext}")
            if document_type == "json":
                with open(file_name, "r") as f:
                    document_list.append(json.load(f))
            elif document_type == "jsonl":
                with open(file_name, "r") as f:
                    for line in f.readlines():
                        document_list.append(json.loads(line))
            elif document_type == "txt":
                with open(file_name, "r") as f:
                    document_list.append(f.read())
        all_filename = f"{folder}/all.{document_type}"
        print(all_filename, document_type)
        with open(all_filename, "w") as f:
            if document_type == "json":
                json.dump(document_list, f)
            elif document_type == "jsonl":
                for document in document_list:
                    f.write(json.dumps(document))
                    f.write("\n")
            elif document_type == "txt":
                for document in document_list:
                    f.write(document)
                    f.write("\n")
        url = oss_client.upload_file_tos(
            all_filename, f"workflow/artifact/{task_id}/result.{document_type}"
        )
        return {"result": url}

def pdf_to_txt_handler(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    task_type = task.get('taskType')
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")

    input_data = task.get("inputData")
    print(input_data)

    folder = ensure_directory_exists(f"./download/{task_id}")
    pdf_folder = ensure_directory_exists(f"./download/{task_id}/pdf")
    docx_folder = ensure_directory_exists(f"./download/{task_id}/docx")
    md_folder = ensure_directory_exists(f"./download/{task_id}/md")
    txt_folder = ensure_directory_exists(f"./download/{task_id}/txt")
    pdfUrl = input_data.get("pdfUrl")
    if not pdfUrl:
        raise Exception("任务参数中不存在 pdfUrl")
    pdf_file = oss_client.download_file(pdfUrl, pdf_folder)
    pdf_name = pdf_file.split("/")[-1]

    # pdf to docx
    cmd = [
        "paddleocr",
        "--image_dir",
        pdf_file,
        "--type",
        "structure",
        "--recovery",
        "true",
        "--use_pdf2docx_api",
        "true",
        "--output",
        docx_folder,
    ]
    try:
        result = subprocess.run(cmd, shell=False, check=True)
        if result.returncode == 0:
            print(f"版面识别成功，docx 文件地址为 {docx_folder}")
    except subprocess.CalledProcessError as e:
        print(f"版面识别失败，错误信息为 {e}")
        raise Exception("版面识别失败")

    docx_path = f"{docx_folder}/{pdf_name.replace('.pdf', '.docx')}"
    md_path = f"{md_folder}/{pdf_name.replace('.pdf', '.md')}"
    cmd = [
        "pandoc",
        "-s",
        docx_path,
        "--wrap=none",
        "--reference-links",
        "-t",
        "markdown",
        "-o",
        md_path,
    ]
    try:
        result = subprocess.run(cmd, shell=False, check=True)
        if result.returncode == 0:
            print(f"pandoc 转换成功，转换之后的 Markdown 文件地址为 {md_path}")
    except subprocess.CalledProcessError as e:
        print(f"pandoc 转换失败，错误信息为 {e}")
        raise Exception("pandoc 转换失败")

    txt_path = f"{txt_folder}/{pdf_name.replace('.pdf', '.txt')}"
    cmd = [
        "pandoc",
        md_path,
        "-o",
        txt_path,
    ]
    try:
        result = subprocess.run(cmd, shell=False, check=True)
        if result.returncode == 0:
            print(f"pandoc 转换成功，转换之后的 txt 文件地址为 {txt_path}")
    except subprocess.CalledProcessError as e:
        print(f"pandoc 转换失败，错误信息为 {e}")
        raise Exception("pandoc 转换失败")
    
    url = oss_client.upload_file_tos(txt_path, f"workflow/artifact/{task_id}/{uuid.uuid4()}.txt")


    return {"result": url}


def pp_structure(task):
    workflow_instance_id = task.get("workflowInstanceId")
    task_id = task.get("taskId")
    task_type = task.get('taskType')
    print(f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")

    input_data = task.get("inputData")
    print(input_data)
    url = input_data.get("url")
    lang = input_data.get("lang")
    isImage = input_data.get("isImage")
    folder = ensure_directory_exists(f"./download/{task_id}")

    ocr_helper = OCRHelper()
    try:
        result = ocr_helper.recognize_text(img_path=str(input_file),task_id=task_id)
        if result is None:
            raise Exception("版面恢复失败")
        # 上传 docx 文件到 OSS
        file_url = oss_client.upload_file_tos(result, key=f"workflow/artifact/{task_id}/{result.split('/')[-1]}")
        return {
            "result": file_url,
        }
    except Exception as e:
        raise Exception(f"版面恢复失败: {e}")


if __name__ == "__main__":
    conductor_client.register_block(block_def)
    conductor_client.register_block(block_def_2)
    conductor_client.register_block(block_def_3)
    conductor_client.register_block(block_def_4)
    conductor_client.register_handler(block_name, text_segment_handler)
    conductor_client.register_handler(block_name_2, text_replace_handler)
    conductor_client.register_handler(block_name_3, text_combination_handler)
    conductor_client.register_handler(block_name_4, pdf_to_txt_handler)
    # conductor_client.register_handler(block_name_5, pp_structure)

    conductor_client.start_polling()
