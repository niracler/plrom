# shellcheck shell=dash

CHARACTER_ID=57410
fp="README.md"
content="$(< README.md jq -Rs -r '@json')"

flag=0
while read -r line; do
    if [ "$line" = "<!--" ] || [ "$line" = "-->" ]; then
        if [ "$flag" -eq 0 ]; then
            flag=1
            elif [ "$flag" -eq 1 ]; then
            break
        fi
    else
        if [ "$flag" -eq 1 ]; then
            key="$(printf "%s\n" "$line" | awk '{print $2}')"
            
            case "$key" in
                title:)
                    title="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}')"
                    eval "title=\"$title\""
                ;;
                summary:)
                    summary="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}')"
                    eval "summary=\"$summary\""
                ;;
                cover:)
                    cover="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}')"
                    eval "cover=\"$cover\""
                ;;
                slug:)
                    slug="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}')"
                    eval "slug=\"$slug\""
                ;;
                tags:)
                    tags="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}' | jq -c '.[]' | tr '\n' ',' | sed 's/,$//')"
                ;;
                note_id:)
                    note_id="$(printf "%s\n" "$line" | awk -F ': ' '{print $2}')"
                    eval "note_id=\"$note_id\""
                ;;
            esac
        fi
    fi
done < "$fp"

if [ -z "$title" ] || [ -z "$summary" ] || [ -z "$cover" ] || [ -z "$slug" ] || [ -z "$tags" ]; then
    echo "Error: Missing required metadata。"
    exit 1
fi

if [ -n "$note_id" ]; then
    echo Update note
    curl -X POST -v \
        -H "Authorization: Bearer $XLOG_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
                "metadata": {
                    "tags": ["post", '"$tags"'],
                    "type": "note",
                    "title": "'"$title"'",
                    "content": '"$content"',
                    "summary": "'"$summary"'",
                    "sources": ["xlog"],
                    "date_published": "2024-03-04T00:00:00.000Z",
                    "attributes": [{
                        "value": "'"$slug"'",
                        "trait_type": "xlog_slug"
                    }],
                    "attachments": [{
                        "name": "cover",
                        "address": "'"$cover"'",
                        "mime_type": ""
                    }]
                }
        }' \
        "https://indexer.crossbell.io/v1/siwe/contract/characters/$CHARACTER_ID/notes/${note_id}/metadata"
else
    echo Create note
    echo ....
fi
