from typing import Optional
import datetime
import decimal

from sqlalchemy import DECIMAL, Date, ForeignKeyConstraint, Index, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class ДействияM(Base):
    __tablename__ = 'действия'

    действие_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    действие: Mapped[str] = mapped_column(String(100), nullable=False)

    журнал_действий: Mapped[list['ЖурналДействийM']] = relationship('ЖурналДействийM', back_populates='действия')


class КаналУведомленийM(Base):
    __tablename__ = 'канал_уведомлений'

    канал_уведомления_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    канал: Mapped[str] = mapped_column(String(100), nullable=False)

    уведомления: Mapped[list['УведомленияM']] = relationship('УведомленияM', back_populates='канал_уведомлений')


class КатегорияУведомленияM(Base):
    __tablename__ = 'категория_уведомления'

    категория_уведомления_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    категория: Mapped[str] = mapped_column(String(100), nullable=False)

    уведомления: Mapped[list['УведомленияM']] = relationship('УведомленияM', back_populates='категория_уведомления_')


class ЛокацииM(Base):
    __tablename__ = 'локации'

    локация_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    название: Mapped[str] = mapped_column(String(255), nullable=False)
    адрес: Mapped[str] = mapped_column(String(255), nullable=False)
    часы_работы: Mapped[Optional[dict]] = mapped_column(JSON)

    оборудование: Mapped[list['ОборудованиеM']] = relationship('ОборудованиеM', back_populates='локации')
    заказы: Mapped[list['ЗаказыM']] = relationship('ЗаказыM', back_populates='локации_')


class МетодыОплатыM(Base):
    __tablename__ = 'методы_оплаты'

    метод_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    метод: Mapped[Optional[str]] = mapped_column(String(100))

    платежи: Mapped[list['ПлатежиM']] = relationship('ПлатежиM', back_populates='методы_оплаты')


class РолиM(Base):
    __tablename__ = 'роли'

    роль_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    название_роли: Mapped[Optional[str]] = mapped_column(String(100))
    описание: Mapped[Optional[str]] = mapped_column(Text)

    пользователи: Mapped[list['ПользователиM']] = relationship('ПользователиM', back_populates='роли')


class СтатусОборудованияM(Base):
    __tablename__ = 'статус_оборудования'

    статус_оборудования_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    статус: Mapped[str] = mapped_column(String(100), nullable=False)

    оборудование: Mapped[list['ОборудованиеM']] = relationship('ОборудованиеM', back_populates='статус_оборудования')


class СтатусУведомленияM(Base):
    __tablename__ = 'статус_уведомления'

    статус_уведомления_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    статус: Mapped[str] = mapped_column(String(100), nullable=False)

    уведомления: Mapped[list['УведомленияM']] = relationship('УведомленияM', back_populates='статус_уведомления')


class СтатусыОплатыM(Base):
    __tablename__ = 'статусы_оплаты'

    статусы_оплаты_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    название: Mapped[Optional[str]] = mapped_column(String(100))

    платежи: Mapped[list['ПлатежиM']] = relationship('ПлатежиM', back_populates='статусы_оплаты')


class ТипКлиентаM(Base):
    __tablename__ = 'тип_клиента'

    тип_клиента_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    тип: Mapped[str] = mapped_column(String(100), nullable=False)

    клиенты: Mapped[list['КлиентыM']] = relationship('КлиентыM', back_populates='тип_клиента')


class УслугиM(Base):
    __tablename__ = 'услуги'

    услуга_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    услуга: Mapped[Optional[str]] = mapped_column(String(100))

    заказы: Mapped[list['ЗаказыM']] = relationship('ЗаказыM', back_populates='услуги_')


class КлиентыM(Base):
    __tablename__ = 'клиенты'
    __table_args__ = (
        ForeignKeyConstraint(['тип'], ['тип_клиента.тип_клиента_id'], name='тип_fk'),
        Index('тип_fk', 'тип')
    )

    клиент_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    имя: Mapped[str] = mapped_column(String(255), nullable=False)
    тип: Mapped[int] = mapped_column(Integer, nullable=False)
    заметки: Mapped[str] = mapped_column(String(255), nullable=True)
    контакты: Mapped[Optional[dict]] = mapped_column(JSON)

    тип_клиента: Mapped['ТипКлиентаM'] = relationship('ТипКлиентаM', back_populates='клиенты')
    заказы: Mapped[list['ЗаказыM']] = relationship('ЗаказыM', back_populates='клиенты')


class ОборудованиеM(Base):
    __tablename__ = 'оборудование'
    __table_args__ = (
        ForeignKeyConstraint(['расположение'], ['локации.локация_id'], name='локация_оборудования_fk'),
        ForeignKeyConstraint(['статус'], ['статус_оборудования.статус_оборудования_id'], name='статус_оборудования_fk'),
        Index('локация_оборудования_fk', 'расположение'),
        Index('статус_оборудования_fk', 'статус')
    )

    оборудование_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    модель: Mapped[str] = mapped_column(String(100), nullable=False)
    серия: Mapped[str] = mapped_column(String(100), nullable=False)
    статус: Mapped[int] = mapped_column(Integer, nullable=False)
    расположение: Mapped[Optional[int]] = mapped_column(Integer)

    локации: Mapped[Optional['ЛокацииM']] = relationship('ЛокацииM', back_populates='оборудование')
    статус_оборудования: Mapped['СтатусОборудованияM'] = relationship('СтатусОборудованияM', back_populates='оборудование')
    заказы: Mapped[list['ЗаказыM']] = relationship('ЗаказыM', back_populates='оборудование_')


class ПользователиM(Base):
    __tablename__ = 'пользователи'
    __table_args__ = (
        ForeignKeyConstraint(['роль'], ['роли.роль_id'], name='роль_fk'),
        Index('роль_fk', 'роль')
    )

    пользователь_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    фамилия: Mapped[str] = mapped_column(String(100), nullable=False)
    имя: Mapped[str] = mapped_column(String(100), nullable=False)
    пароль: Mapped[str] = mapped_column(String(200), nullable=False)
    отчество: Mapped[Optional[str]] = mapped_column(String(100))
    название_организации: Mapped[Optional[str]] = mapped_column(String(100))
    почта: Mapped[Optional[str]] = mapped_column(String(255))
    номер: Mapped[Optional[str]] = mapped_column(String(20))
    роль: Mapped[Optional[int]] = mapped_column(Integer)

    роли: Mapped[Optional['РолиM']] = relationship('РолиM', back_populates='пользователи')
    журнал_действий: Mapped[list['ЖурналДействийM']] = relationship('ЖурналДействийM', back_populates='пользователи')
    операторы: Mapped[list['ОператорыM']] = relationship('ОператорыM', back_populates='пользователи')
    уведомления: Mapped[list['УведомленияM']] = relationship('УведомленияM', back_populates='пользователи')


class ЖурналДействийM(Base):
    __tablename__ = 'журнал_действий'
    __table_args__ = (
        ForeignKeyConstraint(['действие'], ['действия.действие_id'], name='действие_fk'),
        ForeignKeyConstraint(['пользователь'], ['пользователи.пользователь_id'], name='пользователь_действие_fk'),
        Index('действие_fk', 'действие'),
        Index('пользователь_действие_fk', 'пользователь')
    )

    действие_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    пользователь: Mapped[int] = mapped_column(Integer, nullable=False)
    действие: Mapped[int] = mapped_column(Integer, nullable=False)
    что_изменилось: Mapped[str] = mapped_column(Text, nullable=False)
    дата_изменения: Mapped[Optional[datetime.date]] = mapped_column(Date)

    действия: Mapped['ДействияM'] = relationship('ДействияM', back_populates='журнал_действий')
    пользователи: Mapped['ПользователиM'] = relationship('ПользователиM', back_populates='журнал_действий')


class ОператорыM(Base):
    __tablename__ = 'операторы'
    __table_args__ = (
        ForeignKeyConstraint(['пользователь'], ['пользователи.пользователь_id'], name='пользователь_оператор_fk'),
        Index('пользователь_оператор_fk', 'пользователь')
    )

    оператор_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    пользователь: Mapped[int] = mapped_column(Integer, nullable=False)
    локации: Mapped[Optional[dict]] = mapped_column(JSON)
    график: Mapped[Optional[dict]] = mapped_column(JSON)

    пользователи: Mapped['ПользователиM'] = relationship('ПользователиM', back_populates='операторы')
    заказы: Mapped[list['ЗаказыM']] = relationship('ЗаказыM', back_populates='операторы')


class УведомленияM(Base):
    __tablename__ = 'уведомления'
    __table_args__ = (
        ForeignKeyConstraint(['канал_уведомления'], ['канал_уведомлений.канал_уведомления_id'], name='канал_fk'),
        ForeignKeyConstraint(['категория_уведомления'], ['категория_уведомления.категория_уведомления_id'], name='категория_уведомления_fk'),
        ForeignKeyConstraint(['пользователь'], ['пользователи.пользователь_id'], name='пользователь_уведомления_fk'),
        ForeignKeyConstraint(['статус'], ['статус_уведомления.статус_уведомления_id'], name='статус_уведомлений_fk'),
        Index('канал_fk', 'канал_уведомления'),
        Index('категория_уведомления_fk', 'категория_уведомления'),
        Index('пользователь_уведомления_fk', 'пользователь'),
        Index('статус_уведомлений_fk', 'статус')
    )

    уведомление_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    пользователь: Mapped[int] = mapped_column(Integer, nullable=False)
    категория_уведомления: Mapped[int] = mapped_column(Integer, nullable=False)
    канал_уведомления: Mapped[int] = mapped_column(Integer, nullable=False)
    статус: Mapped[int] = mapped_column(Integer, nullable=False)
    дата_отправки: Mapped[Optional[datetime.date]] = mapped_column(Date)

    канал_уведомлений: Mapped['КаналУведомленийM'] = relationship('КаналУведомленийM', back_populates='уведомления')
    категория_уведомления_: Mapped['КатегорияУведомленияM'] = relationship('КатегорияУведомленияM', back_populates='уведомления')
    пользователи: Mapped['ПользователиM'] = relationship('ПользователиM', back_populates='уведомления')
    статус_уведомления: Mapped['СтатусУведомленияM'] = relationship('СтатусУведомленияM', back_populates='уведомления')


class ЗаказыM(Base):
    __tablename__ = 'заказы'
    __table_args__ = (
        ForeignKeyConstraint(['клиент'], ['клиенты.клиент_id'], name='клиент_fk'),
        ForeignKeyConstraint(['локации'], ['локации.локация_id'], name='услуга_заказа_fk'),
        ForeignKeyConstraint(['оборудование'], ['оборудование.оборудование_id'], name='оборудование_fk'),
        ForeignKeyConstraint(['оператор'], ['операторы.оператор_id'], name='оператор_заказа_fk'),
        ForeignKeyConstraint(['услуги'], ['услуги.услуга_id'], name='услуга_fk'),
        Index('клиент_fk', 'клиент'),
        Index('оборудование_fk', 'оборудование'),
        Index('оператор_заказа_fk', 'оператор'),
        Index('услуга_fk', 'услуги'),
        Index('услуга_заказа_fk', 'локации')
    )

    заказ_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    клиент: Mapped[int] = mapped_column(Integer, nullable=False)
    услуги: Mapped[int] = mapped_column(Integer, nullable=False)
    локации: Mapped[int] = mapped_column(Integer, nullable=False)
    оператор: Mapped[int] = mapped_column(Integer, nullable=False)
    оборудование: Mapped[int] = mapped_column(Integer, nullable=False)
    дата_начала: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    дата_конца: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    клиенты: Mapped['КлиентыM'] = relationship('КлиентыM', back_populates='заказы')
    локации_: Mapped['ЛокацииM'] = relationship('ЛокацииM', back_populates='заказы')
    оборудование_: Mapped['ОборудованиеM'] = relationship('ОборудованиеM', back_populates='заказы')
    операторы: Mapped['ОператорыM'] = relationship('ОператорыM', back_populates='заказы')
    услуги_: Mapped['УслугиM'] = relationship('УслугиM', back_populates='заказы')
    платежи: Mapped[list['ПлатежиM']] = relationship('ПлатежиM', back_populates='заказы_')


class ПлатежиM(Base):
    __tablename__ = 'платежи'
    __table_args__ = (
        ForeignKeyConstraint(['заказы'], ['заказы.заказ_id'], name='заказ_fk'),
        ForeignKeyConstraint(['метод'], ['методы_оплаты.метод_id'], name='метод_fk'),
        ForeignKeyConstraint(['статус'], ['статусы_оплаты.статусы_оплаты_id'], name='статус_платежа_fk'),
        Index('заказ_fk', 'заказы'),
        Index('метод_fk', 'метод'),
        Index('статус_платежа_fk', 'статус')
    )

    платежи_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    заказы: Mapped[int] = mapped_column(Integer, nullable=False)
    цена: Mapped[decimal.Decimal] = mapped_column(DECIMAL(15, 2), nullable=False)
    метод: Mapped[int] = mapped_column(Integer, nullable=False)
    статус: Mapped[int] = mapped_column(Integer, nullable=False)
    дата: Mapped[Optional[datetime.date]] = mapped_column(Date)

    заказы_: Mapped['ЗаказыM'] = relationship('ЗаказыM', back_populates='платежи')
    методы_оплаты: Mapped['МетодыОплатыM'] = relationship('МетодыОплатыM', back_populates='платежи')
    статусы_оплаты: Mapped['СтатусыОплатыM'] = relationship('СтатусыОплатыM', back_populates='платежи')