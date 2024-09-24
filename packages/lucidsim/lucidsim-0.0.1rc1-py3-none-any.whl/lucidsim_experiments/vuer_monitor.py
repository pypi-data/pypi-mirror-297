import asyncio

from dotenv import load_dotenv
from vuer import Vuer, VuerSession
from vuer.schemas import ImageBackground
from zaku import TaskQ

load_dotenv()

app = Vuer(port=9002, host="localhost", verbose=True)
queue = TaskQ(name=f"vuer:{TaskQ.ZAKU_USER}:monitor-queue", verbose=True)

# clear queue for better performance.
# queue.clear_queue()

rgb = None


async def task_reader():
    global rgb

    while True:
        print(".", end="")
        with queue.pop() as item:
            if item is not None:
                print("found", *item.keys(), end="")
                rgb = item.get("rgb", None)
                rgb = rgb or item.get("render", None)

        await asyncio.sleep(0.01)


@app.spawn(start=True)
async def main(sess: VuerSession):
    global rgb

    task = app.spawn_task(task_reader())

    try:
        while True:
            print("*", end="")
            if rgb is not None:
                print("new image!")
                sess.upsert @ ImageBackground(rgb, key="image", format="jpeg")
                rgb = None

            await asyncio.sleep(0.05)

    except Exception as e:
        # clean up after.
        task.cancel()
        raise e
