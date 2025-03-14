from app.dao.base import BaseDAO
from app.core.logging import logger
from app.regions.models import Regions


class RegionsDAO(BaseDAO):
    model = Regions
