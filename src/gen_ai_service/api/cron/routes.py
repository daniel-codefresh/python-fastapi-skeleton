from fastapi import APIRouter, Depends
from .models import CronPrompt
from .dependencies import get_cron_expression_generator

from ...llms.cron.cron import CronExpressionGenerator


router = APIRouter()


@router.post("/")
async def generate_cron(
    cron_prompt: CronPrompt,
    cron_generator: CronExpressionGenerator = Depends(get_cron_expression_generator),
):
    result = await cron_generator.generate_cron_expr(cron_prompt.text)
    return {"result": result}
