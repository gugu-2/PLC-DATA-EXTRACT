import pytest
import asyncio
from core.llm_clients import create_llm_client
from core.llm_clients.mock_client import MockClient


def test_factory_creates_mock():
    client = create_llm_client(backend="mock")
    assert isinstance(client, MockClient)
    assert client.get_provider_name() == "mock"


@pytest.mark.asyncio
async def test_mock_client_generation():
    client = create_llm_client(backend="mock")
    res = await client.generate_response(prompt="Generate test block")
    assert "FUNCTION_BLOCK FB_Simulated_CyberPhysical_Benchmark" in res
    assert "END_FUNCTION_BLOCK" in res
