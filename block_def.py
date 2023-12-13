block_name = "text_segment"
block_def = {
    "type": "SIMPLE",
    "name": block_name,
    "displayName": "长文本分段",
    "description": "根据不同类型的文件进行文本分段",
    "icon": "emoji:✂️:#fef8a3",
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


block_name_2 = "text_replace"
block_def_2 = {
    "type": "SIMPLE",
    "name": block_name_2,
    "categories": ["text"],
    "displayName": "文本替换",
    "description": "将文档指定内容替换为另一内容，返回新的文档 URL",
    "icon": "emoji:🤏:#fef8a3",
    "extra": {
        "estimateTime": 30,
    },
    "input": [
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
        {
            "displayName": "文档类型",
            "name": "documentType",
            "type": "options",
            "default": "",
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
    ],
    "output": [
        {
            "name": "result",
            "displayName": "替换后的文档或文档 URL",
            "type": "string",
        },
    ],
}

block_name_3 = "text_combination"
block_def_3 = {
    "type": "SIMPLE",
    "name": block_name_3,
    "categories": ["text"],
    "displayName": "文本合并",
    "icon": "emoji:🫶:#fef8a3",
    "extra": {
        "estimateTime": 30,
    },
    "input": [
        {
            "displayName": "需要合并的文档列表（二选一，支持JSON，JSONL，TXT）",
            "name": "documents",
            "type": "collection",
            "default": [],
            "required": False,
        },
        {
            "displayName": "需要合并的文档 URL 列表（二选一，支持JSON，JSONL，TXT）",
            "name": "documentsUrl",
            "type": "collection",
            "default": [],
            "required": False,
        },
        {
            "displayName": "文档类型",
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


block_name_4 = "pdf_to_txt"
block_def_4 = {
    "type": "SIMPLE",
    "name": block_name_4,
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


block_name_5 = "pp_structure"
block_def_5 = {
    "type": "SIMPLE",
    "name": block_name_5,
    "categories": ["text"],
    "displayName": "版面恢复",
    "description": "对复杂文档进行分析和处理",
    "icon": "emoji:🤏:#fef8a3",
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
