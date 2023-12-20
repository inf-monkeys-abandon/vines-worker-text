BLOCK_NAME = "ocr"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "OCR 识别",
    "description": "使用 OCR 进行识别",
    "icon": 'emoji:🔍:#fef8a3',
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