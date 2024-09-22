from setuptools import setup, find_packages

setup(
    name='chroma_vector_aggregator',
    version='0.1.0',
    description='A package to aggregate embeddings in a Chroma vector store based on metadata columns.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Moudather Chelbi',
    author_email='moudather.chelbi@gmail.com',
    url='https://github.com/vinerya/chroma_vector_aggregator',
    packages=find_packages(include=['chroma_vector_aggregator', 'chroma_vector_aggregator.*']),
    install_requires=[
        'chromadb',
        'numpy',
        'scikit-learn',
        'scipy',
        'langchain',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.8',
)