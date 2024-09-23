from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
with codecs.open(readme_path, encoding="utf-8") as fh:
    long_description = fh.read()
VERSION = '0.0.1'
DESCRIPTION = 'Complementing topic models with few-shot in-context learning to generate interpretable topics'
LONG_DESCRIPTION = 'Complementing topic models with few-shot in-context learning to generate interpretable topics from keywords of topic models (e.g., LDA, BERTopic)'

# Setting up
setup(
    name="ConTextMining",
    version=VERSION,
    author="Charles Alba",
    author_email="alba@wustl.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['torch', 'transformers', 'tokenizers', 'huggingface-hub','accelerate','flash_attn'],
    keywords=['generative AI', 'text mining', 'topic modeling', 'LLMs'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)