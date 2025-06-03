import argparse
from parser import CSVParser
from report import ReportFactory

def main():
    parser = argparse.ArgumentParser(description="Employee payroll report generator")
    parser.add_argument('files', nargs='*', help="CSV files to process")  # Files optional
    parser.add_argument('--report', required=True, help="Report type (e.g., payout)")
    
    args = parser.parse_args()
    
    try:
        # Validate report type before parsing files
        report = ReportFactory.create_report(args.report)  # Raises ValueError for invalid report
        
        # Check for input files
        if not args.files:
            raise ValueError("At least one input file is required")
        
        # Parse CSV files
        csv_parser = CSVParser(args.files)
        employees = csv_parser.parse()
        
        if not employees:
            print("No valid employee data found.")
            return
        
        # Generate report
        output = report.generate(employees)
        print(output)
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
