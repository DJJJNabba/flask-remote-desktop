import PyInstaller.__main__
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Build app.py into app.exe
PyInstaller.__main__.run([
    'app.py',
    '--onefile',
    '--noconsole',
    '--add-data', f'{script_dir}/templates;templates',
    '--add-data', f'{script_dir}/static;static',
    '--add-data', f'{script_dir}/config.py;.',
    '--add-data', f'{script_dir}/key_mapping.py;.',
    '--add-data', f'{script_dir}/restart.py;.',
    '--hidden-import', 'flask_session',
    '--collect-all', 'flask',
    '--collect-all', 'werkzeug',
    '--icon', f'{script_dir}/static/favicon.ico',
    '--name', 'AppServer'
])

# Build server_gui.py into server_gui.exe
PyInstaller.__main__.run([
    'server_gui.py',
    '--onefile',
    '--noconsole',
    '--add-data', f'{script_dir}/server_config.json;.',
    '--add-data', f'{script_dir}/config.py;.',
    '--add-data', f'{script_dir}/static;static',
    '--add-data', f'{script_dir}/templates;templates',
    '--hidden-import', 'psutil',
    '--icon', f'{script_dir}/static/favicon.ico',
    '--add-data', f'{script_dir}/static/favicon.png;static',
    '--name', 'ServerGUI'
])
