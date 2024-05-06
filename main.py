"""
This quick script will get all posts from a Blogger blog, and save them in JSON files.
A nice person needed help backing up his blog, so I wrote this for him.
Use it to backup your blog posts.
Get API Key from here: https://developers.google.com/blogger/docs/3.0/using#APIKey
Get your blog id by searching for BlogID in your blog's HTML source code.
"""

import httpx
import json

KEY = "YOUR_API_KEY"
BLOG_ID = "YOUR_BLOG_ID"


def main():
    counter = 1
    params = {
        "maxResults": 100,
        "key": KEY,
    }
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"

    with httpx.Client() as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        d = r.json()
        with open(f"out/posts-{counter}.json", "w") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        nextPageToken = d.get("nextPageToken")

        while nextPageToken:
            counter += 1
            params["pageToken"] = nextPageToken
            r = client.get(url, params=params)
            r.raise_for_status()
            d = r.json()
            with open(f"out/posts-{counter}.json", "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            nextPageToken = d.get("nextPageToken")
            print(f"Page {counter} done.")

    print("All done.")


if __name__ == "__main__":
    main()
