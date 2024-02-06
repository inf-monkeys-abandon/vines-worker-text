from langchain_community.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
from vines_worker_sdk.conductor.worker import Worker


class ExtractUrlContentWorker(Worker):
    block_name = 'extract_url_content'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["file"],
        "displayName": "URL 文本提取",
        "description": "从 URL 中提取 HTML 内容",
        "icon": "emoji:📝:#56b4a2",
        "extra": {
            "estimateTime": 30,
        },
        "input": [
            {
                "displayName": "启用 Headless Browser",
                "name": "headless",
                "type": "boolean",
                "default": "",
                "required": True,
            },
            {
                "displayName": "URL",
                "name": "url",
                "type": "string",
                "default": "",
                "required": True,
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "提取结果",
                "type": "string",
                "properties": [
                    {
                        "name": "metadata",
                        "displayName": "元数据",
                        "type": "any",
                    },
                    {
                        "name": "page_content",
                        "displayName": "文本内容",
                        "type": "string",
                    },
                ],
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
        url = input_data.get("url")
        headless = input_data.get("headless")
        try:
            if url is None:
                raise Exception("URL 不能为空")
            if headless:
                loader = UnstructuredURLLoader(urls=[url])
            else:
                loader = SeleniumURLLoader(urls=[url])
            document = loader.load()
            result = {}
            for doc in document:
                result["metadata"] = doc.metadata
                result["page_content"] = doc.page_content
            # FIX 不能直接返回 json 数据，否则 conductor 序列化会报错
            return {
                "result": result,
            }
        except Exception as e:
            raise Exception(f"提取 URL 中的文本失败: {e}")
