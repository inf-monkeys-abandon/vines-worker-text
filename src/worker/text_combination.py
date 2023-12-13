BLOCK_NAME = "text_combination"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "文本合并",
    "icon": "emoji:🫶:#fef8a3",
    "extra": {
        "estimateTime": 30,
    },
    "input": [
        {
            "displayName": "文档类型",
            "name": "textOrUrl",
            "type": "options",
            "default": "text",
            "required": False,
            "options": [
                {
                    "name": "纯文本内容",
                    "value": "text"
                },
                {
                    "name": "文本链接",
                    "value": "url"
                }
            ]
        },
        {
            "displayName": "需要合并的文档列表（支持JSON，JSONL，TXT）",
            "name": "documents",
            "type": "collection",
            "default": [],
            "required": False,
            "displayOptions": {
                "show": {
                    "textOrUrl": ["text"]
                }
            }
        },
        {
            "displayName": "需要合并的文档 URL 列表（支持JSON，JSONL，TXT）",
            "name": "documentsUrl",
            "type": "collection",
            "default": [],
            "required": False,
            "displayOptions": {
                "show": {
                    "textOrUrl": ["url"]
                }
            }
        },
        {
            "displayName": "文本格式",
            "name": "documentType",
            "type": "options",
            "options": [
                {
                    "name": "JSON",
                    "value": "json",
                },
                {
                    "name": "JSONL",
                    "value": "jsonl",
                },
                {
                    "name": "TXT",
                    "value": "txt",
                },
            ],
            "default": "txt",
            "required": True,
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "合并后的输出的文本URL",
            "type": "string",
        },
    ],
}
