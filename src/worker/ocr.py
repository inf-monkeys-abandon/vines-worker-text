from paddleocr import PaddleOCR
from vines_worker_sdk.conductor.worker import Worker
from vines_worker_sdk.utils.files import ensure_directory_exists

from src.oss import oss_client


class OCRWorker(Worker):
    block_name = 'ocr'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["file"],
        "displayName": "OCR 识别",
        "description": "使用 OCR 进行识别",
        "icon": "emoji:📝:#56b4a2",
        "extra": {
            "estimateTime": 10,
        },
        "input": [
            {
                "displayName": "图片 URL",
                "name": "url",
                "type": "file",
                "default": "",
                "required": True,
                "typeOptions": {
                    "multipleValues": False,
                    "accept": ".jpg,.jpeg,.png",
                    "maxSize": 1024 * 1024 * 20
                }
            }
        ],
        "output": [
            {
                "name": "result",
                "displayName": "识别结果 TXT",
                "type": "string",
            },
        ],
    }

    def handler(self, task, workflow_context, credential_data):
        workflow_instance_id = task.get("workflowInstanceId")
        task_id = task.get("taskId")
        print(
            f"开始执行任务：workflow_instance_id={workflow_instance_id}, task_id={task_id}")

        input_data = task.get("inputData")
        image_url = input_data.get("url")
        tmp_file_folder = ensure_directory_exists("./download")
        image_file_name = oss_client.download_file(image_url, tmp_file_folder)

        ocr = PaddleOCR(
            # 检测模型
            # det_model_dir='{your_det_model_dir}',
            # # 识别模型
            # rec_model_dir='{your_rec_model_dir}',
            # # 识别模型字典
            # rec_char_dict_path='{your_rec_char_dict_path}',
            # # 分类模型
            # cls_model_dir='{your_cls_model_dir}',
            # 加载分类模型
            use_angle_cls=True,
            lang='ch',
        )
        result = ocr.ocr(image_file_name, cls=True)
        extracted_texts = []
        for item in result:
            for text_block in item:
                text = text_block[1][0]
                extracted_texts.append(text)
        text = "\n".join(extracted_texts)

        print(text)
        return {"result": text}
