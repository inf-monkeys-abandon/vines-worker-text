import subprocess
import uuid

from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists
from src.oss import oss_client


class PdfToTextWorker(Worker):
    block_name = 'pdf_to_txt'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["file"],
        "displayName": "PDF 文本提取",
        "description": "从 PDF 提取纯文本",
        "icon": "emoji:📝:#56b4a2",
        "extra": {
            "estimateTime": 180,
        },
        "input": [
            {
                "displayName": "PDF 文件链接",
                "name": "pdfUrl",
                "type": "file",
                "default": "",
                "required": True,
                "typeOptions": {
                    "multipleValues": False,
                    "accept": ".pdf",
                    "maxSize": 1024 * 1024 * 20
                }
            },
        ],
        "output": [
            {
                "name": "result",
                "displayName": "txt 文件链接",
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
