from setuptools import setup, find_packages

setup(
    name="screen-stream",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Session',
        'opencv-python-headless',
        'mss',
        'numpy',
        'pyautogui',
        'pypiwin32',
        'psutil',
        'socket'
    ]
) 