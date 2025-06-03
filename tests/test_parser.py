import pytest
from parser import CSVParser

def test_parse_valid_csv(tmp_path):
    # Create a temporary CSV file
    csv_content = """id,email,name,department,hours_worked,rate
1,alice@example.com,Alice,Marketing,160,50
2,bob@example.com,Bob,Design,150,40"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    
    parser = CSVParser([str(file_path)])
    employees = parser.parse()
    
    assert len(employees) == 2
    assert employees[0] == {
        'id': 1,
        'email': 'alice@example.com',
        'name': 'Alice',
        'department': 'Marketing',
        'hours_worked': 160,
        'hourly_rate': 50
    }

def test_parse_missing_file():
    parser = CSVParser(["nonexistent.csv"])
    employees = parser.parse()
    assert employees == []

def test_parse_invalid_rate_column(tmp_path):
    csv_content = """id,email,name,department,hours_worked,invalid
1,alice@example.com,Alice,Marketing,160,50"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    
    parser = CSVParser([str(file_path)])
    with pytest.raises(ValueError, match="No valid rate column found"):
        parser.parse()
