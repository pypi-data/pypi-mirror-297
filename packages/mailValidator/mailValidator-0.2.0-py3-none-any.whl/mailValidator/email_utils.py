import time
import re
import concurrent.futures
import socket
from mailValidator.utils.dns_utils import get_mx_record, get_domain_details
from mailValidator.utils.logger import get_logger
from mailValidator.utils.catch_all_utils import check_catch_all
from mailValidator.utils.smtp_utils import smtp_verify_email
from mailValidator.utils.config import MailValidatorConfig

logger = get_logger(__name__)

def check_network_connection(host='8.8.8.8', port=53, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, OSError):
        return False

def validate_domain(domain):
    if not domain or len(domain) > 253 or any(len(label) > 63 for label in domain.split(".")):
        return False
    return True

def verify_email(email, config=None):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if email:
        email = email.strip()
    if config is None:
        config = MailValidatorConfig()
    elif isinstance(config, dict):
        config = MailValidatorConfig(config)

    timeout = config.timeout  # Use the timeout from the config

    if not check_network_connection(timeout=timeout):
        return {"status": "503", "message": "Network connection error"}

    if email in config.whitelisted_emails:
        return {"status": "200", "message": "Whitelisted email"}
    if email in config.blacklisted_emails:
        return {"status": "403", "message": "Blacklisted email"}

    if '@' not in email or '.' not in email or re.match(pattern, email) is None:
        return {"status": "400", "message": "Invalid email format"}

    domain = email.split("@")[1]

    if not validate_domain(domain):
        logger.error(f"Invalid domain in email: {domain}")
        return {"status": "400", "message": "Invalid domain in email"}

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            mx_future = executor.submit(get_mx_record, domain, timeout=timeout)
            details_future = executor.submit(get_domain_details, domain, timeout=timeout)

            mx_record = mx_future.result()
            domain_details = details_future.result()

        if not mx_record or not domain_details:
            if check_catch_all(mx_record, domain):
                return {"status": "201", "message": "Valid email but domain is a catch-all."}
            else:
                return {"status": "404", "message": "MX record or domain details not found."}

        # Pass the timeout to SMTP verification
        result = smtp_verify_email(mx_record, email, timeout=timeout)
        return result

    except KeyboardInterrupt:
        logger.error("Operation interrupted by user.")
        return {"status": "500", "message": "Operation interrupted by user."}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"status": "500", "message": "Internal server error"}


def verify_emails_list(email_list, config=None):
    if config is None:
        config = MailValidatorConfig()
    elif isinstance(config, dict):
        config = MailValidatorConfig(config)
        
    results_by_status = {}

    if not check_network_connection():
        for email in email_list:
            results_by_status["503"].append((email, "Network connection error"))
        return results_by_status

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_email = {executor.submit(verify_email, email, config): email for email in email_list}
        for future in concurrent.futures.as_completed(future_to_email):
            email = future_to_email[future]
            try:
                result= future.result()
                results_by_status[email] = future.result()
            except Exception as e:
                logger.error(f"An error occurred while verifying {email}: {e}")
                results_by_status["500"].append((email, "Internal error"))
    
    return results_by_status
