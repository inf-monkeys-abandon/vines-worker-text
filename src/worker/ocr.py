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
            "type": "string",
            "default": "",
            "required": True,
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
