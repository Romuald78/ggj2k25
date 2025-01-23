import os.path
import shutil
import PyInstaller.__main__


from ecsv3.utils.logs import ECSv3

VERSION = '0.0.1'

if __name__ == '__main__':
    # cleaning build and dist subfolders
    sub_dirs = ['build', 'dist']
    for sd in sub_dirs:
        if os.path.exists(sd):
            shutil.rmtree(sd)

    # clean all pyc files
    sub_dirs = ['ecsv3', 'launchers', 'gamejam']
    for sd in sub_dirs:
        walker = os.walk(sd)
        for w in walker:
            # folder name
            folder_name = w[0].split('/')[-1]
            if folder_name == '__pycache__':
                # remove this folder
                shutil.rmtree(w[0])

    # Running PyInstaller
    PyInstaller.__main__.run([
        'main.py',
        '--onefile',
        '--add-data=resources:resources',
        '--exclude-module=export_exec',
        '--exclude-module=launchers.arcade.configs.debug'
    ])

    # Rename executable if OK
    if os.path.exists('dist/main'):
        shutil.copy('dist/main', f"./ggj2k25-exe-v{VERSION}")
    else:
        ECSv3.error("Error in executable generation !")
