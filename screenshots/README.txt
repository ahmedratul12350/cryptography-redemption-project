SCREENSHOT INDEX

01_GitHub_SSH
--------------
01_ssh_key_files.png
  Shows the generated Ed25519 public/private key filenames in the .ssh folder.

02_github_registered_ssh_key.png
  Shows the public SSH key registered in GitHub account settings.

03_ssh_agent_key_and_authentication.png
  Shows ssh-agent running, the key being added, fingerprint output, and GitHub SSH authentication.

04_github_ssh_authentication_success.png
  Clean proof of successful `ssh -T git@github.com` authentication.

05_git_push_over_ssh_success.png
  Shows a successful Git push to GitHub through the SSH remote.

02_Wireshark_HTTP_vs_HTTPS
--------------------------
01_http_plaintext_credentials_tcp_stream.png
  Shows the dummy username/password readable in the HTTP POST TCP stream.

02_https_tls_capture_application_data.png
  Shows TLS 1.3 Application Data packets captured on HTTPS port 18443.

03_https_encrypted_tcp_stream.png
  Shows the HTTPS TCP stream as unreadable encrypted data.

04_https_encrypted_application_data_packet.png
  Shows Wireshark packet details identifying encrypted TLS Application Data.
