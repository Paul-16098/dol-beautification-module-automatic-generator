const { context } = require("@actions/github");
const { Octokit } = require("@octokit/core");

async function deleteRelease() {
  const octokit = new Octokit({
    auth: process.env.TOKEN,
  });

  const release = await octokit.request(
    "GET /repos/Paul-16098/dol-beautification-module-automatic-generator/releases/tags/last-Release",
    {
      owner: context.repo.owner,
      repo: context.repo.repo,
      tag: "last-Release",
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
        "content-type": "application/json; charset=utf-8",
      },
    }
  );
  console.log(
    "🚀:快速控制台日誌 ~ file: Delete_Release.js:20 ~ deleteRelease ~ release: ",
    release
  );

  await octokit.request(`DELETE ${release.url}`, {
    owner: context.repo.owner,
    repo: context.repo.repo,
    release_id: release.id,
    headers: {
      "X-GitHub-Api-Version": "2022-11-28",
      "content-type": "application/json; charset=utf-8",
    },
  });
}

deleteRelease();
