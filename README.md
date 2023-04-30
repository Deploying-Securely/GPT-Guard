# GPT-Guard
A lightweight library to sanitize data provided to AI tools.

# Setup
```pip install gpt-guard\n
from gpt_guard import extract_sensitive_data, re_append_sensitive_data

# Usage Example
```query_text = ("Please summarize this technical document for ACME CORP:\
## Introduction \
This document provides technical details for the deployment a web application. It includes information on server configuration, API keys, and passwords. \
## Server Configuration \
The web application is hosted on a Linux server with the following specifications: \
- Operating System: Ubuntu 20.04 LTS \
- Processor: Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz \
- Memory: 64 GB RAM \
- Storage: 1 TB SSD \
The server is connected to the internet through a fiber-optic network with the following IPv4 address: `192.168.0.100`. The server also has an IPv6 address of `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. \
## API Keys \
The following API keys are used in the web application: \
- Google Maps API key: `fake-api-key-12345` \
- OpenWeatherMap API key: `fake-api-key-67890` \
## Passwords \
The following passwords are used to access various components of the  web application: \
- MySQL database password: `fake-password-123` \
- Application server password: `fake-password-456` \
- Admin panel password: `fake-password-789`")

sanitized = sanitize_query(query_text, custom_identifiers=['ACME CORP'])

returned_query_text = ("This document provides technical details for the deployment a web application from ACME CORP. It includes information on server configuration, NAME_1, and passwords. ## Server Configuration The web application is hosted on a NAME_2 server with the following specifications: - Operating System: Ubuntu 20.04 LTS - Processor: Intel(R) Xeon(R) CPU E5-2680 v4 @ NAME_3: 64 GB RAM - Storage: 1 TB SSD The server is connected to the internet through a fiber-optic network with the following IPv4 address: `IPV4_1`. The server also has an IPv6 address of `IPV6_1`. ## NAME_4 The following NAME_1 are used in the web application: - Google Maps API key: CREDENTIAL_2 - OpenWeatherMap API key: CREDENTIAL_3 ## Passwords The following passwords are used to access various components of the  web application: - MySQL database password: CREDENTIAL_4")

re_append_sensitive_data(returned_query_text, sanitized[1])
