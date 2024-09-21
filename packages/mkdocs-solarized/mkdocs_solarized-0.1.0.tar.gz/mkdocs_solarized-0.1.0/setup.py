from setuptools import setup, find_packages
import sys

install_requires = [
    'ansi2html==1.9.2',
    'attrs==24.2.0',
    'babel==2.16.0',
    'beautifulsoup4==4.12.3',
    'bracex==2.5',
    'certifi==2024.8.30',
    'charset-normalizer==3.3.2',
    'cli-exit-tools==1.2.6',
    'click==8.1.7',
    'colorama==0.4.6',
    'ghp-import==2.1.0',
    'idna==3.10',
    'igittigitt==2.1.4',
    'Jinja2==3.1.4',
    'lib-detect-testenv==2.0.8',
    'Markdown==3.7',
    'markdown-ansi==0.1.0',
    'markdown-exec==1.9.3',
    'MarkupSafe==2.1.5',
    'mergedeep==1.3.4',
    'mkdocs==1.6.1',
    'mkdocs-file-filter-plugin==0.2.0',
    'mkdocs-get-deps==0.2.0',
    'mkdocs-literate-nav==0.6.1',
    'mkdocs-markmap==2.4.3',
    'mkdocs-material==9.5.35',
    'mkdocs-material-extensions==1.3.1',
    'mkdocs-roamlinks-plugin==0.3.2',
    'packaging==24.1',
    'paginate==0.5.7',
    'pathspec==0.12.1',
    'platformdirs==4.3.6',
    'Pygments==2.18.0',
    'pymdown-extensions==10.9',
    'python-dateutil==2.9.0.post0',
    'PyYAML==6.0.2',
    'pyyaml_env_tag==0.1',
    'regex==2024.9.11',
    'requests==2.32.3',
    'schema==0.7.7',
    'six==1.16.0',
    'soupsieve==2.6',
    'urllib3==2.2.3',
    'watchdog==5.0.2',
    'wcmatch==9.0',
]

# Include importlib_resources for Python versions below 3.7
if sys.version_info < (3, 7):
    install_requires.append('importlib_resources')

setup(
    name='mkdocs_solarized',
    version='0.1.0',
    description='A custom MkDocs theme with solarized styles and overrides',
    author='Andrzej Zahorski',
    author_email='your.email@example.com',  # Replace with your actual email
    url='https://github.com/yourusername/mkdocs_solarized',  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'mkdocs_solarized': [
            'overrides/**/*.*',
            'templates/mkdocs.yml',
        ],
    },
    install_requires=install_requires,
    entry_points={
        'mkdocs.themes': [
            'solarized = mkdocs_solarized',
        ],
        'console_scripts': [
            'mkdocs-solarized-init=mkdocs_solarized.cli:main',
        ],
    },
    classifiers=[
        'Framework :: MkDocs',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
