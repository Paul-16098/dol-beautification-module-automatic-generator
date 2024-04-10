const { getOctokit, context } = require('@actions/github');

// Octokit.js
// https://github.com/octokit/core.js#readme
const octokit = new Octokit({
  auth: "${{ secrets.TOKEN }}"
})

const releases = await octokit.rest.repos.listReleases({
      owner: context.repo.owner,
      repo: context.repo.repo,
    });
const release = releases.data.find((r) => r.tag_name === "last-Release");


await octokit.request('DELETE /repos/Paul-16098/dol-beautification-module-automatic-generator/releases/{release_id}', {
        owner: context.repo.owner,
        repo: context.repo.repo,
        release_id: release.id,
  headers: {
    'X-GitHub-Api-Version': '2022-11-28'
  }
})