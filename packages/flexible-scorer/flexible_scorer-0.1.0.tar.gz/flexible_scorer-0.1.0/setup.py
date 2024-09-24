from setuptools import setup, find_packages

setup(
    name='flexible_scorer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'openai>=0.10.0',
        'plotly>=5.0.0',
        'scipy>=1.7.0',
    ],
    description='A flexible scoring library using OpenAI models.',
    author='Michael',
    author_email='miryaboy@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',           # Update based on your chosen license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
