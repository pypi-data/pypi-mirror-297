# typoglycemia

## Introduction

Typoglycemia is a CLI tool that displays the given text with a typoglycemia effect. The typoglycemia effect involves keeping the first and last letters of a word in place while shuffling the internal letters randomly.

## Installation

```console
pip install typoglycemia
```

## API Usage

```bash
>>> import typoglycemia

>>> typoglycemia.make_typoglycemia('Hello World')
'Hlelo Wrold'

>>> typoglycemia.make_typoglycemia('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
'Lroem isupm dloor sit aemt, cnosetcuter aidipcsing elit.'
```

## Command Line Usage

```bash
$ typoglycemia -t "Hello World"
Hlelo Wrold

$ typoglycemia -t "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
Lroem isupm dloor sit aemt, cnosetcuter aidipcsing elit.
```

## Contributing

[![Contributors](https://contrib.rocks/image?repo=hooli-dev/typoglycemia&columns=5)](https://github.com/hooli-dev/typoglycemia/graphs/contributors)
