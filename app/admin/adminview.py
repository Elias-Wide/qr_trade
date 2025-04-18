from sqladmin import ModelView
from app.acces_codes.models import Acces_Codes
from app.core.constants import ADMIN_VIEW_PAGE_SIZE
from app.points.models import Points
from app.regions.models import Regions
from app.sale_codes.models import SaleCodes
from app.schedules.models import Schedules
from app.trades.models import Trades
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    """Настройка страницы пользователей."""

    page_size = ADMIN_VIEW_PAGE_SIZE
    column_list = [
        Users.id,
        Users.username,
        Users.telegram_id,
        Users.point_id,
        Users.manager_id,
        Users.ban,
    ] + [Users.points, Users.schedule]
    name = "Пользователь"
    name_plural = "Пользователи"
    can_delete = True
    column_searchable_list = [
        Users.username,
        Users.telegram_id,
        Users.point_id,
        Users.manager_id,
    ]
    icon = "fa-solid fa-user"


class SchedulesAdmin(ModelView, model=Schedules):
    """Настрйоки страницы графика."""

    column_list = [Schedules.user] + [c.name for c in Schedules.__table__.c]
    name = "Оповещение"
    name_plural = "Оповещения"
    can_delete = False
    column_searchable_list = [Schedules.user_id]
    column_sortable_list = [Schedules.notice_type]
    icon = "fa fa-bell"
    can_edit = False


class PointsAdmin(ModelView, model=Points):
    """Настройки страницы офисов."""

    column_list = [c.name for c in Points.__table__.c] + [
        Points.region,
        Points.managers,
    ]
    name = "Офис"
    name_plural = "Офисы"
    can_delete = True
    column_sortable_list = [Points.addres]
    column_searchable_list = [Points.addres, Points.point_id]
    icon = "fa fa-house"


class SaleCodesAdmin(ModelView, model=SaleCodes):
    """Настройки страницы кодов продаж."""

    name = "Код продажи"
    name_plural = "Коды продаж"
    can_delete = True
    column_searchable_list = [SaleCodes.client_id]
    column_exclude_list = [SaleCodes.encoded_value, SaleCodes.trades]
    icon = "fa fa-star"


class TradesAdmin(ModelView, model=Trades):
    """Настройки страницы трейдов"""

    column_list = [c.name for c in Trades.__table__.c] + [
        Trades.users,
        Trades.point,
    ]
    name = "Трейд"
    name_plural = "Трейды"
    can_delete = True
    can_edit = False
    column_searchable_list = [Trades.user_id, Trades.point_id]
    icon = "fa fa-handshake"


class RegionsAdmin(ModelView, model=Regions):
    """Настройки страницы офисов."""

    column_list = [c.name for c in Regions.__table__.c] + [
        Regions.ceo,
        Regions.points,
    ]
    name = "Регион"
    name_plural = "Регионы"
    can_delete = True
    column_sortable_list = [Regions.name]
    column_searchable_list = [Regions.name, Regions.ceo]
    icon = "fa fa-map"


class AccesCodesAdmin(ModelView, model=Acces_Codes):
    """Настройки страницы кодов доступа."""

    column_list = [c.name for c in Acces_Codes.__table__.c]
    name = "Код доступа"
    name_plural = "Код доступа"
    can_delete = True
    icon = "fa fa-lock"


admin_views: tuple[ModelView] = (
    UsersAdmin,
    SchedulesAdmin,
    PointsAdmin,
    RegionsAdmin,
    SaleCodesAdmin,
    TradesAdmin,
    AccesCodesAdmin,
)
