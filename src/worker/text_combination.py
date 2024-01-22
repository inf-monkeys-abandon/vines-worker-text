BLOCK_NAME = "text_combination"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "文本合并",
    "icon": "emoji:✂️:#f3cd5f",
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
                {"name": "纯文本内容", "value": "text"},
                {"name": "文本链接", "value": "url"},
            ],
        },
        {
            "displayName": "需要合并的文档列表（支持JSON，JSONL，TXT）",
            "name": "documents",
            "type": "string",
            "default": [],
            "required": False,
            "displayOptions": {"show": {"textOrUrl": ["text"]}},
            "typeOptions": {
                "multipleValues": True
            }
        },
        {
            "displayName": "需要合并的文档 URL 列表（支持JSON，JSONL，TXT）",
            "name": "documentsUrl",
            "type": "file",
            "default": [],
            "required": False,
            "displayOptions": {"show": {"textOrUrl": ["url"]}},
            "typeOptions": {
                "multipleValues": True,
                "accept": ".json,.jsonl,.txt",
                "maxSize": 1024 * 1024 * 20
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
