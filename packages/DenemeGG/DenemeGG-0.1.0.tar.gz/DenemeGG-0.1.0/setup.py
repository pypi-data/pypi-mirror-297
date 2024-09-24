from setuptools import setup, find_packages

setup(
    name="DenemeGG",                    # The name of your package
    version="0.1.0",                  # Version of your package
    author="Göktuğ",                  # Your name
    author_email="goktugonal76@gmail.com", # Your email address
    description="A simple package to greet users",  # A short description
    long_description=open("README.md").read(),      # Detailed description (from your README file)
    long_description_content_type="text/markdown",  # README format (usually markdown)
    url="https://github.com/GoktugSuvorun/DenemeGG.git",  # Your project's URL (GitHub or other repo)
    packages=find_packages(),         # Automatically find and include all packages in the directory
    classifiers=[                     # Additional metadata to classify your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',          # Minimum Python version required to run your package
    install_requires=[                # Dependencies that your package needs (if any)
        "numpy",                      # Example of a dependency
        "pandas",                     # Another example dependency
    ],
)
