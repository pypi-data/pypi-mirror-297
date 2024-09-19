import click


from .append_ans import mark_answer


@click.command(
    help="Process images using OpenAI's GPT-4 Vision model and extract the response."
)
@click.option(
    "-a",
    "--answer-key",
    type=click.Path(exists=True),
    default="answer_key.json",
    show_default=True,
    help="Path to the answer key file",
)
@click.option(
    '-r',
    '--range',
    type=click.Tuple([int, int]),
    default=(1, 1),
    show_default=True,
    help="Problem range to mark the answer, e.g. 1 10",
)
@click.option(
    '-p',
    '--problem-input-pattern',
    type=click.Path(exists=True),
    default="src/src_tex/problem_1.tex",
    show_default=True,
    help="Path to the problem input file pattern",
)
def appendfromjson(answer_key, problem_input_pattern, range):

    mark_answer(range, answer_key, problem_input_pattern)
