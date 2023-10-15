#!/usr/bin/env python3
import os

version = os.getenv("TELEGRAM_FEEDBACK_BOT_VERSION")
if not version:
    version = "1.0.0"

if version.startswith("v"):
    version = version.lstrip("v")

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='telegram-feedback-bot',  # Required
    version=version,  # Required
    description='Advanced multi-channel file-sharing tool',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/le-p0pug-labs/telegram-feedback-bot',  # Optional
    author='LE POPUG',  # Optional
    author_email='fixions@protonmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',

        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='file-sharing, ngrok, flask',  # Optional
    package_dir={'': './src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    install_requires=[
        "pyngrok",
        "python-telegram-bot"
    ],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'telegram-feedback-bot=telegramfeedbackbot.telegram_feedback_bot:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/le-p0pug-labs/telegram-feedback-bot/issues',
        'Source': 'https://github.com/le-p0pug-labs/telegram-feedback-bot',
    },
)
