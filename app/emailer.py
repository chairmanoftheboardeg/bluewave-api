# Placeholder: production should use Resend/SendGrid/Mailgun.
# For now we just log to console so the flow is complete.

def send_email(to: str, subject: str, body: str) -> None:
    print("=== EMAIL (stub) ===")
    print("TO:", to)
    print("SUBJECT:", subject)
    print("BODY:", body)
    print("====================")
