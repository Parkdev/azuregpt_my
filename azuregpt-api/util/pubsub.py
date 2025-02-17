from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential

import os

# 펍섭 클라이언트 생성
pubsub_client = WebPubSubServiceClient(
    endpoint=os.environ["PUBSUB_CONNECTION_URL"],
    hub=os.environ["PUBSUB_HUB"],
    credential=AzureKeyCredential(os.environ["PUBSUB_KEY"]),
)
