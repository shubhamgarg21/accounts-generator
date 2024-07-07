# Email Generator with Browser Automation

This Python project allows you to generate emails using browser automation. It supports integrated proxy rotation, User-Agent rotation, and checks if an email is already in use. Captchas must be solved manually during email generation, as they cannot be effectively solved by any library present currently.

## Features

- **Browser Automation**: Automates the process of email generation using a web browser.
- **Proxy Rotation**: Integrated support for rotating proxies to change IP addresses.
- **User-Agent Rotation**: Rotates User-Agent headers to simulate different browsers and devices.
- **Duplicate Email Check**: Checks if an email address is already registered.

## Usage

1. **Installation**

   ```bash
   # Clone the repository
   git clone <repository-url>
   cd generate-email

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running the Script**

   ```bash
   python run.py
   ```

   Follow the on-screen instructions to input captchas when prompted.

## Future Work

- Integration of LLM models to automate solving advanced captchas commonly used today.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the GPL 3.0 License - see the LICENSE file for details.

---