BLOCK_NAME = "pp_structure"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["file"],
    "displayName": "版面恢复",
    "description": "对复杂文档进行分析和处理",
    "icon": "emoji:📝:#56b4a2",
    "extra": {
        "estimateTime": 60,
    },
    "input": [
        {
            "displayName": "文件 URL",
            "name": "url",
            "type": "string",
            "default": "",
            "required": True,
        },
        {
            "displayName": "主要语言",
            "name": "lang",
            "type": "options",
            "default": "ch",
            "required": True,
            "options": [
                {
                    "name": "ch",
                    "value": "ch",
                },
                {
                    "name": "en",
                    "value": "en",
                },
            ],
        },
        # {
        #     "displayName": "启用版面分析",
        #     "name": "enableStructure",
        #     "type": "boolean",
        #     "default": "",
        #     "required": True,
        # },
        {
            "displayName": "启用表格识别",
            "name": "enableTableStructure",
            "type": "boolean",
            "default": "",
            "required": True,
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "文档 URL",
            "type": "string",
        },
    ],
}
