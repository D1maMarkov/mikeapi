import enum
from datetime import datetime

import pytz
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    case,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from src.entites.schedler import WEEKDAYS_LIST, WeekDays
from src.db.database import Model, Session
from src.entites.ticker import TICKER_TYPES
from src.entites.trader import TraderStatus, TraderWatch


class UrlEnum(str, enum.Enum):
    in_work = "Включен"
    unavailable = "Недоступен"
    error = "Сбой"
    failure = "Ошибка"


class VendorOrm(Model):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(String)
    auth_token = Column(String)
    logs = relationship("LogOrm", back_populates="app")
    traders = relationship("TraderOrm", back_populates="app")
    pings = relationship("PingOrm", back_populates="app")

    def __str__(self) -> str:
        return self.app_id


class APIURLSOrm(Model):
    __tablename__ = "main_url"

    id = Column(Integer, primary_key=True, index=True)
    main_url = Column(String)
    main_url_status = Column(Enum(UrlEnum, native_enum=False))
    reverse_url = Column(String)
    reverse_url_status = Column(Enum(UrlEnum, native_enum=False))


class UserOrm(Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    hash_password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __str__(self) -> str:
        return self.username


class TraderOrm(Model):
    __tablename__ = "traders"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    code = Column(String, unique=True)

    status = Column(String, nullable=True)
    subscribes = Column(Integer, nullable=True)
    subscribers = Column(Integer, nullable=True)

    portfolio = Column(String, nullable=True)
    trades = Column(Integer, nullable=True)
    profit = Column(Float, default=0)
    badges = Column(ARRAY(String), nullable=True)

    watch = Column(String, server_default="new")
    count = Column(Integer, default=0)
    logs = relationship("LogOrm", back_populates="user")
    app_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    app = relationship(VendorOrm, back_populates="traders")
    last_update = Column(TIMESTAMP(timezone=True), nullable=True)
    scanned = Column(Boolean, default=False)

    watches = TraderWatch
    statuses = TraderStatus

    def __str__(self) -> str:
        return self.username


class LogOrm(Model):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey("vendors.id"))
    app = relationship(VendorOrm, back_populates="logs")
    time = Column(TIMESTAMP(timezone=True), index=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone("Europe/Moscow")))
    user_id = Column(Integer, ForeignKey("traders.id", ondelete="CASCADE"))
    user = relationship(TraderOrm, back_populates="")
    main_server = Column(Boolean)
    price = Column(Float)
    currency = Column(String)
    operation = Column(String)

    ticker_id = Column(Integer, ForeignKey("tickers.id"))
    ticker = relationship("TickerOrm", back_populates="logs")

    @hybrid_property
    def delayed(self, db=Session()):
        query = select(SettingsOrm)
        settings = db.execute(query).scalars().first()

        if self.created_at and self.time:
            return (self.created_at - self.time).total_seconds() >= settings.log_delay
        return None

    @delayed.expression
    def delayed(cls, db=Session()):
        query = select(SettingsOrm)
        settings = db.execute(query).scalars().first()

        return func.extract("epoch", cls.created_at) - func.extract("epoch", cls.time) >= settings.log_delay


class LogActivityOrm(Model):
    __tablename__ = "logsactivity"

    id = Column(Integer, index=True, primary_key=True)
    date = Column(Date)

    hour00 = Column(Integer, default=0)
    hour01 = Column(Integer, default=0)
    hour02 = Column(Integer, default=0)
    hour03 = Column(Integer, default=0)
    hour04 = Column(Integer, default=0)
    hour05 = Column(Integer, default=0)
    hour06 = Column(Integer, default=0)
    hour07 = Column(Integer, default=0)
    hour08 = Column(Integer, default=0)
    hour09 = Column(Integer, default=0)
    hour10 = Column(Integer, default=0)
    hour11 = Column(Integer, default=0)
    hour12 = Column(Integer, default=0)
    hour13 = Column(Integer, default=0)
    hour14 = Column(Integer, default=0)
    hour15 = Column(Integer, default=0)
    hour16 = Column(Integer, default=0)
    hour17 = Column(Integer, default=0)
    hour18 = Column(Integer, default=0)
    hour19 = Column(Integer, default=0)
    hour20 = Column(Integer, default=0)
    hour21 = Column(Integer, default=0)
    hour22 = Column(Integer, default=0)
    hour23 = Column(Integer, default=0)

    last_day = Column(Integer, default=0)


class TickerOrm(Model):
    __tablename__ = "tickers"

    id = Column(Integer, index=True, primary_key=True)
    slug = Column(String, index=True)
    name = Column(String, nullable=True)
    lot = Column(Integer, default=0)
    type = Column(String, nullable=True)
    currency = Column(String)

    logs = relationship("LogOrm")

    trades = Column(Integer, default=0)
    traders = Column(Integer, default=0)
    last_month_traders = Column(Integer, default=0)
    last_month = Column(Integer, default=0)
    last_week_traders = Column(Integer, default=0)
    last_week = Column(Integer, default=0)
    last_day = Column(Integer, default=0)
    last_day_traders = Column(Integer, default=0)
    last_hour_traders = Column(Integer, default=0)
    last_hour = Column(Integer, default=0)
    last_trade_price = Column(Float, default=0)

    end = Column(Date, nullable=True)

    types = TICKER_TYPES

    @hybrid_property
    def rare(self, db=Session()) -> bool:
        settings = db.execute(select(SettingsOrm)).scalars().first()
        if not settings:
            return False

        return self.last_month < settings.rare_tickers_limit

    @rare.expression
    def rare(self, db=Session()):
        settings = db.execute(select(SettingsOrm)).scalars().first()
        if not settings:
            return False

        return case((self.last_month < settings.rare_tickers_limit, True), else_=False)

    @hybrid_property
    def archive(self) -> bool:
        if not self.end:
            return False

        return self.end < datetime.now().date()

    @archive.expression
    def archive(self):
        if not self.end:
            return False

        return case((self.end < func.current_date(), True), else_=False)

    def __str__(self) -> str:
        return self.slug


class SettingsOrm(Model):
    __tablename__ = "settings"

    id = Column(Integer, index=True, primary_key=True)
    log_delay = Column(Integer, default=0)
    rare_tickers_limit = Column(Integer, default=0)


class PingOrm(Model):
    __tablename__ = "pings"

    id = Column(Integer, index=True, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone("Europe/Moscow")))
    app_id = Column(Integer, ForeignKey("vendors.id"))
    app = relationship(VendorOrm, back_populates="pings")


class TradersBuffer(Model):
    __tablename__ = "buffer"

    id = Column(Integer, index=True, primary_key=True)
    usernames = Column(ARRAY(String))


class UnsuccessLog(Model):
    __tablename__ = "unsuccesslog"

    id = Column(Integer, index=True, primary_key=True)
    body = Column(String)
    
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone("Europe/Moscow")))


class SchedulerRuleOrm(Model):
    __tablename__ = 'schedulerrule'
    
    id = Column(Integer, index=True, primary_key=True)
    day_l = Column(String)
    day_r = Column(String)
    
    hour_l = Column(Integer)
    hour_r = Column(Integer)

    minute_l = Column(Integer)
    minute_r = Column(Integer)
    
    interval1 = Column(Integer)
    interval2 = Column(Integer)


class ContactOrm(Model):
    __tablename__ = "contacts"
    
    id = Column(Integer, index=True, primary_key=True)
    channel = Column(String)
    contact = Column(String)
    

class AlertsOrm(Model):
    __tablename__ = "alerts"
    
    id = Column(Integer, index=True, primary_key=True)
    first_log = Column(String)
    first_log_channel = Column(String)
    
    second_log = Column(String)
    second_log_channel = Column(String)
    
    trades_recovered = Column(String)
    trades_recovered_channel = Column(String)
    
    first_ping = Column(String)
    first_ping_channel = Column(String)
    
    second_ping = Column(String)
    second_ping_channel = Column(String)
    
    pings_recovered = Column(String)
    pings_recovered_channel = Column(String)
    
    pings_interval1 = Column(Integer)
    pings_interval2 = Column(Integer)
