import os
import re
import json
import subprocess
# # Answer you provided
# answer_key = {
#     1: 'a',
#     2: 'c',
#     3: 'd',
#     4: 'b',
#     5: 'b',
#     6: 'c',
#     7: 'd',
#     8: 'b',
#     9: 'a',
#     10: 'b',
#     11: 'd',
#     12: 'c',
#     13: 'd',
#     14: 'd',
#     15: 'd',
#     16: 'd'
# }


def mark_answer(problem_range, answer_key, problem_input_pattern):
    with open(answer_key, 'r') as f:
        data = json.load(f)
        answer_key = data['answer_key']

    file_path_basedir = os.path.dirname(problem_input_pattern)
    file_path_basename = os.path.basename(problem_input_pattern)

    # Split the basename into string part and number part
    name_pattern = re.compile(r'([a-zA-Z_]+)(\d+)(\..*)')
    match = name_pattern.match(file_path_basename)

    if not match:
        print(f"Could not parse filename pattern from {file_path_basename}")
        return

    name_prefix, base_number, file_extension = match.groups()
    # base_number = int(base_number)

    for problem_number in range(problem_range[0], problem_range[1] + 1, 1):
        answer = answer_key.get(str(problem_number))
        if not answer:
            print(f"No answer found for problem {problem_number}.")
            continue

        # Construct the filename using the extracted parts
        current_number = problem_number
        file_name = f"{name_prefix}{current_number}{file_extension}"
        file_path = os.path.join(file_path_basedir, file_name)

        try:
            print(f"Current file:")
            subprocess.Popen(
                f'bat -l latex {file_path} --file-name "{file_name}"', shell=True)
            os.system(f'sleep 1')
        except Exception as e:
            print(f"Error: {e}")

        if not os.path.isfile(file_path):
            print(f"File {file_path} does not exist.")
            continue

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = re.compile(
            r'\\begin{tasks}\(\d+\)(.*?)\\end{tasks}', re.DOTALL)
        tasks_match = pattern.search(content)

        if not tasks_match:
            print(f"Tasks environment not found in {file_path}.")
            return

        tasks_content = tasks_match.group(1)

        print(f"Answer key for problem {problem_number}: {answer}")

        # Convert answer letter to index (a=0, b=1, c=2, d=3)
        correct_task_index = ord(answer.lower()) - ord('a')

        def process_task():
            current_index = 0

            def inner_process(match):
                nonlocal current_index
                full_match = match.group(0)
                task_content = match.group(1)
                print(f"Processing task {current_index}: {
                      task_content.strip()}")
                if current_index == correct_task_index:
                    if '\\ans' not in task_content:
                        print(f"Appending \\ans to task {current_index}")
                        result = f"{task_content.strip()} \\ans"
                        # Preserve the original line break and indentation
                        if '\n' in full_match:
                            result += full_match[full_match.index('\n'):]
                    else:
                        print(f"\\ans already present in task {current_index}")
                        result = full_match
                else:
                    print(f"Skipping task {current_index}")
                    result = full_match
                current_index += 1
                return result
            return inner_process

        new_tasks_content = re.sub(
            r'(\\task\s+.*?)(?=\\task|\Z)', process_task(), tasks_content, flags=re.DOTALL)

        if new_tasks_content == tasks_content:
            print("No changes were made to the tasks content.")
        else:
            print("Changes were made to the tasks content.")

        new_content = content.replace(tasks_content, new_tasks_content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"Marked the answer for problem {
              problem_number} in {file_path}.")
        print("Updated content:")
        try:
            subprocess.Popen(
                f'bat -l latex {file_path} --file-name "{file_name}"', shell=True)
            os.system(f'sleep 1')
        except Exception as e:
            print(f"Error: {e}")


# if __name__ == "__main__":
#     import json

#     # Load the answer key from a JSON file
#     with open('answer_key.json', 'r') as f:
#         answer_key = json.load(f)

#     # Iterate through every problem in the answer key
#     for problem_number, answer in answer_key.items():
#         print(f"Processing problem {problem_number}")
#         mark_answer(problem_number)

#     print("All problems processed.")
