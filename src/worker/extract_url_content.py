BLOCK_NAME = "extract_url_content"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "提取 URL 内容",
    "description": "从 URL 中提取 HTML 内容",
    "icon": "emoji:🤏:#fef8a",
    "extra": {
        "estimateTime": 30,
    },
    "input": [
        {
            "displayName": "启用 Headless Browser",
            "name": "headless",
            "type": "boolean",
            "default": "",
            "required": True,
        },
        {
            "displayName": "URL",
            "name": "url",
            "type": "string",
            "default": "",
            "required": True,
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "提取结果",
            "type": "collection",
            "properties": [
                {
                    "name": "metadata",
                    "displayName": "元数据",
                    "type": "any",
                },
                {
                    "name": "page_content",
                    "displayName": "文本内容",
                    "type": "string",
                },
            ],
        },
    ],
}
