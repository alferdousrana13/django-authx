# django-authx

Reusable Django authentication package with email-based authentication, OTP verification, and JWT support.

---

## 🚀 Features

- Email-based authentication (no username)
- Signup with email & password
- Email OTP verification
- Resend OTP support
- Forgot password (OTP-based)
- Reset password via OTP
- JWT authentication (access + refresh tokens)
- Role-based permissions (Admin / Manager / User)
- Fully configurable via `.env`
- Clean and consistent API response format
- Production-ready structure
- Custom signals for extensibility

---

## 📦 Installation

```bash
pip install -e .


## 🔔 Available Signals

The package exposes the following Django signals:

- `otp_created`
- `user_verified`
- `password_reset_done`

These can be used to hook in custom business logic such as:
- sending notifications
- audit logging
- onboarding flows
- analytics events