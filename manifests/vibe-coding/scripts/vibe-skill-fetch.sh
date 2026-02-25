#!/bin/bash
# vibe-skill-fetch: 快捷调用 skill-seekers

if [ -z "$1" ]; then
    echo "Usage: vibe-skill-fetch <URL_OR_REPO> [NAME]"
    exit 1
fi

SOURCE=$1
NAME=${2:-"new-skill"}

# 检查是否是 GitHub 仓库
if [[ $SOURCE == *"github.com"* ]]; then
    REPO=$(echo $SOURCE | sed 's/.*github.com\///')
    echo "Fetching skill from GitHub repo: $REPO..."
    skill-seekers github --repo "$REPO" --name "$NAME"
else
    echo "Scraping skill from URL: $SOURCE..."
    skill-seekers scrape --url "$SOURCE" --name "$NAME"
fi

echo "Skill fetched. To install to Cursor, run:"
echo "skill-seekers install-agent output/$NAME/ --agent cursor"
