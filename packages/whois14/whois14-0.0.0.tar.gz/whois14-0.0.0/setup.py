from setuptools import setup

APP = ['whois14.py']  # Replace with your actual Python script name
OPTIONS = {
    'argv_emulation': True,
    # Remove or add actual packages if your script uses any
    # 'packages': ['some_package'], 
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
