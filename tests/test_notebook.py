import nbformat
from nbclient import NotebookClient
from pathlib import Path
import pytest

NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / 'notebooks' / 'test.ipynb'
DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'external' / 'sample.jpg'

@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_notebook_runs():
    assert NOTEBOOK_PATH.exists(), f"Notebook not found: {NOTEBOOK_PATH}"
    assert DATA_PATH.exists(), f"Sample image not found: {DATA_PATH}"

    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Replace Windows-style path with POSIX path for cross-platform execution
    for cell in nb.cells:
        if cell.cell_type == 'code' and "..\\data\\external\\sample.jpg" in ''.join(cell.source):
            cell.source = cell.source.replace('..\\data\\external\\sample.jpg', str(DATA_PATH))

    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()
