import pytest
from unittest.mock import patch
from main import main

@patch('sys.argv', ['main.py', 'sample_data/data1.csv', '--report', 'payout'])
def test_main_valid_input_table(capsys):
    with patch('parser.CSVParser.parse', return_value=[
        {'id': 1, 'name': 'Alice', 'department': 'Marketing', 'hours_worked': 160, 'hourly_rate': 50}
    ]):
        main()
        captured = capsys.readouterr()
        assert "ID | Name  | Department | Hours Worked | Hourly Rate | Payout" in captured.out
        assert "1  | Alice | Marketing  | 160.00       | $50.00      | $8000.00" in captured.out

@patch('sys.argv', ['main.py', 'sample_data/data1.csv', '--report', 'payout', '--format', 'json'])
def test_main_valid_input_json(capsys):
    with patch('parser.CSVParser.parse', return_value=[
        {'id': 1, 'name': 'Alice', 'department': 'Marketing', 'hours_worked': 160, 'hourly_rate': 50}
    ]):
        main()
        captured = capsys.readouterr()
        assert '"payout": 8000.0' in captured.out
        assert '"hours_worked": 160.0' in captured.out
        assert '"hourly_rate": 50.0' in captured.out

@patch('sys.argv', ['main.py', 'sample_data/dummy.csv', '--report', 'invalid'])
def test_main_invalid_report(capsys):
    main()
    captured = capsys.readouterr()
    assert "Error: Unknown report type: invalid" in captured.out
