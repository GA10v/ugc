from core.config import settings
from services.clickhouse import ClickHouseClientETL

client = ClickHouseClientETL(**settings.ch.client_conf)
client.init_db()
