# func host start --port 7072

from openai import OpenAI

from util.servicebus import servicebus_client

import azure.functions as func
import logging
import json

app = func.FunctionApp()
client = OpenAI()


@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="process-request-queue",
    connection="SERVICEBUS_CONNECTION_URL",
)
async def process_request(msg: func.ServiceBusMessage):
    message = json.loads(msg.get_body().decode("utf-8"))

    # 요청 보내기
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "질문에 대해서 한국어로 대답해"},
            {"role": "user", "content": message["content"]},
        ],
    )

    # 요청 답변 확인
    logging.info(completion.choices[0].message.content)

    # 전송 포멧
    answer_data = {
        "channel_id": message["channel_id"],
        "content": completion.choices[0].message.content,
        "type": "answer",
    }

    await servicebus_client.send_message("process-response-queue", answer_data)

    # 응답 전송
