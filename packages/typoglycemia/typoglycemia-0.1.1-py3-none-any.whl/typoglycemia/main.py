import random
import argparse
import re

__version__ = "0.1.1"


def shuffle(word):
    if len(word) <= 3:
        return word

    parts = re.split(r'([_\W]+)', word)
    shuffled_parts = [
        part if len(part) <= 3 or not part.isalnum() else part[0] + ''.join(random.sample(part[1:-1], len(part[1:-1]))) + part[-1]
        for part in parts
    ]

    return ''.join(shuffled_parts)


def make_typoglycemia(sentence):
    if not sentence:
        return ""

    return ' '.join(shuffle(word) for word in sentence.split())


def cli() -> int:
    parser = argparse.ArgumentParser(
        prog="Typoglycemia",
        description="CLI tool to display text with Typoglycemia effect.",
    )

    parser.add_argument("-t", "--text", required=True, help="Text to process.")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    args = parser.parse_args()

    typoglycemia = make_typoglycemia(args.text)
    print(typoglycemia)
    return 0


if __name__ == "__main__":
    cli()
