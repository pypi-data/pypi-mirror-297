# llmtranslate
[![Test](https://github.com/adam-pawelek/llmtranslate/actions/workflows/test.yml/badge.svg)](https://github.com/adam-pawelek/llmtranslate/actions/workflows/test.yml)
[![Python package - Publish](https://github.com/adam-pawelek/llmtranslate/actions/workflows/publish.yml/badge.svg)](https://github.com/adam-pawelek/llmtranslate/actions/workflows/publish.yml)
[![Python Versions](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/llmtranslate)](https://pypi.org/project/llmtranslate/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/adam-pawelek/llmtranslate/graph/badge.svg?token=WCQOJC032S)](https://codecov.io/github/adam-pawelek/llmtranslate)
[![Downloads](https://static.pepy.tech/badge/llmtranslate)](https://pepy.tech/project/llmtranslate)
## Overview

llmtranslate is a Python library designed to identify the language of a given text and translate text between multiple languages using OpenAI's GPT-4o. The library is especially useful for translating text containing multiple languages into a single target language.

## Features

- **Language Detection:** Identify the language of a given text in ISO 639-1 format.
- **Translation:** Translate text containing multiple languages into another language in ISO 639-1 format.

## Requirements

To use this library, you must have an OpenAI API key. This key allows the library to utilize OpenAI's GPT-4o for translation and language detection.



## Installation

You can install the llmtranslate library from PyPI:

```bash
pip install llmtranslate
```

## Usage

### Setting the OpenAI API Key

Before using llmtranslate with OpenAI, you need to set your OpenAI API key. You can do this by creating an instance of the TranslatorOpenAI class.

```python
from llmtranslate import TranslatorOpenAI
# Set your OpenAI API key
translator = TranslatorOpenAI(open_ai_api_key="YOUR_OPENAI_API_KEY")

```

### Setting the Azure OpenAI API Key

If you are using Azure's OpenAI services, you need to set your Azure OpenAI API key along with additional required parameters. Use the TranslatorAzureOpenAI class for this.

```python
from llmtranslate import TranslatorAzureOpenAI

# Set your Azure OpenAI API key and related parameters
translator = TranslatorAzureOpenAI(
  azure_endpoint="YOUR_AZURE_ENDPOINT",
  api_key="YOUR_AZURE_API_KEY",
  api_version="YOUR_API_VERSION",
  azure_deployment="YOUR_AZURE_DEPLOYMENT"
)

```


### Language Detection

To detect the language of a given text:

```python
from llmtranslate import TranslatorOpenAI

# Set your OpenAI API key
translator = TranslatorOpenAI(open_ai_api_key="YOUR_OPENAI_API_KEY")

# Detect language
detected_language = translator.get_text_language("Hello world")
if detected_language is not None:
  print(detected_language.ISO_639_1_code)  # Output: 'en'
  print(detected_language.ISO_639_2_code)  # Output: 'eng'
  print(detected_language.ISO_639_3_code)  # Output: 'eng'
  print(detected_language.language_name)  # Output: 'English'

```

> [!IMPORTANT]
> If the translator does not detect any language, it will return None.<br>
> Before using results of translator detection you should check if it returned correct result or None

### Translation

To translate text containing multiple languages into another language:

```python
from llmtranslate import TranslatorOpenAI

# Set your OpenAI API key
translator = TranslatorOpenAI(open_ai_api_key="YOUR_OPENAI_API_KEY")

# Translate text
translated_text = translator.translate("Cześć jak się masz? Meu nome é Adam", "en")
print(translated_text)  # Output: "Hello how are you? My name is Adam"
```


### Full Example

Here is a complete example demonstrating how to use the library:

```python
from llmtranslate import TranslatorOpenAI

# Initialize the translator with your OpenAI API key
translator = TranslatorOpenAI(open_ai_api_key="YOUR_OPENAI_API_KEY")

# Detect language
detected_language = translator.get_text_language("jak ty się nazywasz")
if detected_language is not None:
  print(detected_language.ISO_639_1_code)  # Output: 'pl'
  print(detected_language.ISO_639_2_code)  # Output: 'pol'
  print(detected_language.ISO_639_3_code)  # Output: 'pol'
  print(detected_language.language_name)  # Output 'Polish'

# Translate text
translated_text = translator.translate("Cześć jak się masz? Meu nome é Adam", "en")
print(translated_text)  # Output: "Hello how are you? My name is Adam"

```

## Supported Languages

llmtranslate supports all languages supported by GPT-4o. For a complete list of language codes, you can visit the [ISO 639-1 website](https://localizely.com/iso-639-1-list/).

Here are some of the most popular languages and their ISO 639-1 codes:

- **English**: `en`
- **Spanish**: `es`
- **French**: `fr`
- **German**: `de`
- **Chinese**: `zh`
- **Japanese**: `ja`
- **Korean**: `ko`
- **Portuguese**: `pt`
- **Russian**: `ru`
- **Italian**: `it`
- **Dutch**: `nl`
- **Arabic**: `ar`
- **Hindi**: `hi`
- **Bengali**: `bn`
- **Turkish**: `tr`
- **Polish**: `pl`
- **Swedish**: `sv`
- **Norwegian**: `no`
- **Danish**: `da`
- **Finnish**: `fi`
- **Greek**: `el`
- **Hebrew**: `he`

## Additional Resources

- [PyPI page](https://pypi.org/project/llm_translate/)
- [ISO 639-1 Codes](https://localizely.com/iso-639-1-list/)
- [Github project repository](https://github.com/adam-pawelek/llmtranslate)
- [Documentation](https://llm-translate.com/)

## Authors
- Adam Pawełek  
  - [LinkedIn](https://www.linkedin.com/in/adam-roman-pawelek/)  
  - [Email](mailto:adam.pwk@outlook.com)
  


## License

llmtranslate is licensed under the MIT License. See the LICENSE file for more details.


