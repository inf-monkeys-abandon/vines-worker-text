from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, CharacterTextSplitter
from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists

from src.oss import oss_client


class TextSegmentWorker(Worker):
    block_name = "text_segment"
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "displayName": "长文本分段",
        "description": "根据不同类型的文件进行文本分段",
        "icon": "emoji:✂️:#f3cd5f",
        "categories": ["text"],
        "extra": {
            "estimateTime": 60,
        },
        "input": [
            {
                "displayName": "txt 文件",
                "name": "txtUrl",
                "type": "file",
                "default": "",
                "required": True,
                "typeOptions": {
                    "multipleValues": False,
                    "accept": ".txt",
                    "maxSize": 1024 * 1024 * 20
                }
            },
            {
                "displayName": "切割器",
                "name": "splitType",
                "type": "options",
                "default": "splitByCharacter",
                "options": [
                    {
                        "name": "字符切割器",
                        "value": "splitByCharacter",
                        "description": "字符切割器",
                    },
                    {
                        "name": "代码切割器",
                        "value": "splitCode",
                        "description": "代码切割器",
                    },
                    {
                        "name": "Markdown 切割器",
                        "value": "markdown",
                        "description": "Markdown 切割器",
                    },
                    {
                        "name": "递归字符切割器",
                        "value": "recursivelySplitByCharacter",
                        "description": "递归字符切割器",
                    },
                    {
                        "name": "Token 切割器",
                        "value": "splitByToken",
                        "description": "Token 切割器",
                    },
                ],
                "required": False,
            },
            {
                "displayName": "块大小",
                "name": "chunkSize",
                "type": "number",
                "default": 2000,
                "required": True,
            },
            {
                "displayName": "块重叠",
                "name": "chunkOverlap",
                "type": "number",
                "default": 10,
                "required": True,
            },
            {
                "displayName": "分割符",
                "name": "separator",
                "type": "string",
                "default": "\n\n",
                "required": False,
                "displayOptions": {
                    "show": {
                        "splitType": [
                            "splitByCharacter",
                            "recursivelySplitByCharacter",
                        ],
                    },
                },
            },
            {
                "displayName": "语言",
                "name": "language",
                "type": "options",
                "default": "python",
                "displayOptions": {
                    "show": {
                        "splitType": ["splitCode"],
                    },
                },
                "options": [
                    {
                        "name": "cpp",
                        "value": "cpp",
                    },
                    {
                        "name": "go",
                        "value": "go",
                    },
                    {
                        "name": "java",
                        "value": "java",
                    },
                    {
                        "name": "js",
                        "value": "js",
                    },
                    {
                        "name": "php",
                        "value": "php",
                    },
                    {
                        "name": "proto",
                        "value": "proto",
                    },
                    {
                        "name": "python",
                        "value": "python",
                    },
                    {
                        "name": "rst",
                        "value": "rst",
                    },
                    {
                        "name": "ruby",
                        "value": "ruby",
                    },
                    {
                        "name": "rust",
                        "value": "rust",
                    },
                    {
                        "name": "scala",
                        "value": "scala",
                    },
                    {
                        "name": "swift",
                        "value": "swift",
                    },
                    {
                        "name": "markdown",
                        "value": "markdown",
                    },
                    {
                        "name": "latex",
                        "value": "latex",
                    },
                    {
                        "name": "html",
                        "value": "html",
                    },
                    {
                        "name": "sol",
                        "value": "sol",
                    },
                ],
                "required": True,
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "分段后的文本列表",
                "type": "string",
                "typeOptions": {
                    "multipleValues": True
                }
            },
        ],
    }

    def handler(self, task, workflow_context, credential_data):
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

