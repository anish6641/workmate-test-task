import pytest
from report import PayoutReport

def test_payout_report():
    data = [
        {'id': 1, 'name': 'Alice', 'department': 'Marketing', 'hours_worked': 160, 'hourly_rate': 50},
        {'id': 2, 'name': 'Bob', 'department': 'Design', 'hours_worked': 150, 'hourly_rate': 40}
    ]
    report = PayoutReport()
    output = report.generate(data)
    
    assert "ID | Name  | Department | Hours Worked | Hourly Rate | Payout" in output
    assert "1  | Alice | Marketing  | 160.00       | $50.00      | $8000.00" in output
    assert "2  | Bob   | Design     | 150.00       | $40.00      | $6000.00" in output

def test_payout_report_empty():
    report = PayoutReport()
    output = report.generate([])
    assert output == "No data to display."
