

prompt_answer_dict = r"""
Please analyse the image provided, it contains answer key. Extract the answers and format it into python dictionary form. Name this dictionary as "answer_key", then format it into json format.

Reference answer format:
{
    "answer_key": {
        "1": "b",
        "2": "a",
        "3": "c",
        "4": "d"
    }
}
"""


def switch_prompt(value):
    if value == "answer_dict":
        return prompt_answer_dict
    else:
        return value
