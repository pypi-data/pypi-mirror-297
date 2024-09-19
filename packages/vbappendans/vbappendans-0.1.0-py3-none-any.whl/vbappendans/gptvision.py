import click
import os
import sys

from rich.console import Console

from .functions import process_images
from .prompts import switch_prompt
from .choice_option import ChoiceOption


@click.command(
    help="Process images using OpenAI's GPT-4 Vision model and extract the response."
)
@click.option(
    "-i",
    "--image",
    type=click.Path(exists=True),
    required=True,
    multiple=True,
    help="Path to the image file",
)
@click.option(
    "-p",
    "--prompt",
    cls=ChoiceOption,
    type=click.Choice(
        [
            "answer_dict",
            "prompt",
        ],
        case_sensitive=False),
    prompt=True,
    default=1,
    show_default=True,
    help="Prompt to use for the completion",
)
@click.option(
    "-m",
    "--model",
    cls=ChoiceOption,
    type=click.Choice(
        [
            "gpt-4o",
            "gpt-4o-2024-08-06",
            "gpt-4-turbo",
            "gpt-4-turbo-preview",
            "gpt-4-vision-preview",
            "gpt-4o-mini"
        ],
        case_sensitive=False),
    prompt=True,
    default=2,
    show_default=True,
    help="Prompt to use for the completion",
)
@click.option(
    "--max-tokens",
    type=int,
    default=2000,
    show_default=True,
    help="The maximum number of tokens to generate.",
)
def imgtojson(image, prompt, model, max_tokens):
    """
    Process images using OpenAI's GPT-4 Vision and extract LaTeX code from the response.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        console = Console()
        console.print(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.", style="bold red")
        sys.exit(1)

    if prompt == "prompt":
        prompt = click.prompt("Please enter your custom prompt", type=str)

    prompt = switch_prompt(prompt)
    process_images(image, prompt, model, api_key, max_tokens)
    # mark_answer(range, answer_key, problem_input_pattern)
