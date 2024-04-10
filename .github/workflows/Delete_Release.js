const { context } = require("@actions/github");
const { Octokit } = require("@octokit/core");

async function deleteRelease() {
  const octokit = new Octokit({
    auth: process.env.TOKEN,
  });

  const release = await octokit.request(
    "GET /repos/Paul-16098/dol-beautification-module-automatic-generator/releases/tags/{tag}",
    {
      owner: context.repo.owner,
      repo: context.repo.repo,
      tag: "last-Release",
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    }
  );

  await octokit.request("DELETE /repos/Paul-16098/dol-beautification-module-automatic-generator/releases/{release_id}", {
    owner: context.repo.owner,
    repo: context.repo.repo,
    release_id: release.id,
    headers: {
      "X-GitHub-Api-Version": "2022-11-28",
    },
  });
}

deleteRelease();
