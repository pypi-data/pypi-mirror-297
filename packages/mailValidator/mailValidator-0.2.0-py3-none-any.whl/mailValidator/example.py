from mailValidator import verify_email, verify_emails_list



config= {
    "timeout": 5
}
email = "example@example.com"
result = verify_email(email)
result_config = verify_email(email, config)
print("output:")
print('result: ')
print(result)
print('result_config: ')
print(result_config)

email_list = ["anu.t@mitsogo.com", "test@example.com"]
results_list = verify_emails_list(email_list)
results_list_config = verify_emails_list(email_list, result_config)
print("-------------")
print('results_list: ' )
print(results_list )
print('results_list_config: ' )
print(results_list_config )