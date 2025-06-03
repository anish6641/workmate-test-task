from typing import List, Dict, Any

class CSVParser:
    """Parses CSV files without using the csv module."""
    
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.valid_rate_columns = {'hourly_rate', 'rate', 'salary'}

    def parse(self) -> List[Dict[str, Any]]:
        """Parse all CSV files and return a list of employee records."""
        employees = []
        for file_path in self.file_paths:
            employees.extend(self._parse_file(file_path))
        return employees

    def _parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a single CSV file."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return []
                
                # Extract headers and normalize
                headers = lines[0].strip().split(',')
                rate_column = self._find_rate_column(headers)
                if not rate_column:
                    raise ValueError(f"No valid rate column found in {file_path}")
                
                # Map headers to standard keys
                header_map = {h: h for h in headers}
                if rate_column in header_map:
                    header_map[rate_column] = 'hourly_rate'

                # Parse rows
                result = []
                for line in lines[1:]:
                    values = line.strip().split(',')
                    if len(values) != len(headers):
                        continue  # Skip malformed rows
                    employee = {}
                    for header, value in zip(headers, values):
                        key = header_map[header]
                        # Convert numeric fields
                        if key in ('hours_worked', 'hourly_rate', 'id'):
                            try:
                                employee[key] = float(value) if '.' in value else int(value)
                            except ValueError:
                                continue
                        else:
                            employee[key] = value
                    result.append(employee)
                return result
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return []
        except ValueError as e:
            print(f"Error processing {file_path}: {e}")
            raise  # Re-raise ValueError for tests
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []

    def _find_rate_column(self, headers: List[str]) -> str:
        """Identify the rate column from possible names."""
        for header in headers:
            if header in self.valid_rate_columns:
                return header
        return ""
