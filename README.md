# Account Generator with Browser Automation

This Python project allows you to generate accounts using browser automation. It supports integrated proxy rotation, User-Agent rotation, and checks if an account is already in use. Captchas must be solved manually during account generation, as they cannot be effectively solved by any library present currently.

## Features

- **Browser Automation**: Automates the process of account generation using a web browser.
- **Proxy Rotation**: Integrated support for rotating proxies to change IP addresses.
- **User-Agent Rotation**: Rotates User-Agent headers to simulate different browsers and devices.
- **Duplicate Email Check**: Checks if an account is already registered.

## Usage

1. **Installation**

   ```bash
   # Clone the repository
   git clone <repository-url>
   cd account-generator

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Running the Script**

   ```bash
   python run.py
   ```

   Follow the on-screen instructions to input captchas when prompted. Also, chromedriver should pe available in the system PATH.

## Future Work

- Integration of LLM models to automate solving advanced captchas commonly used today.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the GPL 3.0 License - see the LICENSE file for details.

---