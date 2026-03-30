import logging
import time

import pytest

# We want to test chunk sizes of 500, 1000, 2000, 5000, and 10000
chunk_scenarios = [
    {"records": 50000, "chunk_size": 500},
    {"records": 50000, "chunk_size": 1000},
    {"records": 50000, "chunk_size": 2000},
    {"records": 50000, "chunk_size": 5000},
    {"records": 50000, "chunk_size": 10000},
]


@pytest.mark.load
@pytest.mark.parametrize("setup_bulk_parents", chunk_scenarios, indirect=True)
def test_benchmark_chunk_sizes(setup_bulk_parents, request, capsys):
    # caplog.set_level(logging.INFO)

    # Intentionally fail the test and dump the captured log text to the console
    # Check the logs for the chunk times, to choose the best chunk_size
    captured = capsys.readouterr()
    # assert False, f"\n--- BENCHMARK RESULTS ---\n{captured.out}"
