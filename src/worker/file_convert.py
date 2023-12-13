BLOCK_NAME = "file_convert"
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["text"],
    "displayName": "文件格式转换",
    "description": "对文件格式进行转换",
    "icon": "emoji:🔁:#fef8a",
    "extra": {
        "estimateTime": 10,
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
            "displayName": "输入格式",
            "name": "input_format",
            "type": "options",
            "default": "PNG",
            "required": True,
            "options": [
                {
                    "name": "PNG",
                    "value": "png",
                },
                {
                    "name": "JPG",
                    "value": "jpg",
                },
                {
                    "name": "PDF",
                    "value": "pdf",
                },
                {
                    "name": "DOCX",
                    "value": "docx",
                },
                {
                    "name": "XLSX",
                    "value": "xlsx",
                },
                {
                    "name": "CSV",
                    "value": "csv",
                },
                {
                    "name": "MD",
                    "value": "md",
                },
            ],
        },
        {
            "displayName": "输出格式",
            "name": "output_format",
            "type": "options",
            "default": "",
            "required": True,
            "options": [
                {
                    "name": "PNG",
                    "value": "png",
                },
                {
                    "name": "JPG",
                    "value": "jpg",
                },
            ],
            "displayOptions": {
                "show": {
                    "input_format": ["jpg", "png"],
                }
            },
        },
        {
            "displayName": "输出格式",
            "name": "output_format",
            "type": "options",
            "default": "",
            "required": True,
            "options": [
                {
                    "name": "PDF",
                    "value": "pdf",
                },
                {
                    "name": "DOCX",
                    "value": "docx",
                },
                {
                    "name": "Markdown",
                    "value": "md",
                },
            ],
            "displayOptions": {
                "show": {
                    "input_format": ["pdf", "docx", "md"],
                }
            },
        },
        {
            "displayName": "输出格式",
            "name": "output_format",
            "type": "options",
            "default": "",
            "required": True,
            "options": [
                {
                    "name": "XLSX",
                    "value": "xlsx",
                },
                {
                    "name": "CSV",
                    "value": "csv",
                },
            ],
            "displayOptions": {
                "show": {
                    "input_format": ["xlsx", "csv"],
                }
            },
        },
    ],
    "output": [
        {
            "name": "result",
            "displayName": "转换后结果的 URL",
            "type": "any",
        },
    ],
}
