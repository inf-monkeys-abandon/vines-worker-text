from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists

from src.oss import oss_client


class TextReplaceWorker(Worker):
    block_name = 'text_replace'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["text"],
        "displayName": "文本替换",
        "description": "将文档指定内容替换为另一内容，返回新的文档 URL",
        "icon": "emoji:✂️:#f3cd5f",
        "extra": {
            "estimateTime": 30,
        },
        "input": [
            {
                "displayName": "文档类型",
                "name": "documentType",
                "type": "options",
                "default": "document",
                "options": [
                    {
                        "name": "纯文本",
                        "value": "document",
                    },
                    {
                        "name": "文本 URL",
                        "value": "documentUrl",
                    },
                ],
                "required": True,
            },
            {
                "displayName": "文档文本",
                "name": "document",
                "type": "string",
                "default": "",
                "required": False,
                "displayOptions": {
                    "show": {
                        "documentType": ["document"],
                    },
                },
            },
            {
                "displayName": "文档 URL",
                "name": "documentUrl",
                "type": "file",
                "default": "",
                "required": False,
                "displayOptions": {
                    "show": {
                        "documentType": ["documentUrl"],
                    },
                },
                "typeOptions": {
                    "multipleValues": False,
                    "accept": ".txt",
                    "maxSize": 1024 * 1024 * 20
                }
            },
            {
                "displayName": "在文档中搜索的文本",
                "name": "searchText",
                "type": "string",
                "default": "",
                "required": True,
            },
            {
                "displayName": "替换搜索结果的文本",
                "name": "replaceText",
                "type": "string",
                "default": "",
                "required": True,
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "替换后的文档或文档 URL",
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
