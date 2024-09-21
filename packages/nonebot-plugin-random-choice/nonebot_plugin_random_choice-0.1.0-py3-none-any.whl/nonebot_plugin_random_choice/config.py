from pydantic import BaseModel
from typing import Literal
from nonebot import get_driver, get_plugin_config

class ScopedConfig(BaseModel):
    response_format:str = "唔...我觉得选“{response}”更好！"
    reply:bool = True
    at_sender:bool = False
    # analytical_method:Literal['alc','re'] = 'alc'
    
class Config(BaseModel):
    random_choice: ScopedConfig = ScopedConfig()
    
global_config = get_driver().config
plugin_config = get_plugin_config(Config).random_choice