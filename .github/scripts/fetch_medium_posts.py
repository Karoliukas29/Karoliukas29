import feedparser
import re

# Medium RSS Feed URL
FEED_URL = "https://medium.com/feed/@karollismarmokas"

# Fetch and parse the feed
feed = feedparser.parse(FEED_URL)

# Markdown formatted string for updating README
markdown_content = ""

# Iterate over the feed entries (blog posts)
for index, entry in enumerate(feed.entries[:3]):  # Limiting to 3 posts
    # Extract the title and link
    title = entry.title
    link = entry.link

    # For the first post (latest), also extract the image
    if index == 0:
        # Use regex to extract image from content (if available)
        content = entry.summary
        image_match = re.search(r'<img.*?src="(.*?)"', content)
        image_url = image_match.group(1) if image_match else None

        # Build the Markdown block for the latest post with an image
        markdown_content += f"- **[{title}]({link})**\n"
        if image_url:
            markdown_content += f"  \n![{title}]({image_url})\n\n"
    else:
        # For other posts, only show the title and link
        markdown_content += f"- **[{title}]({link})**\n\n"

# Read the existing README file
with open("README.md", "r") as file:
    readme_content = file.read()

# Replace the blog post section in the README
new_content = re.sub(
    r"(?s)(<!-- BLOG-POST-LIST:START -->)(.*?)(<!-- BLOG-POST-LIST:END -->)",
    f"\\1\n{markdown_content}\n\\3",
    readme_content
)

# Write the updated content to the README file
with open("README.md", "w") as file:
    file.write(new_content)
