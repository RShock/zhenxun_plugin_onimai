import os
import json
from nonebot import logger
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    Message,
    MessageSegment, Bot,
)
from nonebot.exception import FinishedException
from nonebot.params import CommandArg

require("nonebot_plugin_apscheduler")

__zx_plugin_name__ = "《别当欧尼酱了！》漫画鉴赏"
__plugin_usage__ = """
usage：
    看漫画：显示漫画目录
    继续看：从下一话继续看。
    看漫画 X：跳转到第X话，具体参考看漫画的目录
    漫画帮助：显示这段文字。
""".strip()
__plugin_des__ = "了解真寻背后的故事"
__plugin_type__ = ("来点好康的",)
__plugin_cmd__ = ["看漫画", "继续看", "漫画帮助"]
__plugin_version__ = 1.0
__plugin_author__ = "XiaoR"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "cmd": ["看漫画", "继续看", "漫画帮助"],
}
__plugin_configs__ = {
}

# 看漫画/继续看
# 漫画帮助
watch = on_command("看漫画", priority=5, block=True)
continue_watch = on_command("继续看", aliases={"下一话"}, priority=5, block=True)
comic_help = on_command("漫画帮助", priority=5, block=True)

path = os.path.dirname(__file__)
image_path = f"{path}/src/comic/"


@watch.handle()
async def watch_handle(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    num = arg.extract_plain_text().strip()
    if num == '':
        # 发送图片
        await send_index(bot,event)
    else:
        file = check_num(num)
        if not file:
            await watch.finish(f'您输入的章节"{num}"无法找到')
        await send_comic(bot,event, file)
        await save_json(event.user_id, file)


# 风控！
@continue_watch.handle()
async def continue_watch_handle(bot: Bot, event: MessageEvent):
    file_name = get_next(await load_json(event.user_id))
    await send_comic(bot,event, file_name)
    await save_json(event.user_id, file_name)
    pass


@comic_help.handle()
async def help_handle():
    await comic_help.send("""看漫画：显示漫画目录
继续看/下一话：从下一话继续看
看漫画 X：跳转看对应话。X为数字，如1 1.5 或ex1 
漫画帮助：显示这段文字。""")


async def send_index(bot: Bot,event: MessageEvent):
    index_file_path = f"file:///{path}/src/目录/"
    index_path = f"{path}/src/目录/"
    file = os.listdir(index_path)
    file.sort(key=lambda x: int(x.split('.')[0]))

    msg = ["别当欧尼酱了！目录：", "输入看漫画 X 就可以抵达对应章节了（X为目录左侧的章节数字，如`看漫画 1`）"]
    for file_name in file:
        if file_name.endswith('.jpg'):
            file_path = index_file_path + file_name
            msg.append(MessageSegment.image(file_path))
    await super_send(bot,event, msg)


async def send_comic(bot: Bot,event: MessageEvent, file):
    image_file_path = f"file:///{path}/src/comic/{file}/"

    files = os.listdir(image_path + file)
    files.sort(key=lambda x: int(x.split('.')[0]))

    msg = ["你正在观看：" + file]
    for file2 in files:
        if file2.endswith('.jpg'):
            file_path = image_file_path + file2
            msg.append(MessageSegment.image(file_path))
    await super_send(bot,event, msg)


async def send_group_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        msgs: list[str],
):
    """
    发送合并消息(发送人名称相同)
    @param bot: 机器人的引用
    @param event: 用来获取群id
    @param name: 发消息的人的名字
    @param msgs: 要发的消息(list[str])
    @return:
    """
    messages = [MessageSegment.node_custom(bot.self_id, name, m) for m in msgs]
    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_private_forward_msg", user_id	=event.user_id, messages=messages
        )


async def super_send(bot,event, msg):
    try:
        await send_group_msg(bot, event, "小真寻", msg)
    except Exception as e:
        if not isinstance(e, FinishedException):
            logger.warning("检查到风控！")
            await bot.send("发送失败，过段时间再来吧")


# 保存用户看到哪一集了
filename = path + '/观看记录（勿删）.json'


async def save_json(user_id, num):
    js = await read_json(user_id)

    js[user_id] = num
    json_dump = json.dumps(js)
    f2 = open(filename, 'w')
    f2.write(json_dump)
    f2.close()


async def load_json(user_id):
    js = await read_json(user_id)
    return js.get(str(user_id), "0")


async def read_json(user_id):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        content = f.read()
    else:
        content = "{}"
    return json.loads(content)


def get_next(file_name):
    flg = False
    files = os.listdir(image_path)
    files.sort()
    for file in files:
        if flg:
            return file
        if file.startswith(file_name):
            flg = True
    return "别当欧尼酱了！01"


def check_num(num):
    if float(num) < 10:
        num = "0" + num
    files = os.listdir(image_path)
    files.sort()
    for file in files:
        if file.startswith("别当欧尼酱了！" + num):
            return file
    return None
    # return os.path.exists(image_path + filename)
