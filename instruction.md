There's an Apache-style access log at /app/access.log. Parse it and write a summary
report to /app/report.json.

Success criteria:

1. /app/report.json exists.
2. It contains a single JSON object with exactly these keys: `total_requests`,
   `unique_ips`, `top_path`.
3. `total_requests` equals the total number of log lines (requests) in the file.
4. `unique_ips` equals the number of distinct client IP addresses that appear.
5. `top_path` equals the single most frequently requested path (the request
   target, e.g. `/index.html`), counting each request regardless of HTTP
   method or status code.
