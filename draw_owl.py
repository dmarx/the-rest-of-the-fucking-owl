import os
import openai
from omegaconf import OmegaConf

CONFIG_FILE="config.yaml"

DEFAULT_SYSTEM_PROMPT = (
    "You are an experienced staff software engineer who writes perfect code. "
    "Your code is concise, self-explanatory, modular, scalable, and generally demonstrates best practices. "
    "You prefer python. Your python code is always fully type hinted and has docstrings formatted for generating documentation. "
    "Your projects include full test coverage. Pytest is your prefferred testing framework. "
    "You use github actions for ci/cd automation. "
    "A personality quirk of yours is that you rarely speak or express yourself outside of the code and documentation you write. "
    "When you need to communicate, you do so with as few words of your own as are strictly needed."
)
DEFAULT_USER_TEMPLATE = (
    "you are presented with the following incomplete document. "
    "<document>\n{text}\n</document>\n"
    "YOUR ASSIGNMENT IS TO COMPLETELY FILL OUT THE INCOMPLETE DOCUMENT. "
    "respond only with perfect, working code and/or documentation. "
    "do not acknowledge me or my inquiry. Do not provide any caveats, disclaimers, or followup thoughts. "
    "your response should be only the raw text content of the completed document (i.e. please do not add markdown code formatting). "
)

def generate_code_completion(
    prompt: str,
    **kargs
) -> str:
    """
    Generate code completion using OpenAI's Codex model.

    Args:
        prompt (str): The prompt to generate code completion for.

    Returns:
        str: The generated code completion.
    """

    completions = openai.ChatCompletion.create(
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": DEFAULT_USER_TEMPLATE.format(text=prompt)},
        ], **kargs)
    return completions.choices[0]['message']['content'].strip()


def process_file(
    file_path: str,
    prompt_extension: str, 
    target_extension: str,
    completion_kargs: dict,
) -> None:
    """
    Process a file by generating code completion for the prompts in the file.

    Args:
        file_path (str): The file path of the file to process.
    """
    print(file_path)
    with open(file_path, "r") as file:
        #prompts = file.read().split("\n")
        prompt = file.read()
    #for prompt in prompts:
    if not prompt:
        return
    completed_code = generate_code_completion(prompt, **completion_kargs)
    print(completed_code)
    target_file = os.path.splitext(file_path)[0] + target_extension
    print(target_file)
    with open(target_file, "w") as f:
        f.write(completed_code + "\n")


if __name__ == "__main__":
    config = OmegaConf.load(CONFIG_FILE)

    for file_name in os.listdir():
        if file_name.endswith(prompt_extension):
            process_file(
                file_name, 
                prompt_extension=config.prompt_extension, 
                target_extension=config.target_extension,
                completion_kargs=OmegaConf.to_container(config.completion_options),
            )
