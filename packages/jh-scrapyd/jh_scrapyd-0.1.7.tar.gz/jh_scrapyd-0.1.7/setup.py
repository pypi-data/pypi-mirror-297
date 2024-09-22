from setuptools import setup, find_packages

setup(
    name='jh_scrapyd',
    version='0.1.7',
    packages=find_packages(),
    license='MIT',
    description='Preemptive scraping cluster',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mr Ye',
    author_email='mrye5869@gmail.com',
    url='https://github.com/mrye5869/jh_scrapyd',
    install_requires=[
        # 依赖列表
        'scrapyd>=1.4.3'
    ]
)