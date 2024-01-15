BLOCK_NAME = "pdf_to_txt"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
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
