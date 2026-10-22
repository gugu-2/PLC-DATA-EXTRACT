import pytest
import shutil
from pathlib import Path
from core.storage import DatasetStorage


@pytest.fixture
def temp_storage(tmp_path):
    st = DatasetStorage(save_dir=tmp_path / "test_raw")
    yield st
    shutil.rmtree(tmp_path / "test_raw", ignore_errors=True)


def test_atomic_save_and_deduplication(temp_storage):
    prompt = "Test Prompt"
    code = "FUNCTION_BLOCK FB_Test END_FUNCTION_BLOCK"
    
    path, rec_id = temp_storage.save_record(
        prompt=prompt,
        code=code,
        domain_id="test_dom",
        domain_name="Test Domain",
        function_block_name="FB_Test",
        validation_metrics={"char_count": len(code)}
    )

    assert path.exists()
    assert temp_storage.is_duplicate(code) is True
    assert temp_storage.get_total_records() == 1
