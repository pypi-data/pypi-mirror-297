from setuptools import setup, find_packages

setup(
    name='flexible_scorer',
    version='0.1.12',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'openai',
        'plotly',
        'scipy',
    ],
    description='A flexible scoring library using OpenAI models.',
    author='Michael',
    author_email='miryaboy@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update based on your chosen license
        'Operating System :: OS Independent',
    ],
    readme="README.md",
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
)
