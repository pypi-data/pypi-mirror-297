import random

from typing import Any, Annotated

from nonebot import require
from nonebot.rule import to_me
from nonebot.params import RegexStr
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, on_regex
from nonebot.adapters import Event

require("nonebot_plugin_saa")
import nonebot_plugin_saa as saa 

from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="Bot帮我选",
    description="不知道怎么选？让bot来帮你选一个？",
    usage="艾特bot并发送：选xx还是ss，或者：选xx还是ss还是mm（可以跟无数个还是），bot就会帮你从中选择呢！",
    homepage="https://github.com/ChenXu233/nonebot_plugin_random_choice",
    type="application",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_saa"
    ),
    config=Config,
)

choice = on_regex(r"选(.*?)(还是.*?)+$", rule=to_me(),priority=1, block=True)

@choice.handle()
async def make_choice(match: Annotated[str, RegexStr()]):
    choices = match[1:].split("还是")
    for i in choices:
        if not i:
            choices.remove(i)
    choice = random.choice(choices)
    await saa.Text(plugin_config.response_format.format(response=choice)).finish(reply=plugin_config.reply,at_sender=plugin_config.at_sender)