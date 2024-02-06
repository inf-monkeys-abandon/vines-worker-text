from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.string import generate_random_string

from src.oss import oss_client
from src.utils.file_convert_helper import FileConvertHelper


class FileConvertWorker(Worker):
    block_name = 'file_convert'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["file"],
        "displayName": "文件格式转换",
        "description": "对文件格式进行转换",
        "icon": "emoji:📝:#56b4a2",
        "extra": {
            "estimateTime": 10,
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
                    "accept": ".png,.jpg,.pdf,.docx,.xlsx,.csv,.md",
                    "maxSize": 1024 * 1024 * 20
                }
            },
            {
                "displayName": "输入格式",
                "name": "input_format",
                "type": "options",
                "default": "PNG",
                "required": True,
                "options": [
                    {
                        "name": "PNG",
                        "value": "png",
                    },
                    {
                        "name": "JPG",
                        "value": "jpg",
                    },
                    {
                        "name": "PDF",
                        "value": "pdf",
                    },
                    {
                        "name": "DOCX",
                        "value": "docx",
                    },
                    {
                        "name": "XLSX",
                        "value": "xlsx",
                    },
                    {
                        "name": "CSV",
                        "value": "csv",
                    },
                    {
                        "name": "MD",
                        "value": "md",
                    },
                ],
            },
            {
                "displayName": "输出格式",
                "name": "output_format",
                "type": "options",
                "default": "",
                "required": True,
                "options": [
                    {
                        "name": "PNG",
                        "value": "png",
                    },
                    {
                        "name": "JPG",
                        "value": "jpg",
                    },
                ],
                "displayOptions": {
                    "show": {
                        "input_format": ["jpg", "png"],
                    }
                },
            },
            {
                "displayName": "输出格式",
                "name": "output_format",
                "type": "options",
                "default": "",
                "required": True,
                "options": [
                    {
                        "name": "PDF",
                        "value": "pdf",
                    },
                    {
                        "name": "DOCX",
                        "value": "docx",
                    },
                    {
                        "name": "Markdown",
                        "value": "md",
                    },
                ],
                "displayOptions": {
                    "show": {
                        "input_format": ["pdf", "docx", "md"],
                    }
                },
            },
            {
                "displayName": "输出格式",
                "name": "output_format",
                "type": "options",
                "default": "",
                "required": True,
                "options": [
                    {
                        "name": "XLSX",
                        "value": "xlsx",
                    },
                    {
                        "name": "CSV",
                        "value": "csv",
                    },
                ],
                "displayOptions": {
                    "show": {
                        "input_format": ["xlsx", "csv"],
                    }
                },
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "转换后结果的 URL",
                "type": "any",
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
        helper = FileConvertHelper(url)
        input_format = input_data.get("input_format")
        output_format = input_data.get("output_format")

        # 1. 将文件下载到本地
        task_id = task.task_id if task is not None else generate_random_string(20)
        input_file = helper.download_file(url, "tmp/" + task_id)

        # 2. 根据 input_format 调用helper
        if input_format == "png" or input_format == "jpg":
            output_file = input_file + "." + output_format
            helper.convert_image(input_file, output_file, output_format)
        elif input_format == "pdf" and output_format == "docx":
            output_file = input_file + "." + output_format
            helper.pdf_to_docx(input_file, output_file)
        elif input_format == "docx" and output_format == "md":
            output_file = input_file + "." + output_format
            helper.docx_to_markdown(input_file, output_file)
        elif input_format == "pdf" and output_format == "md":
            output_file = input_file + "." + output_format
            helper.pdf_to_markdown(input_file, output_file)
        elif input_format == "xlsx" and output_format == "csv":
            output_file = input_file + "." + output_format
            helper.xlsx_to_csv(input_file, output_file)
        elif input_format == "csv" and output_format == "xlsx":
            output_file = input_file + "." + output_format
            helper.csv_to_xlsx(input_file, output_file)
        else:
            raise Exception("不支持的格式转换")
        # 3. 将文件上传到 OSS
        url = oss_client.upload_file_tos(output_file, key=f"workflow/artifact/{task_id}/{output_file.split('/')[-1]}")
        print("txt_url", url)
        # 4. 返回文件 URL
        return {
            "result": url,
        }

