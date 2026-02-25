# WebSentinel
WebSentinel is a modular Dynamic Application Security Testing (DAST) engine that automatically scans web applications for common vulnerabilities by interacting with live endpoints.
It performs intelligent crawling, form discovery, payload injection, and response analysis to identify security weaknesses such as SQL injection, reflected cross site scripting, insecure headers, and abnormal response behavior.
The system is designed to simulate real world attack patterns while maintaining structured reporting and severity classification.

## Core Features

-Recursive internal crawler with depth control
-Automatic form and input field extraction
-SQL injection payload testing with response diff analysis
-Reflected XSS detection via injection and reflection checks
-HTTP security header analysis
-Baseline response hashing and anomaly detection
-JSON and Markdown vulnerability reports
-Parallelized scanning with rate limiting

## Architecture

WebSentinel is built with a modular architecture:
-Crawler module for URL discovery
-Scanner module for vulnerability testing
-Payload engine for injection strategies
-Response diff engine for anomaly detection
-Reporting engine for structured output
This separation allows easy extension through additional vulnerability plugins.

## Testing Environment

WebSentinel is designed to be tested against intentionally vulnerable applications such as:
-OWASP Juice Shop
-DVWA
-bWAPP
It should only be used on systems you own or have explicit permission to test.

## Goals

The goal of WebSentinel is to demonstrate:

-Deep understanding of HTTP mechanics
-Practical vulnerability detection logic
-False positive mitigation strategies
-Security oriented systems design
-Clean modular engineering
