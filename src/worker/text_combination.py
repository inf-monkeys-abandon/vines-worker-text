import json
import os

from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists

from src.oss import oss_client


class TextCombinationWorker(Worker):
    block_name = 'text_combination'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["text"],
        "displayName": "文本合并",
        "icon": "emoji:✂️:#f3cd5f",
        "extra": {
            "estimateTime": 30,
        },
        "input": [
            {
                "displayName": "文档类型",
                "name": "textOrUrl",
                "type": "options",
                "default": "text",
                "required": False,
                "options": [
                    {"name": "纯文本内容", "value": "text"},
                    {"name": "文本链接", "value": "url"},
                ],
            },
            {
                "displayName": "需要合并的文档列表（支持JSON，JSONL，TXT）",
                "name": "documents",
                "type": "string",
                "default": [],
                "required": False,
                "displayOptions": {"show": {"textOrUrl": ["text"]}},
                "typeOptions": {
                    "multipleValues": True
                }
            },
            {
                "displayName": "需要合并的文档 URL 列表（支持JSON，JSONL，TXT）",
                "name": "documentsUrl",
                "type": "file",
                "default": [],
                "required": False,
                "displayOptions": {"show": {"textOrUrl": ["url"]}},
                "typeOptions": {
                    "multipleValues": True,
                    "accept": ".json,.jsonl,.txt",
                    "maxSize": 1024 * 1024 * 20
                }
            },
            {
                "displayName": "文本格式",
                "name": "documentType",
                "type": "options",
                "options": [
                    {
                        "name": "JSON",
                        "value": "json",
                    },
                    {
                        "name": "JSONL",
                        "value": "jsonl",
                    },
                    {
                        "name": "TXT",
                        "value": "txt",
                    },
                ],
                "default": "txt",
                "required": True,
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "合并后的输出的文本URL",
                "type": "string",
            },
        ],
    }

    def handler(self, task, workflow_context, credential_data):
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
