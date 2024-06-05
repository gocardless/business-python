Vulnerabilities are flaws in software and services that, if exploited, may allow malicious actors to perform reconnaissance, steal sensitive information, perform protected actions, or make a system or service unavailable. A confirmed vulnerability is usually registered by MITRE as a CVE ([Common Vulnerability or Exposure](https://cve.mitre.org/)) and assigned a CVSS ([Common Vulnerability Scoring System](https://www.sans.org/blog/what-is-cvss/)) score to reflect the potential risk it could introduce to an organisation.

Exploitation is the next step after finding a vulnerability. Exploits are the means through which a vulnerability can be leveraged for malicious activity by perpetrators. Exploits can manifest as pieces of software, sequences of commands, or even open-source exploit kits.

Alongside following secure design, development, and configuration principles, GoCardless performs regular vulnerability assessments and security tests to identify flaws in our production services and systems that may be exploited for malicious purposes.

GoCardless also looks forward to working with the security community to find security vulnerabilities enabling us to keep our business and customers safe.

# Report a Vulnerability
If you think you have identified a vulnerability and can present a proof of concept (PoC) or other evidence that a vulnerability exists in our systems or services, please use our public [Bug Bounty program](https://hackerone.com/gocardless_bbp) to submit a report.

Alternatively, email [vuln-disc@gocardless.com](mailto:vuln-disc@gocardless.com) to receive further instructions on reporting a vulnerability to the GoCardless security team.

Please do not discuss any vulnerabilities (even resolved ones) outside of the program without express consent from GoCardless.

Please review our [vulnerability disclosure policy](https://hackerone.com/gocardless_bbp?view_policy=true) before submitting a report.

# Testing Restrictions
Please conduct dynamic testing on our Sandbox environment only. You can sign up for a [Sandbox account](https://manage-sandbox.gocardless.com/signup) to get started. Our [developer documentation](https://developer.gocardless.com/getting-started/introduction) provides details on how to configure an account.

There is currently no Sandbox environment for the Bank Account Data portal. As such, no automated scanning is to be conducted, and only manual testing is permitted on the following in-scope domains (both represent the same application):
* https://bankaccountdata.gocardless.com
* https://ob.gocardless.com
Consult the [documentation](https://developer.gocardless.com/bank-account-data/sandbox) to find out how to use sandbox bank details for Bank Account Data testing purposes.

You must use a [HackerOne email alias](https://docs.hackerone.com/hackers/hacker-email-alias.html) account for accounts configured in our environments (e.g., `hacker123@wearehackerone.com`).

You must not conduct denial of service or other forms of destructive testing, and social engineering against GoCardless employees or customers is strictly prohibited.

# Response Targets
GoCardless will make the best effort to meet the following response targets for processing submissions from the community:

* Time to first response (from report submission) - 5 business days
* Time to triage (from report submission) - 10 business days
* Time to bounty (from report submission) - 30 business days

# Scope
You can review the full scope of our bug bounty and vulnerability disclosure programme on the [program scope page](https://hackerone.com/gocardless_bbp/policy_scopes).

Our [public GitHub repositories](https://github.com/gocardless?q=&type=public&language=&sort=) are also included.

# Out of Scope
Third-party services are out of scope for this program, even if they are accessible under an in-scope URL. This would typically include services, such as Zendesk or externally hosted forms.

GitHub repositories under the GoCardless organisation that are forks, mirrors, or archived are out of scope.

Please refer to our [vulnerability disclosure program page](https://hackerone.com/gocardless_bbp?view_policy=true) for a full list of vulnerabilities that are considered to be out of scope.
 
# Safe Harbor
Any activities conducted in a manner consistent with this policy will be considered authorized conduct and we will not initiate legal action against you. If legal action is initiated by a third party against you in connection with activities conducted under this policy, we will take steps to make it known that your actions were conducted in compliance with this policy.
