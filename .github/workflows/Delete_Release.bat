curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer process.env.TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/releases/tags/last-Release