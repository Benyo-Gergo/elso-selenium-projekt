# 🤖 Advanced SauceDemo Automation Bot

A professional-grade Python automation script using **Selenium WebDriver**. This project demonstrates robust web interaction, secure credential handling, and automated reporting.

## 🚀 Key Features
* **Secure Login:** Uses `.env` files to handle credentials safely (no hardcoded passwords). 🔐
* **Error Resilience:** Implemented `try-except` blocks with **automatic screenshots** on failure. 📸
* **Technical Logging:** Generates a `robot.log` file with timestamps and error levels for debugging. 📄
* **Smart Reporting:** Automatically creates unique, timestamped `.txt` reports of all purchases. 💰
* **Data-Driven Logic:** Filters products based on price limits dynamically.

## 🛠️ Tech Stack
* **Python 3** 🐍
* **Selenium WebDriver** 🌐
* **python-dotenv** (Environment variable management)
* **Webdriver-manager** (Automated driver handling)

## 📦 Installation & Usage
1.  **Clone the repo:**
    `git clone https://github.com/Benyo-Gergo/elso-selenium-projekt.git`
2.  **Install dependencies:**
    `pip install selenium webdriver-manager python-dotenv`
3.  **Setup Credentials:** Create a `.env` file in the root folder:
    ```text
    SAUCE_USER=your_username
    SAUCE_PASSWORD=your_password
    ```
4.  **Run the script:**
    `python main.py`

## 👤 Author
**Gergo Benyo**
*QA Automation Enthusiast* 👨‍💻
