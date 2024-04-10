const { context } = require("@actions/github");
const { Octokit } = require("@octokit/core");

async function deleteRelease() {
  const octokit = new Octokit({
    auth: process.env.TOKEN,
  });

  const releases = await octokit.repos.listReleases({
    owner: context.repo.owner,
    repo: context.repo.repo,
  });
  const release = releases.data.find((r) => r.tag_name === "last-Release");

  await octokit.repos.deleteRelease({
    owner: context.repo.owner,
    repo: context.repo.repo,
    release_id: release.id,
  });
}

deleteRelease();
