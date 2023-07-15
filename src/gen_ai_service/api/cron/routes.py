from typing import Annotated

from fastapi import APIRouter, Depends

from ...helpers.exception_handler_route import ExceptionHandlerRoute
from ...llms.cron.cron import CronExpressionGenerator
from .dependencies import get_cron_expression_generator
from .models import CronPrompt

router = APIRouter(route_class=ExceptionHandlerRoute)


@router.post("/")
async def generate_cron(
    cron_prompt: CronPrompt,
    cron_generator: Annotated[
        CronExpressionGenerator,
        Depends(get_cron_expression_generator),
    ],
) -> dict[str, str]:
    result = await cron_generator.generate_cron_expr(cron_prompt.text)
    return {"result": result}
