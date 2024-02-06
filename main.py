from dotenv import load_dotenv

from src.oss import oss_client

load_dotenv()

import sys
from vines_worker_sdk.conductor import ConductorClient
import signal
import os
from src.worker.extract_url_content import ExtractUrlContentWorker
from src.worker.file_convert import FileConvertWorker
from src.worker.ocr import OCRWorker
from src.worker.pdf_to_txt import PdfToTextWorker
from src.worker.pp_structure import PPStructureWorker
from src.worker.text_combination import TextCombinationWorker
from src.worker.text_replace import TextReplaceWorker
from src.worker.text_segment import TextSegmentWorker

SERVICE_REGISTRATION_URL = os.environ.get("SERVICE_REGISTRATION_URL")
SERVICE_REGISTRATION_TOKEN = os.environ.get("SERVICE_REGISTRATION_TOKEN")
CONDUCTOR_BASE_URL = os.environ.get("CONDUCTOR_BASE_URL")
CONDUCTOR_CLIENT_NAME_PREFIX = os.environ.get("CONDUCTOR_CLIENT_NAME_PREFIX", "")
CONDUCTOR_USERNAME = os.environ.get("CONDUCTOR_USERNAME")
CONDUCTOR_PASSWORD = os.environ.get("CONDUCTOR_PASSWORD")
WORKER_ID = os.environ.get("WORKER_ID")
REDIS_URL = os.environ.get("REDIS_URL")

CONDUCTOR_EXTERNAL_STORAGE_TMP_FOLDER = os.path.join(os.path.dirname(__file__), "external-storage")
conductor_client = ConductorClient(
    redis_url=REDIS_URL,
    service_registration_url=SERVICE_REGISTRATION_URL,
    service_registration_token=SERVICE_REGISTRATION_TOKEN,
    conductor_base_url=CONDUCTOR_BASE_URL,
    worker_name_prefix=CONDUCTOR_CLIENT_NAME_PREFIX,
    worker_id=WORKER_ID,
    authentication_settings={
        "username": CONDUCTOR_USERNAME,
        "password": CONDUCTOR_PASSWORD,
    },
    external_storage=oss_client,
    external_storage_tmp_folder=CONDUCTOR_EXTERNAL_STORAGE_TMP_FOLDER,
)


def signal_handler(signum, frame):
    print("SIGTERM or SIGINT signal received.")
    print("开始标记所有 task 为失败状态 ...")

    conductor_client.set_all_tasks_to_failed_state()
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    conductor_client.register_worker(ExtractUrlContentWorker())
    conductor_client.register_worker(FileConvertWorker())
    conductor_client.register_worker(OCRWorker())
    conductor_client.register_worker(PdfToTextWorker())
    conductor_client.register_worker(PPStructureWorker())
    conductor_client.register_worker(TextCombinationWorker())
    conductor_client.register_worker(TextReplaceWorker())
    conductor_client.register_worker(TextSegmentWorker())
    conductor_client.start_polling()
