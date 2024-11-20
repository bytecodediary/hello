# Security Policy

## Supported Versions

We take security seriously and work hard to ensure the safety and integrity of the system. The following versions of the system are currently supported for security updates:

| Version        | Supported          |
| -------------- | ------------------ |
| v1.0.x         | ✅ Supported        |
| v0.x.x         | ❌ Not supported    |

---

## Reporting a Vulnerability

If you discover any security vulnerabilities or potential threats within the real estate system, please follow the steps below:

1. **Do not open a public issue.**  
   Instead, email us directly at **[security@greywolfx.com](mailto:security@greywolfx.com)** to ensure the vulnerability is addressed before any public disclosure.

2. Provide as much detail as possible to help us quickly understand and resolve the issue:
   - A detailed description of the vulnerability.
   - Steps to reproduce the vulnerability (if applicable).
   - Any proof-of-concept (PoC) code or links.
   - The potential impact and severity of the issue.

3. We aim to acknowledge your email within **48 hours** and will work to resolve the issue promptly, providing patches and mitigations as necessary.

---

## Security Update Process

We follow a responsible disclosure process:
1. Vulnerabilities are confirmed internally, and patches are created.
2. If necessary, we may request more details or work with the reporter to better understand the issue.
3. After a fix is developed, it will be applied to the most recent version(s).
4. A security advisory will be posted with details on the vulnerability and the patch.

---

## Scope

The following areas are considered in-scope for security vulnerabilities:
- Authentication and Authorization (e.g., user login, session handling)
- Data integrity (e.g., database access control, data leaks)
- API Security (e.g., access control, improper validation)
- Code injections (e.g., SQL injection, command injection)
- Access Control & Privilege Escalation
- Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF)
- Sensitive Data Exposure (e.g., PII, financial data)

**Out-of-scope:**
- Social engineering attacks (e.g., phishing)
- DDoS (Distributed Denial of Service) attacks
- Issues found on outdated versions not supported by us

---

## Security Best Practices

To help ensure the security of your system, we recommend:
- Keeping your system up to date with the latest versions.
- Regularly auditing your own infrastructure for misconfigurations.
- Using strong, unique passwords and enabling two-factor authentication (2FA) where possible.

---

## Thank You

We deeply appreciate responsible security researchers who help us keep the system secure. All vulnerability reporters will be credited and thanked unless they wish to remain anonymous.
