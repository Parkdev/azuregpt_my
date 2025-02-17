# func host start --port 7073

import azure.functions as func

from util.pubsub import pubsub_client
from util.db import db

import json

app = func.FunctionApp()


@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="process-response-queue",
    connection="SERVICEBUS_CONNECTION_URL",
)
async def process_response_function(msg: func.ServiceBusMessage):

    response = json.loads(msg.get_body().decode("utf-8"))

    # db 저장
    result = await db.messages.insert_one(response)
    response["_id"] = str(response["_id"])

    # 펍섭 메세지 전송
    await pubsub_client.send_to_group(group=response["channel_id"], message=response)
