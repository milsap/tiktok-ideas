from apify_client import ApifyClient

APIFY_TOKEN = "PON_AQUI_TU_TOKEN"  # https://apify.com → Settings → Integrations

def extraer(video_url: str, limite: int = 200) -> list[dict]:
    client = ApifyClient(APIFY_TOKEN)
    run = client.actor("clockworks/tiktok-comments-scraper").call(run_input={
        "postUrls": [video_url],
        "commentsPerPost": limite,
        "includeReplies": False,
    })
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
    return [{"usuario": i.get("author",{}).get("username",""),
             "texto": i.get("text",""),
             "likes": i.get("likesCount",0)} for i in items]
