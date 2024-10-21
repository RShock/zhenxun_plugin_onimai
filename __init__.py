import os
import json
import requests
from PIL import Image
from nonebot import logger, on_command, require
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    Message,
    MessageSegment, Bot, ActionFailed,
)
from nonebot.exception import FinishedException
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="《别当欧尼酱了！》漫画鉴赏",
    description="了解真寻背后的故事",
    usage="""
    看漫画：显示漫画目录
    继续看：从下一话继续看。
    看漫画 X：跳转到第X话，具体参考看漫画的目录
    漫画帮助：显示这段文字。
    """.strip(),
)
# 看漫画/继续看
# 漫画帮助
watch = on_command("看漫画", priority=5, block=True)
continue_watch = on_command("继续看", aliases={"下一话"}, priority=5, block=True)
comic_help = on_command("漫画帮助", priority=5, block=True)

path = os.path.dirname(__file__)
image_path = f"{path}/src/comic/"
name_list = ['别当欧尼酱了！01', '别当欧尼酱了！01.5', '别当欧尼酱了！02', '别当欧尼酱了！03', '别当欧尼酱了！04', '别当欧尼酱了！05', '别当欧尼酱了！05.5', '别当欧尼酱了！06',
             '别当欧尼酱了！06.5', '别当欧尼酱了！07', '别当欧尼酱了！08', '别当欧尼酱了！08.5', '别当欧尼酱了！09', '别当欧尼酱了！09.5', '别当欧尼酱了！10',
             '别当欧尼酱了！10.5', '别当欧尼酱了！10.7(第一卷附录)', '别当欧尼酱了！11', '别当欧尼酱了！12', '别当欧尼酱了！12.5', '别当欧尼酱了！13', '别当欧尼酱了！14',
             '别当欧尼酱了！15', '别当欧尼酱了！15.5', '别当欧尼酱了！16', '别当欧尼酱了！17', '别当欧尼酱了！18', '别当欧尼酱了！18.5', '别当欧尼酱了！19', '别当欧尼酱了！20',
             '别当欧尼酱了！20.5(第二卷附录)', '别当欧尼酱了！21', '别当欧尼酱了！21附录', '别当欧尼酱了！22', '别当欧尼酱了！23', '别当欧尼酱了！24', '别当欧尼酱了！24附录',
             '别当欧尼酱了！25', '别当欧尼酱了！25.5+附录', '别当欧尼酱了！26', '别当欧尼酱了！26.5', '别当欧尼酱了！27', '别当欧尼酱了！27.5', '别当欧尼酱了！28',
             '别当欧尼酱了！29', '别当欧尼酱了！30', '别当欧尼酱了！30.5（黑猫汉化）', '别当欧尼酱了 ！30.7(第3卷附录)', '别当欧尼酱了！31', '别当欧尼酱了！32',
             '别当欧尼酱了！32.5', '别当欧尼酱了！33', '别当欧尼酱了！33.5', '别当欧尼酱了！34', '别当 欧尼酱了！34.5', '别当欧尼酱了！35', '别当欧尼酱了！36',
             '别当欧尼酱了！36.5', '别当欧尼酱了！37', '别当欧尼酱了！37.5', '别当欧尼酱了！38', '别当欧尼酱了！38.5', '别当欧尼酱了！39', '别当欧尼酱了！40',
             '别当欧尼酱了！40.5', '别当欧尼酱了！40.7(第四卷附录)', '别当欧尼酱了！41', '别当欧尼酱了！41.3-41.7', '别当欧尼酱了！42', '别当欧尼酱了！42.5',
             '别当欧尼酱了！43', '别当欧尼酱了！43.5', '别当欧尼酱了！44', '别当欧尼酱了！45', '别当欧尼酱了！46', '别当欧尼酱了！46.5', '别当欧尼酱了！47',
             '别当欧尼酱了！47.5', '别当欧尼酱了！48', '别当欧尼酱了！48.5', '别当欧尼酱了！49', '别当欧尼酱了！50', '别 当欧尼酱了！50.5', '别当欧尼酱了！50.7(第5卷附录)',
             '别当欧尼酱了！51', '别当欧尼酱了！51.5', '别当欧尼酱了！52', '别当欧尼酱了！53', '别当欧尼酱了！53.5', '别当欧尼酱了！54', '别当欧尼酱了！54.5',
             '别当欧尼酱了！55', '别当欧尼酱了！56', '别当欧尼酱了！56.5', '别当欧尼酱了！57', '别当欧尼酱了！58', '别当欧尼酱了！58.5', '别当欧尼酱了！59', '别当欧尼酱了！60',
             '别当欧尼酱了！60.5(第6卷附录)', '别当欧尼酱了！61', '别当欧尼酱了！62', '别当欧尼酱了！62.5（来自贴吧）', '别当欧尼酱了！63', '别当欧尼酱了！63.5（来自贴吧）',
             '别当欧尼酱了！64', '别当欧尼酱了！65（黑猫汉化到此为止）', '别当欧尼酱了！66.5（来自贴吧）', '别当欧尼酱了！66（b站版本）', '别当欧尼酱了！67（b站版本）',
             '别当欧尼酱了！68（b站版本）', '别当欧尼酱了！69.5（来自贴吧）', '别当欧尼酱了！69（b站版本）', '别当欧尼酱了！70（b站版本）', '别当欧尼酱了！71（别酱了汉化组·应是第8卷内容）',
             '别当欧尼酱了！ex1(ex1试看版)', '别当欧尼酱了！ex1.5(ex1完整版)', '别当欧尼酱了！ex2(ex2试看版)', '别当欧尼酱了！ex2.5(ex2完整版)',
             '别当欧尼酱了！ex3(ex3试看版)', '别当欧尼酱了！ex3.5(ex3完整版)','别当欧尼酱了！72（b站版本）','别当欧尼酱了！73（b站版本）','别当欧尼酱了！74（b站版本）','别当欧尼酱了！75（b站版本）',
             '别当欧尼酱了！76（贴吧@这可一点也不酷o）','别当欧尼酱了！77（贴吧@这可一点也不酷o）','别当欧尼酱了！78（贴吧@这可一点也不酷o）','别当欧尼酱了！79（贴吧@这可一点也不酷o）','别当欧尼酱了！80（贴吧@这可一点也不酷o）',
             '别当欧尼酱了！81（贴吧@这可一点也不酷o）','别当欧尼酱了！82（贴吧@这可一点也不酷o）','别当欧尼酱了！83（贴吧@这可一点也不酷o）','别当欧尼酱了！84（贴吧@这可一点也不酷o）','别当欧尼酱了！85（贴吧@这可一点也不酷o）',
             '别当欧尼酱了！85.5（贴吧@这可一点也不酷o）','别当欧尼酱了！86（贴吧@这可一点也不酷o）','别当欧尼酱了！87（贴吧@这可一点也不酷o）','别当欧尼酱了！88（贴吧@这可一点也不酷o）','别当欧尼酱了！89（贴吧@这可一点也不酷o）',
             '别当欧尼酱了！90（贴吧@这可一点也不酷o）','别当欧尼酱了！91（贴吧@这可一点也不酷o）','别当欧尼酱了！92（贴吧@这可一点也不酷o）']


@watch.handle()
async def watch_handle(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    num = arg.extract_plain_text().strip()
    if num.isdigit() and float(num) < 10:
        num = "0" + num

    if os.path.exists(f'{path}/src'):
        if num == '':
            # 发送目录
            await send_index(bot, event)
        else:
            # 发送章节
            file = check_num(num)
            if not file:
                await watch.finish(f'您输入的章节"{num}"无法找到')
            await send_comic(bot, event, file)
            await save_json(event.user_id, file)
    elif os.path.exists(f'{path}/menu.json'):
        await watch.send('未检测到src数据，正在使用在线访问……')
        if num == '':
            await send_comic_from_web(bot, event, "menu")
        else:
            if chapter_name := next((name for name in name_list if name.startswith("别当欧尼酱了！" + num)), None):
                await send_comic_from_web(bot, event, chapter_name)
                await save_json(event.user_id, chapter_name)
            await watch.finish(f'您输入的章节"{num}"无法找到')
    else:
        await watch.finish('请拉取src进行本地浏览或拉取menu.json进行在线浏览')


@continue_watch.handle()
async def continue_watch_handle(bot: Bot, event: MessageEvent):
    if os.path.exists(f'{path}/src'):
        file_name = get_next(await load_json(event.user_id))
        if file_name == '已经是最后一话了':
            await continue_watch.finish("你已经看完了")
        await send_comic(bot, event, file_name)
        await save_json(event.user_id, file_name)
    else:
        await watch.send('未检测到src数据，正在使用在线访问……')
        now_read = await load_json(event.user_id)
        if next_read:= get_next(now_read) is None:
            await watch.send('你已经看完了')
        await send_comic_from_web(bot, event, next_read)
        await save_json(event.user_id, next_read)


async def send_comic_from_web(bot, event, name):
    f = open(f'{path}/menu.json', 'r', encoding='utf-8')
    content = f.read()
    menu = json.loads(content)

    if name == "menu":
        msg = ["别当欧尼酱了！目录：", "输入看漫画 X 就可以抵达对应章节了（X为目录左侧的章节数字，如`看漫画 1`）"]
        lis = list(menu['menu']['url'])
    else:
        for page in menu:
            if menu[page]['name'] == name:
                msg = ["你正在观看：别当欧尼酱了！" + menu[page]['name']]
                lis = list(menu[page]['url'])

    for url in lis:
        r = requests.get(url,
                         headers={
                             'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                             'Referer': 'https://postimg.cc/'}
                         )
        msg.append(MessageSegment.image(r.content))
    await send_group_msg(bot, event, '小真寻', msg)


@comic_help.handle()
async def help_handle():
    await comic_help.send("""看漫画：显示漫画目录
继续看/下一话：从下一话继续看
看漫画 X：跳转看对应话。X为数字，如1 1.5 或ex1 
漫画帮助：显示这段文字。""")


async def send_index(bot: Bot, event: MessageEvent):
    index_file_path = f"file:///{path}/src/目录/"
    index_path = f"{path}/src/目录/"
    await super_pic_send(bot, event, ["别当欧尼酱了！目录：", "输入看漫画 X 就可以抵达对应章节了（X为目录左侧的章节数字，如`看漫画 1`）"],
                         index_file_path, index_path)


async def send_comic(bot: Bot, event: MessageEvent, file):
    image_file_path = f"file:///{path}/src/comic/{file}/"
    file_path = image_path + file
    await super_pic_send(bot, event, ["你正在观看：" + file], image_file_path, file_path)


async def super_pic_send(bot, event, title, image_file_path, file_path):
    """
    特殊的图片组发送函数，按序发送指定文件夹下所有图片，如果发送失败则修改图片哈希值再试一次
    """
    # 普通发送
    msg = title.copy()
    files = os.listdir(file_path)
    files.sort(key=lambda x: int(x.split('.')[0]))

    msg.extend(MessageSegment.image(image_file_path+file_name) for file_name in files if file_name.endswith('.jpg'))
    try:
        await send_group_msg(bot, event, "小真寻", msg)
    except ActionFailed:
        await watch.send("检测到风控，正在绕过...")
        # 修改哈希值发送
        from PIL import Image
        from io import BytesIO
        msg = title.copy()
        for file_name in os.listdir(file_path):
            img = Image.open(file_path+'/'+file_name)
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=95)
            msg.append(MessageSegment.image(buffer))
        try:
            await send_group_msg(bot, event, "小真寻", msg)
        except ActionFailed:
            await watch.send("发送失败，请稍后重试")


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
        await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=messages)
    else:
        await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=messages)


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
        with open(filename, 'r') as f:
            content = f.read()
    else:
        content = "{}"
    return json.loads(content)


def get_next(file_name):
    index = name_list.index(file_name)
    if index == len(name_list) - 1:
        return None
    return name_list[(index + 1)]


def check_num(num):
    return next((file for file in os.listdir(image_path) if file.startswith("别当欧尼酱了！" + num)), None)
