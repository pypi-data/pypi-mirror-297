from setuptools import setup, Extension

# Определяем модуль
module = Extension(
    'Kpickmenu',  # Название модуля
    sources=['Kpickmenu.c'],  # Исходные файлы
    libraries=['msvcrt']  # Библиотеки, которые нужно подключить
)

# Настройка пакета
setup(
    name='Kpickmenu',  # Название вашей библиотеки
    version='1.0',  # Версия библиотеки
    description='Python module for creating menus',  
    ext_modules=[module],  
    author='krendel',  
    author_email='39krendeloff39@gmail.com',  
    url='https://github.com/krendel001/Kpick', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    classifiers=[
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',  
)