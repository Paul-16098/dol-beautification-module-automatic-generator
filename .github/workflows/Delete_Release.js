const { context } = require("@actions/github");
const { Octokit } = require("@octokit/core");

async function deleteRelease() {
  const octokit = new Octokit({
    auth: process.env.TOKEN,
  });

  const release = await octokit.request(
    "GET /repos/{owner}/{repo}/releases/tags/{tag}",
    {
      owner: context.repo.owner,
      repo: context.repo.repo,
      tag: "last-Release",
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    }
  );

  await octokit.repos.deleteRelease({
    owner: context.repo.owner,
    repo: context.repo.repo,
    release_id: release.id,
  });
}

deleteRelease();
