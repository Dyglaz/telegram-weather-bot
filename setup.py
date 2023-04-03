from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name='telegram-weather-bot',
        version='0.1',
        packages=find_packages(),
        install_requires=[
            "matplotlib",
            "pyTelegramBotAPI",
            "python_telegram_bot",
            "requests",
            "setuptools",
            "telegram",
            "wikipedia"
        ],
        data_files=[('config', ['/config.py'])]
    )
