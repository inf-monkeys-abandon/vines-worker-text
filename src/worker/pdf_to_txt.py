BLOCK_NAME = "pdf_to_txt"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "PDF 转 TXT",
    "description": "从 PDF 提取纯文本",
    "icon": "emoji:📄:#fef8a3",
    "extra": {
        "estimateTime": 180,
    },
    "input": [
        {
            "displayName": "PDF 文件链接",
            "name": "pdfUrl",
            "type": "string",
            "default": "",
            "required": True,
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
