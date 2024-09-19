import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Email Validator CLI.')
    
    # Argument for the email list
    parser.add_argument(
        '--emails',
        type=str,
        required=True,
        help='Comma-separated list of email addresses to verify.'
    )
    
    # Optional timeout argument
    parser.add_argument(
        '--timeout',
        type=int,
        default=5,  # Default timeout value
        help='Timeout for the SMTP operation (default: 5 seconds).'
    )
    
    # Argument for the output file
    parser.add_argument(
        '--output',
        type=str,
        # required=True,
        help='Output file name to store the results (supports .txt and .xlsx formats).'
    )
    
    return parser.parse_args()
