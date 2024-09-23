import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Email Validator CLI.')
    
    parser.add_argument(
        '--emails',
        type=str,
        required=True,
        help='Comma-separated list of email addresses to verify.'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=5,  # Set a default timeout value
        help='SMTP timeout in seconds (default: 30).'
    )

    parser.add_argument(
        '--output',
        type=str,
        # required=True,
        help='Output file name to store the results (supports .txt and .xlsx formats).'
    )
    
    return parser.parse_args()
