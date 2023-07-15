from fastapi.testclient import TestClient

from gen_ai_service.api.cron.dependencies import get_cron_expression_generator
from gen_ai_service.app import get_app
from gen_ai_service.config import Settings, get_settings
from gen_ai_service.llms.cron.cron import CronExpressionGenerator


def get_settings_override() -> Settings:
    return Settings(openai_api_key="123")


setting = get_settings_override()

app = get_app(setting)
app.dependency_overrides[get_settings] = get_settings_override

client = TestClient(app)


def test_generate_cron() -> None:
    mock_cron_expression: str = "* * * * *"

    def cron_expression_generator_override() -> CronExpressionGenerator:
        class MockCronExpressionGenerator(CronExpressionGenerator):
            async def generate_cron_expr(self, cron_prompt: str) -> str:
                return mock_cron_expression

        return MockCronExpressionGenerator(llm=None)  # type: ignore

    app.dependency_overrides[get_cron_expression_generator] = (
        cron_expression_generator_override
    )

    response = client.post(
        f"{setting.api_v1_prefix}/cron/", json={"text": "every hour"}
    )

    assert response.status_code == 200
    assert response.json() == {"result": mock_cron_expression}

    del app.dependency_overrides[get_cron_expression_generator]
