set TOKEN=secrets.TOKEN
echo "%TOKEN%"

curl -L -H "Accept: application/vnd.github+json" -H "Authorization: Bearer %TOKEN%" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/Paul-16098/dol-beautification-module-automatic-generator/releases/tags/last-Release>output.json
