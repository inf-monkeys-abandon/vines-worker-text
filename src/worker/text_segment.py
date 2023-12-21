BLOCK_NAME = "text_segment"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "displayName": "长文本分段",
    "description": "根据不同类型的文件进行文本分段",
    "icon": "emoji:✂️:#f3cd5f",
    "categories": ["text"],
    "extra": {
        "estimateTime": 60,
    },
    "input": [
        {
            "displayName": "txt 文件",
            "name": "txtUrl",
            "type": "string",
            "default": "",
            "required": True,
        },
        {
            "displayName": "切割器",
            "name": "splitType",
            "type": "options",
            "default": "splitByCharacter",
            "options": [
                {
                    "name": "字符切割器",
                    "value": "splitByCharacter",
                    "description": "字符切割器",
                },
                {
                    "name": "代码切割器",
                    "value": "splitCode",
                    "description": "代码切割器",
                },
                {
                    "name": "Markdown 切割器",
                    "value": "markdown",
                    "description": "Markdown 切割器",
                },
                {
                    "name": "递归字符切割器",
                    "value": "recursivelySplitByCharacter",
                    "description": "递归字符切割器",
                },
                {
                    "name": "Token 切割器",
                    "value": "splitByToken",
                    "description": "Token 切割器",
                },
            ],
            "required": False,
        },
        {
            "displayName": "块大小",
            "name": "chunkSize",
            "type": "number",
            "default": 2000,
            "required": True,
        },
        {
            "displayName": "块重叠",
            "name": "chunkOverlap",
            "type": "number",
            "default": 10,
            "required": True,
        },
        {
            "displayName": "分割符",
            "name": "separator",
            "type": "string",
            "default": "\n\n",
            "required": False,
            "displayOptions": {
                "show": {
                    "splitType": [
                        "splitByCharacter",
                        "recursivelySplitByCharacter",
                    ],
                },
            },
        },
        {
            "displayName": "语言",
            "name": "language",
            "type": "options",
            "default": "python",
            "displayOptions": {
                "show": {
                    "splitType": ["splitCode"],
                },
            },
            "options": [
                {
                    "name": "cpp",
                    "value": "cpp",
                },
                {
                    "name": "go",
                    "value": "go",
                },
                {
                    "name": "java",
                    "value": "java",
                },
                {
                    "name": "js",
                    "value": "js",
                },
                {
                    "name": "php",
                    "value": "php",
                },
                {
                    "name": "proto",
                    "value": "proto",
                },
                {
                    "name": "python",
                    "value": "python",
                },
                {
                    "name": "rst",
                    "value": "rst",
                },
                {
                    "name": "ruby",
                    "value": "ruby",
                },
                {
                    "name": "rust",
                    "value": "rust",
                },
                {
                    "name": "scala",
                    "value": "scala",
                },
                {
                    "name": "swift",
                    "value": "swift",
                },
                {
                    "name": "markdown",
                    "value": "markdown",
                },
                {
                    "name": "latex",
                    "value": "latex",
                },
                {
                    "name": "html",
                    "value": "html",
                },
                {
                    "name": "sol",
                    "value": "sol",
                },
            ],
            "required": True,
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "分段后的文本列表",
            "type": "collection",
        },
    ],
}
