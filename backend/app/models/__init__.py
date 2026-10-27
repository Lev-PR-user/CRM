from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .model import ДействияM, КаналУведомленийM, КатегорияУведомленияM, ЛокацииM, МетодыОплатыM
from .model import РолиM, СтатусОборудованияM, СтатусУведомленияM, СтатусыОплатыM
from .model import ТипКлиентаM, УслугиM, КлиентыM, ОборудованиеM, ПользователиM
from .model import ЖурналДействийM, ОператорыM, УведомленияM, ЗаказыM, ПлатежиM 
