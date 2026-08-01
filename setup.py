cat > setup.py << 'EOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-code-review",
    version="1.0.0",
    author="Divya",
    author_email="your-email@example.com",
    description="AI-powered code review system with ChatGPT-like capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-code-review",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.9",
    install_requires=[
        "Django>=4.2.3",
        "djangorestframework>=3.14.0",
        "django-cors-headers>=4.1.0",
        "python-dotenv>=1.0.0",
        "psycopg2-binary>=2.9.6",
        "djangorestframework-simplejwt>=5.2.2",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-code-review=manage:main",
        ],
    },
)
EOF