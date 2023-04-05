# the-rest-of-the-fucking-owl

🚧 **WORK IN PROGRESS** 🚧

![](https://i.imgur.com/RadSf.jpg)


### Trigger an LLM in your CI/CD to auto-complete your work

1. Write files with incomplete content. Save them with the extension `.llm_prompt`.
2. Conclude the commit message with the trigger word: "4LLM"
3. Your LLM of choice completes your work and pushes it to a PR for review!


# Setup

1. Create a new github repository, using this as a [template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).
2. Configure your `OPENAI_API_KEY` as a secret on the repository: https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository
3. Make sure `Settings > Actions > General` is configured thusly:
  - Actions permissions: Allow all actions and reusable workflows
  - Workflow permissions: Read and write permissions
  - Workflow permissions: Allow Github Actions to create and approve pull requests 

# Use

Write skeleton code files and name them with the file extension `.llm_prompt`

When you push a commit ending with a particular trigger word in the commit message -- `4LLM` by default -- github actions will run a script that sends the files to an LLM to be fleshed out. 

The files generated by the LLM will automatically be pushed to a new branch and proposed in a PR.

A sample `.llm_prompt` is included. You can test that you've configured configured everything properly by creating a new commit containing the trigger word.  
Click on the "Actions" tab: if you see a green check mark, that means the workflow ran successfully. You should be able to review the suggested changes in the "Pull Requests" tab.

# Related Projects

* https://github.com/irgolic/AutoPR
* https://github.com/biobootloader/wolverine
