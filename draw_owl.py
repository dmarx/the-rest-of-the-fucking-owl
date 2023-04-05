import os
import openai
from omegaconf import OmegaConf

# Load config from config.yaml
CONFIG_FILE = "config.yaml"
config = OmegaConf.load(CONFIG_FILE)

# Extract variables from config
model_name = config.model_name
prompt_extension = config.prompt_extension
target_extension = config.target_extension
commit_message_tag = config.commit_message_tag
#commit_message_prefix = config.commit_message_prefix
#repo_name = config.repo_name
branch_name = config.branch_name

# Set up OpenAI API
#openai.api_key = config.api_key

DEFAULT_SYSTEM_PROMPT = (
    "You are an experienced staff software engineer who writes perfect code. "
    "Your code is concise, self-explanatory, modular, scalable, and generally demonstrates best practices. "
    "You prefer python. Your python code is always fully type hinted and has docstrings formatted for generating documentation. "
    "Your projects include full test coverage. Pytest is your prefferred testing framework. "
    "You use github actions for ci/cd automation. "
)
DEFAULT_USER_TEMPLATE = (
    "you are presented with the following incomplete document. "
    "<document>\n{text}\n</document>\n"
    "respond with the completed document. "
    "do not acknowledge me or my inquiry. "
    "respond only with perfect, working code and/or documentation. "
)

def generate_code_completion(prompt: str) -> str:
    """
    Generate code completion using OpenAI's Codex model.

    Args:
        prompt (str): The prompt to generate code completion for.

    Returns:
        str: The generated code completion.
    """

    completions = openai.ChatCompletion.create(
        model=model_name,
        #prompt=prompt,
        max_tokens=2048,
        messages=[
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": DEFAULT_USER_TEMPLATE.format(text=prompt)},
        ],
    )
    return completions.choices[0]['message']['content'].strip()


def process_file(file_path: str) -> None:
    """
    Process a file by generating code completion for the prompts in the file.

    Args:
        file_path (str): The file path of the file to process.
    """
    with open(file_path, "r") as file:
        prompts = file.read().split("\n")
    for prompt in prompts:
        if not prompt:
            continue
        completed_code = generate_code_completion(prompt)
        target_file = os.path.splitext(file_path)[0] + target_extension
        with open(target_file, "a") as f:
            f.write(completed_code + "\n")


if __name__ == "__main__":
    # Read config file
    config = OmegaConf.load(CONFIG_FILE)

    # Extract variables from config
    model_name = config.model_name
    prompt_extension = config.prompt_extension
    target_extension = config.target_extension
    commit_message_tag = config.commit_message_tag
    #commit_message_prefix = config.commit_message_prefix
    #repo_name = config.repo_name
    branch_name = config.branch_name

    # Process each file with prompt extension
    for file_name in os.listdir():
        if file_name.endswith(prompt_extension):
            process_file(file_name)

    # Commit and push changes
    os.system(f"git checkout -b {config.branch_name}")
    os.system("git add .")
    os.system("git commit -m 'LLM autocompletion'")
    os.system(f"git push -u origin {config.branch_name}")

    print(f"Code completion completed and changes pushed to branch {config.branch_name}")
