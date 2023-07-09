from functools import lru_cache

from ...llms.cron.cron import CronExpressionGenerator


@lru_cache()
def get_cron_expression_generator():
    return CronExpressionGenerator()
