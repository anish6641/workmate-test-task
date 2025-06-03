from typing import List, Dict, Any
import json

class Report:
    """Base class for reports."""
    def generate(self, data: List[Dict[str, Any]], output_format: str = 'table') -> str:
        raise NotImplementedError

class PayoutReport(Report):
    """Generates a payroll report in tabular or JSON format."""
    
    def generate(self, data: List[Dict[str, Any]], output_format: str = 'table') -> str:
        """Generate a payroll report."""
        if not data:
            return "No data to display." if output_format == 'table' else json.dumps([])
        
        # Prepare report data
        report_data = []
        for employee in data:
            payout = employee['hours_worked'] * employee['hourly_rate']
            report_data.append({
                'id': int(employee['id']),
                'name': employee['name'],
                'department': employee['department'],
                'hours_worked': float(employee['hours_worked']),
                'hourly_rate': float(employee['hourly_rate']),
                'payout': float(round(payout, 2))
            })

        if output_format == 'json':
            return json.dumps(report_data, indent=2, ensure_ascii=False)

        # Tabular format
        headers = ["ID", "Name", "Department", "Hours Worked", "Hourly Rate", "Payout"]
        rows = []
        for item in report_data:
            rows.append([
                str(item['id']),
                item['name'],
                item['department'],
                f"{item['hours_worked']:.2f}",
                f"${item['hourly_rate']:.2f}",
                f"${item['payout']:.2f}"
            ])

        # Calculate column widths
        widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(cell))

        # Build table
        output = []
        header_row = " | ".join(f"{header:<{widths[i]}}" for i, header in enumerate(headers))
        output.append(header_row)
        output.append("-" * (sum(widths) + 3 * (len(headers) - 1)))
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
