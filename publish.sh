# shellcheck shell=dash

content="$(< README.md jq -Rs -r '@json')"
version="${1:?version is required}"

git tag "$version"
git push origin "$version"

curl -X POST \
    -H "Authorization: Bearer $XLOG_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
            "metadata": {
                "tags": ["post", "life"],
                "type": "note",
                "title": "人 X 社区 X 物 - '"$version"'",
                "content": '"$content"',
                "summary": "一个人所用的工具以及关注的事情，很大程度上定义了他是谁",
                "sources": ["xlog"],
                "date_published": "2024-03-04T00:00:00.000Z",
                "attributes": [{
                    "value": "plrom",
                    "trait_type": "xlog_slug"
                }],
                "attachments": [{
                    "name": "cover",
                    "address": "https://ipfs.crossbell.io/ipfs/QmR5AtZLDJqXUgn9gcYLKbcnRtGA6QtA14Xrzh6PuTsM9c",
                    "mime_type": ""
                }]
            }
    }' \
    "https://indexer.crossbell.io/v1/siwe/contract/characters/$CHARACTER_ID/notes/273/metadata"
