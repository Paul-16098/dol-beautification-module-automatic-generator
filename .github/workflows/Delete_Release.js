const { getOctokit } = require('@actions/github');

const deleteRelease = async () => {
  try {
    const octokit = getOctokit("${{ secrets.TOKEN }}");

    const releases = await octokit.rest.repos.listReleases({
      owner: context.repo.owner,
      repo: context.repo.repo,
    });

    const release = releases.data.find((r) => r.tag_name === "last-Release");
    if (release) {
      await octokit.rest.repos.deleteRelease({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        release_id: release.id,
      });
      console.log("Release deleted successfully.");
    } else {
      console.log("Release not found.");
    }
  } catch (error) {
    console.error("Error deleting release:", error);
  }
};

deleteRelease();
