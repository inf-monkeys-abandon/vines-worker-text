from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists

from src.oss import oss_client
from src.utils.ocr_helper import OCRHelper


class PPStructureWorker(Worker):
    block_name = 'pp_structure'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["file"],
        "displayName": "版面恢复",
        "description": "对复杂文档进行分析和处理",
        "icon": "emoji:📝:#56b4a2",
        "extra": {
            "estimateTime": 60,
        },
        "input": [
            {
                "displayName": "文件 URL",
                "name": "url",
                "type": "file",
                "default": "",
                "required": True,
                "typeOptions": {
                    "multipleValues": False,
                    "accept": ".jpg,.jpeg,.png",
                    "maxSize": 1024 * 1024 * 20
                }
            },
            {
                "displayName": "主要语言",
                "name": "lang",
                "type": "options",
                "default": "ch",
                "required": True,
                "options": [
                    {
                        "name": "ch",
                        "value": "ch",
                    },
                    {
                        "name": "en",
                        "value": "en",
                    },
                ],
            },
            # {
            #     "displayName": "启用版面分析",
            #     "name": "enableStructure",
            #     "type": "boolean",
            #     "default": "",
            #     "required": True,
            # },
            {
                "displayName": "启用表格识别",
                "name": "enableTableStructure",
                "type": "boolean",
                "default": "",
                "required": True,
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "文档 URL",
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
        url = input_data.get("url")
        lang = input_data.get("lang")
        isImage = input_data.get("isImage")
        folder = ensure_directory_exists(f"./download/{task_id}")
        input_file = oss_client.download_file(url, folder)
        ocr_helper = OCRHelper()
        try:
            result = ocr_helper.recognize_text(img_path=str(input_file), task_id=task_id)
            if result is None:
                raise Exception("版面恢复失败")
            # 上传 docx 文件到 OSS
            file_url = oss_client.upload_file_tos(result, key=f"workflow/artifact/{task_id}/{result.split('/')[-1]}")
            return {
                "result": file_url,
            }
        except Exception as e:
            raise Exception(f"版面恢复失败: {e}")
