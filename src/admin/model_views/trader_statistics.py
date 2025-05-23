from src.entites.trader import StatisticPeriodEnum, StatisticPeriod
from src.db.models.models import TraderOrm, TraderStatisticOrm
from markupsafe import Markup
from fastapi.requests import Request

from src.admin.model_views.base import BaseModelView, format_sum, render_degrees
from sqlalchemy import (
    and_,
    Select,
    desc,
    asc,
)
from starlette.routing import URLPath
from datetime import datetime, timedelta


class TraderStatisticsAdmin(BaseModelView, model=TraderStatisticOrm):
    column_list = [
        TraderStatisticOrm.end_date,
        TraderStatisticOrm.trader,
    
        TraderStatisticOrm.cash_balance,

        TraderStatisticOrm.stock_balance,
        TraderStatisticOrm.active_lots,

        TraderStatisticOrm.deals,
        
        TraderStatisticOrm.trade_volume,
        TraderStatisticOrm.income,

        TraderStatisticOrm.yield_,
        TraderStatisticOrm.gain,
        TraderStatisticOrm.tickers
    ]
    
    column_sortable_list = [
        TraderStatisticOrm.end_date,
        TraderStatisticOrm.trader,
    
        TraderStatisticOrm.cash_balance,

        TraderStatisticOrm.stock_balance,
        TraderStatisticOrm.active_lots,

        TraderStatisticOrm.deals,
        
        TraderStatisticOrm.trade_volume,
        TraderStatisticOrm.income,

        TraderStatisticOrm.yield_,
        TraderStatisticOrm.gain,
        TraderStatisticOrm.tickers
    ]

    column_formatters = {
        TraderStatisticOrm.end_date: lambda a, _: a.date_value,
        TraderStatisticOrm.trader: lambda a, _: Markup(
            f"""<a href="{URLPath(f'''/admin/trader-statistic-orm/list?trader_id={a.trader_id}''')}">{a.trader}</a>"""
        ),
        TraderStatisticOrm.gain: lambda a, _: Markup(f"{round(a.gain, 2)} % {render_degrees(a.gain_degrees)}"),
        TraderStatisticOrm.trade_volume: lambda a, _: Markup(f"{format_sum(a.trade_volume)} {render_degrees(a.trade_volume_degrees)}"),
        TraderStatisticOrm.stock_balance: lambda a, _: Markup(f"{format_sum(a.stock_balance)} {render_degrees(a.stock_balance_degrees)}"),
        TraderStatisticOrm.cash_balance: lambda a, _: Markup(f"{format_sum(a.cash_balance)} {render_degrees(a.cash_balance_degrees)}"),
        TraderStatisticOrm.income: lambda a, _: Markup(f"{format_sum(a.income)} {render_degrees(a.income_degrees)}"),
        TraderStatisticOrm.yield_: lambda a, _: f"{round(a.yield_, 2)} %",
        TraderStatisticOrm.deals: lambda a, _: Markup(
            f"""<a href="{URLPath(f'''/admin/deal-orm/list?trader_id={a.trader_id}&start_date={a.start_date.strftime("%d.%m.%Y")}&end_date={a.end_date.strftime("%d.%m.%Y")}''')}">{a.deals} {render_degrees(a.deals_degrees)}</a>"""
        ),
    }

    name = "Торговля"
    name_plural = "Торговля"

    column_default_sort = ("end_date", "desc")

    page_size = 100

    list_template = "sqladmin/list-traders-statistics.html"

    column_labels = {
        "trader": "Трейдер",
        "cash_balance": "Баланс",
        "stock_balance": "Портфель",
        "active_lots": "Лоты",
        "deals": "Сделки",
        "trade_volume": "Оборот",
        "income": "Прибыль",
        "yield_": "Маржа",
        "gain": "Успех",
        "tickers": "Тикеры",
    }

    diapazon_filter_fields = [
        TraderStatisticOrm.stock_balance,
        TraderStatisticOrm.deals,
        TraderStatisticOrm.trade_volume,
        TraderStatisticOrm.income,
        TraderStatisticOrm.yield_,
        TraderStatisticOrm.gain,
        TraderStatisticOrm.tickers,
    ]
    
    def filters_from_request(self, request: Request) -> Select:
        filters = super().filters_from_request(request)
        trader_id = request.query_params.get("trader_id")
        period = request.query_params.get("period", StatisticPeriodEnum.week)
        search = request.query_params.get("search", None)

        filters &= and_(TraderStatisticOrm.period==period)

        if search:
            filters &= and_(TraderOrm.username==search)

        if trader_id:
            filters &= and_(TraderStatisticOrm.trader_id==int(trader_id))
        else:
            filters &= and_(TraderStatisticOrm.end_date >= (datetime.today() - timedelta(days=StatisticPeriod(period).days)).date())
        return filters
    
    def sort_query(self, stmt: Select, request: Request) -> Select:
        """
        A method that is called every time the fields are sorted
        and that can be customized.
        By default, sorting takes place by default fields.

        The 'sortBy' and 'sort' query parameters are available in this request context.
        """
        sort_by = request.query_params.get("sortBy", None)
        sort = request.query_params.get("sort", "asc")

        if sort_by:
            sort_fields = [(sort_by, sort == "desc")]
        else:
            sort_fields = self._get_default_sort()

        for sort_field, is_desc in sort_fields:
            model = self.model

            parts = self._get_prop_name(sort_field).split(".")
            for part in parts[:-1]:
                model = getattr(model, part).mapper.class_
                stmt = stmt.join(model)

            if parts[-1] == "trader":
                if is_desc:
                    stmt = stmt.order_by(desc(TraderOrm.username))
                else:
                    stmt = stmt.order_by(asc(TraderOrm.username))
            else:
                if is_desc:
                    stmt = stmt.order_by(desc(getattr(model, parts[-1])))
                else:
                    stmt = stmt.order_by(asc(getattr(model, parts[-1])))
        return stmt
