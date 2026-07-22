There's an Apache-style access log at /app/access.log. Parse it and write a JSON
summary report to /app/report.json.

Each line follows the common log format, e.g. `192.168.0.1 - - [16/Jun/2026:10:00:01
+0000] "GET /index.html HTTP/1.1" 200 1024`. The client IP is the first field, and
the requested path is the second token inside the quoted request line.

The report must be a JSON object with exactly three keys: total_requests, the total
number of log lines in the file; unique_ips, the number of distinct client IP
addresses across all lines; and top_path, the request path that occurs most often
in the log.

Success criteria:
1. /app/report.json exists and contains valid JSON.
2. The JSON object has exactly the keys total_requests, unique_ips, and top_path (no others).
3. total_requests equals the number of non-blank lines in /app/access.log.
4. unique_ips equals the number of distinct client IP addresses in /app/access.log.
5. top_path equals the most frequently requested path in /app/access.log.
