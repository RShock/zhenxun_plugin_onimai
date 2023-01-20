import os
import json
import requests
from nonebot import logger
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    Message,
    MessageSegment, Bot,
)
from nonebot.exception import FinishedException
from configs.path_config import TEMP_PATH
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
#test = on_command('在线漫画',priority=5,block=True)
watch = on_command("看漫画", priority=5, block=True)
continue_watch = on_command("继续看", aliases={"下一话"}, priority=5, block=True)
comic_help = on_command("漫画帮助", priority=5, block=True)

path = os.path.dirname(__file__)
image_path = f"{path}/src/comic/"
name_list = ['别当欧尼酱了！01', '别当欧尼酱了！01.5', '别当欧尼酱了！02', '别当欧尼酱了！03', '别当欧尼酱了！04', '别当欧尼酱了！05', '别当欧尼酱了！05.5', '别当欧尼酱了！06', '别当欧尼酱了！06.5', '别当欧尼酱了！07', '别当欧尼酱了！08', '别当欧尼酱了！08.5', '别当欧尼酱了！09', '别当欧尼酱了！09.5', '别当欧尼酱了！10', '别当欧尼酱了！10.5', '别当欧尼酱了！10.7(第一卷附录)', '别当欧尼酱了！11', '别当欧尼酱了！12', '别当欧尼酱了！12.5', '别当欧尼酱了！13', '别当欧尼酱了！14', '别当欧尼酱了！15', '别当欧尼酱了！15.5', '别当欧尼酱了！16', '别当欧尼酱了！17', '别当欧尼酱了！18', '别当欧尼酱了！18.5', '别当欧尼酱了！19', '别当欧尼酱了！20', '别当欧尼酱了！20.5(第二卷附录)', '别当欧尼酱了！21', '别当欧尼酱了！21附录', '别当欧尼酱了！22', '别当欧尼酱了！23', '别当欧尼酱了！24', '别当欧尼酱了！24附录', '别当欧尼酱了！25', '别当欧尼酱了！25.5+附录', '别当欧尼酱了！26', '别当欧尼酱了！26.5', '别当欧尼酱了！27', '别当欧尼酱了！27.5', '别当欧尼酱了！28', '别当欧尼酱了！29', '别当欧尼酱了！30', '别当欧尼酱了！30.5（黑猫汉化）', '别当欧尼酱了 ！30.7(第3卷附录)', '别当欧尼酱了！31', '别当欧尼酱了！32', '别当欧尼酱了！32.5', '别当欧尼酱了！33', '别当欧尼酱了！33.5', '别当欧尼酱了！34', '别当 欧尼酱了！34.5', '别当欧尼酱了！35', '别当欧尼酱了！36', '别当欧尼酱了！36.5', '别当欧尼酱了！37', '别当欧尼酱了！37.5', '别当欧尼酱了！38', '别当欧尼酱了！38.5', '别当欧尼酱了！39', '别当欧尼酱了！40', '别当欧尼酱了！40.5', '别当欧尼酱了！40.7(第四卷附录)', '别当欧尼酱了！41', '别当欧尼酱了！41.3-41.7', '别当欧尼酱了！42', '别当欧尼酱了！42.5', '别当欧尼酱了！43', '别当欧尼酱了！43.5', '别当欧尼酱了！44', '别当欧尼酱了！45', '别当欧尼酱了！46', '别当欧尼酱了！46.5', '别当欧尼酱了！47', '别当欧尼酱了！47.5', '别当欧尼酱了！48', '别当欧尼酱了！48.5', '别当欧尼酱了！49', '别当欧尼酱了！50', '别 当欧尼酱了！50.5', '别当欧尼酱了！50.7(第5卷附录)', '别当欧尼酱了！51', '别当欧尼酱了！51.5', '别当欧尼酱了！52', '别当欧尼酱了！53', '别当欧尼酱了！53.5', '别当欧尼酱了！54', '别当欧尼酱了！54.5', '别当欧尼酱了！55', '别当欧尼酱了！56', '别当欧尼酱了！56.5', '别当欧尼酱了！57', '别当欧尼酱了！58', '别当欧尼酱了！58.5', '别当欧尼酱了！59', '别当欧尼酱了！60', '别当欧尼酱了！60.5(第6卷附录)', '别当欧尼酱了！61', '别当欧尼酱了！62', '别当欧尼酱了！62.5（来自贴吧）', '别当欧尼酱了！63', '别当欧尼酱了！63.5（来自贴吧）', '别当欧尼酱了！64', '别当欧尼酱了！65（黑猫汉化到此为止）', '别当欧尼酱了！66.5（来自贴吧）', '别当欧尼酱了！66（b站版本）', '别当欧尼酱了！67（b站版本）', '别当欧尼酱了！68（b站版本）', '别当欧尼酱了！69.5（来自贴吧）', '别当 欧尼酱了！69（b站版本）', '别当欧尼酱了！70（b站版本）', '别当欧尼酱了！71（别酱了汉化组·应是第8卷内容）', '别当欧尼酱了！ex1(ex1试看版)', '别当欧尼酱了！ex1.5(ex1完整版)', '别当欧尼酱了！ex2(ex2试看版)', '别当欧尼酱了！ex2.5(ex2完整版)', '别当欧尼酱了！ex3(ex3试看版)', '别当欧尼酱了！ex3.5(ex3完整版)']

# @test.handle()
# async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
#     f = open(f'{path}/meun.json', 'r')
#     f1 = open(f'{path}/meun1.json', 'r',encoding='utf-8')
#     content = f.read()
#     content1 = f1.read()
#     meun = json.loads(content)
#     name = json.loads(content1)
#     update = {}
#     for page in meun.keys():
#         update[page] = {"url":meun[page],"name":name[page]['name']}
#     f = open(f'{path}/meun2.json', 'w')
#     f.write(json.dumps(update))
#     f.close
#     await test.finish('已完成')



@watch.handle()
async def watch_handle(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    num = arg.extract_plain_text().strip()
    if os.path.exists(f'{path}/src'):
        if num == '':
            # 发送图片
            await send_index(bot,event)
        else:
            file = check_num(num)
            if not file:
                await watch.finish(f'您输入的章节"{num}"无法找到')
            await send_comic(bot,event, file)
            await save_json(event.user_id, file)
    elif os.path.exists(f'{path}/meun.json'):
        await watch.send('未检测到src数据，正在使用在线访问……')
        f = open(f'{path}/meun.json', 'r',encoding='utf-8')
        content = f.read()
        meun = json.loads(content)
        if num == '':
            # 发送图片
            msg = ["别当欧尼酱了！目录：", "输入看漫画 X 就可以抵达对应章节了（X为目录左侧的章节数字，如`看漫画 1`）"]
            for url in list(meun['meun']['url']):
                    r = requests.get(url,
                    headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                    'Referer':'https://postimg.cc/'}
                    )
                    msg.append(MessageSegment.image(r.content))
            await send_group_msg(bot,event, '小真寻',msg)
            pass
        else:
            if not num in meun.keys():
                await watch.finish(f'您输入的章节"{num}"无法找到')
            msg = ["你正在观看：别当欧尼酱了！" + meun[num]['name']]
            for url in list(meun[num]['url']):
                    r = requests.get(url,
                    headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                    'Referer':'https://postimg.cc/'}
                    )
                    msg.append(MessageSegment.image(r.content))
            await send_group_msg(bot,event, '小真寻',msg)
            await save_json(event.user_id, meun[num]['name'])
            pass
    else:
        await watch.finish('请拉取src进行本地浏览或拉取meun.json进行在线浏览')


# 风控！
@continue_watch.handle()
async def continue_watch_handle(bot: Bot, event: MessageEvent):
    if os.path.exists(f'{path}/src'):
        file_name = get_next(await load_json(event.user_id))
        await send_comic(bot,event, file_name)
        await save_json(event.user_id, file_name)
        pass
    else:
        await watch.send('未检测到src数据，正在使用在线访问……')
        f = open(f'{path}/meun.json', 'r',encoding='utf-8')
        content = f.read()
        meun = json.loads(content)
        now_index = await load_json(event.user_id)
        next_index = name_list.index(now_index)+1
        for page in meun:
            if meun[page]['name'] == name_list[next_index]:
                msg = ["你正在观看：别当欧尼酱了！" + meun[page]['name']]
                for url in list(meun[page]['url']):
                        r = requests.get(url,
                        headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                        'Referer':'https://postimg.cc/'}
                        )
                        msg.append(MessageSegment.image(r.content))
                await send_group_msg(bot,event, '小真寻',msg)
                await save_json(event.user_id, meun[page]['name'])




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
    js = await read_json()

    js[user_id] = num
    json_dump = json.dumps(js)
    f2 = open(filename, 'w')
    f2.write(json_dump)
    f2.close()


async def load_json(user_id):
    js = await read_json()
    return js.get(str(user_id), "0")


async def read_json():
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

