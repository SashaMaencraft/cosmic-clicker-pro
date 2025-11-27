from setuptools import setup, find_packages

setup(
    name="CosmicClickerPro",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pillow>=9.0.0",
    ],
    entry_points={
        'console_scripts': [
            'cosmicclicker=cosmic_clicker_crossplatform:run_app',
        ],
    },
    package_data={
        '': ['*.json', '*.png', '*.ico'],
    },
    author="Your Name",
    description="Cosmic Clicker Pro - Multiplatform Clicker Game",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)