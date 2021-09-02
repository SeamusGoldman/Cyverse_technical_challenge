import requests
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def run(loop):
    # reponse = requests.get("https://friends-quotes-api.herokuapp.com/quotes/random")
    # print(reponse.json())

    nc = NATS()

    await nc.connect("0.0.0.0:4222", loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
    # print("about to publish")

    sid = await nc.subscribe("foo", cb=message_handler)

    await nc.publish("foo", b'Hello')

    await nc.close()




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()