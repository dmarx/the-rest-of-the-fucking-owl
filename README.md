# the-rest-of-the-fucking-owl

![](https://i.imgur.com/RadSf.jpg)

trigger an LLM in your CI/CD to auto-complete your work

idea fleshed out here: https://github.com/dmarx/bench-warmers/blob/main/auto-coder.md

working on it here: https://github.com/dmarx/owl-test/

# Setup

1. Create a new github repository, using this as a [template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
2. Configure your `OPENAI_API_KEY` as a secret on the repository: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository

# Use

Write skeleton code files and name them with the file extension `.llm_prompt`

When you push a commit ending with a particular trigger word -- `4LLM` by default -- github actions will run a script that sends the files to an LLM to be fleshed out.
