from setuptools import setup, find_packages

setup(
    name="dropdown_filters",  # El nombre del paquete
    version="0.2",  # Versión inicial
    description="Reusable Django admin filters",  # Breve descripción
    long_description=open('README.md').read(),  # Descripción más larga (README.md)
    long_description_content_type='text/markdown',
    author="Diego Piedra",
    author_email="diego@dieveloper.com",
    url="https://github.com/DiegoP2001/Dropdown_filters",  # Si lo publicas en GitHub u otro lugar
    packages=find_packages(),  # Esto encuentra todos los paquetes automáticamente
    include_package_data=True,  # Incluye archivos estáticos y plantillas
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=2.0.8",  # Versión mínima de Django requerida
    ],
)
