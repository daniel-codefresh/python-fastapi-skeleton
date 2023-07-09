from fastapi.testclient import TestClient
from src.python_project_skeleton.api.cron.routes import router as cron_router
from src.python_project_skeleton.api.cron.models import CronPrompt
from src.python_project_skeleton.api.cron.dependencies import get_cron_expression_generator
from src.python_project_skeleton.llms.cron.cron import CronExpressionGenerator
from src.python_project_skeleton.main import app

client = TestClient(app)

def test_generate_cron():
    # We'll use a fixed cron expression for testing
    mock_cron_expression = "0 * * * *"

    # Create a mock instance of CronExpressionGenerator
    class MockCronExpressionGenerator:
        async def generate_cron_expr(self, cron_prompt: str) -> str:
            return mock_cron_expression

    # Replace the original dependency with our mock instance
    app.dependency_overrides[get_cron_expression_generator] = MockCronExpressionGenerator

    # Send a POST request to the route
    response = client.post("/api/cron/", json={"text": "every hour"})

    # Check the status code and the json response
    assert response.status_code == 200
    assert response.json() == {"result": mock_cron_expression}

    # Remove the dependency override
    del app.dependency_overrides[get_cron_expression_generator]
