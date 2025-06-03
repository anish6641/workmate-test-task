from typing import List, Dict, Any

class Report:
    """Base class for reports."""
    def generate(self, data: List[Dict[str, Any]]) -> str:
        raise NotImplementedError

class PayoutReport(Report):
    """Generates a payroll report in tabular format."""
    
    def generate(self, data: List[Dict[str, Any]]) -> str:
        """Generate a tabular payroll report with $ prefix."""
        if not data:
            return "No data to display."
        
        # Define table headers
        headers = ["ID", "Name", "Department", "Hours Worked", "Hourly Rate", "Payout"]
        rows = []
        for employee in data:
            payout = employee['hours_worked'] * employee['hourly_rate']
            rows.append([
                str(int(employee['id'])),  # Ensure ID is integer
                employee['name'],
                employee['department'],
                f"{employee['hours_worked']:.2f}",  # 2 decimal places
                f"${employee['hourly_rate']:.2f}",  # $ prefix for hourly rate
                f"${round(payout, 2):.2f}"  # $ prefix for payout
            ])
        
        # Calculate column widths
        widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(cell))
        
        # Build table
        output = []
        # Header row
        header_row = " | ".join(f"{header:<{widths[i]}}" for i, header in enumerate(headers))
        output.append(header_row)
        output.append("-" * (sum(widths) + 3 * (len(headers) - 1)))  # Separator
        # Data rows
        for row in rows:
            row_str = " | ".join(f"{cell:<{widths[i]}}" for i, cell in enumerate(row))
            output.append(row_str)
        
        return "\n".join(output)

class ReportFactory:
    """Factory to create report instances."""
    
    @staticmethod
    def create_report(report_type: str) -> Report:
        if report_type == 'payout':
            return PayoutReport()
        raise ValueError(f"Unknown report type: {report_type}")
