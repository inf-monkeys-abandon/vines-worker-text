BLOCK_NAME = "text_replace"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "文本替换",
    "description": "将文档指定内容替换为另一内容，返回新的文档 URL",
    "icon": "emoji:✂️:#f3cd5f",
    "extra": {
        "estimateTime": 30,
    },
    "input": [
        {
            "displayName": "文档类型",
            "name": "documentType",
            "type": "options",
            "default": "document",
            "options": [
                {
                    "name": "纯文本",
                    "value": "document",
                },
                {
                    "name": "文本 URL",
                    "value": "documentUrl",
                },
            ],
            "required": True,
        },
        {
            "displayName": "文档文本",
            "name": "document",
            "type": "string",
            "default": "",
            "required": False,
            "displayOptions": {
                "show": {
                    "documentType": ["document"],
                },
            },
        },
        {
            "displayName": "文档 URL",
            "name": "documentUrl",
            "type": "string",
            "default": "",
            "required": False,
            "displayOptions": {
                "show": {
                    "documentType": ["documentUrl"],
                },
            },
        },
        {
            "displayName": "在文档中搜索的文本",
            "name": "searchText",
            "type": "string",
            "default": "",
            "required": True,
        },
        {
            "displayName": "替换搜索结果的文本",
            "name": "replaceText",
            "type": "string",
            "default": "",
            "required": True,
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "替换后的文档或文档 URL",
            "type": "string",
        },
    ],
}
