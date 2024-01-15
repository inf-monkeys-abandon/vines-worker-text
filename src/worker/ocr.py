BLOCK_NAME = "ocr"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
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
