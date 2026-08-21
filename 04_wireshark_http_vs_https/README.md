# Lab 4 — Wireshark: HTTP vs HTTPS Credentials

## Safety boundary

Perform this only against the included **localhost lab server** and use **dummy credentials**. Do not capture other people's traffic or real account passwords.

## Objective

Submit the same dummy login form over:

- HTTP on `127.0.0.1:18080`
- HTTPS/TLS on `127.0.0.1:18443`

Then compare the packet contents in Wireshark.

## 1. Start the HTTP server

Terminal 1:

```bash
cd 04_wireshark_http_vs_https
python local_login_server.py
```

Open:

```text
http://127.0.0.1:18080
```

Use dummy values such as:

```text
Username: student_demo
Password: NotARealPassword123!
```

## 2. Create a one-day self-signed certificate for the HTTPS lab

In the same folder:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 1 -subj "/CN=localhost"
```

PowerShell can run the same OpenSSL command on one line:

```powershell
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 1 -subj "/CN=localhost"
```

## 3. Start the HTTPS server

Terminal 2:

```bash
cd 04_wireshark_http_vs_https
python local_login_server.py --https
```

Open:

```text
https://127.0.0.1:18443
```

Because the certificate is self-signed for a local lab, the browser will warn that it is not trusted. Continue only for this localhost exercise, or use curl with `-k`.

Example HTTP request using curl:

```bash
curl -d "username=student_demo&password=NotARealPassword123!" http://127.0.0.1:18080/login
```

Example HTTPS request using curl:

```bash
curl -k -d "username=student_demo&password=NotARealPassword123!" https://127.0.0.1:18443/login
```

## 4. Capture only the local lab traffic in Wireshark

On Windows, select the loopback capture interface provided by Npcap (often shown as **Npcap Loopback Adapter**). On Linux/macOS, use the loopback interface if available.

Useful **display filters**:

```text
tcp.port == 18080
```

```text
tcp.port == 18443
```

For HTTP POST requests:

```text
http.request.method == "POST"
```

## 5. Compare the streams

For the HTTP test:

1. Select an HTTP packet.
2. Choose **Analyze → Follow → TCP Stream** (or follow the HTTP stream).
3. The form body should be readable because HTTP itself does not encrypt the request payload.

For the HTTPS test:

1. Select traffic on TCP port 18443.
2. Observe the TLS handshake and encrypted application data.
3. Following the raw TCP stream should not reveal the dummy username/password in plaintext because TLS protects the application payload.

## Expected result table

| Property | HTTP | HTTPS |
|---|---|---|
| Application payload encrypted | No | Yes, by TLS |
| Dummy form fields visible in ordinary packet inspection | Yes | No |
| Suitable for real login credentials | No | Yes, when certificate validation is correct |

## Screenshots to submit

1. Wireshark HTTP packet list filtered to port 18080.
2. HTTP Follow TCP Stream showing the **dummy** form fields.
3. Wireshark HTTPS/TLS packet list filtered to port 18443.
4. HTTPS stream showing encrypted/binary TLS application data rather than readable dummy credentials.

## Key conclusion

HTTP transmits application data without transport encryption, so anyone able to observe that network path may be able to read sensitive form data. HTTPS wraps HTTP inside TLS, which protects confidentiality and integrity in transit when correctly configured and validated.
