import feedparser
import re

# Medium RSS Feed URL
FEED_URL = "https://medium.com/feed/@karollismarmokas"

# Fetch and parse the feed
feed = feedparser.parse(FEED_URL)

# Markdown formatted string for updating README
markdown_content = "### Blog posts\n\n"

# Iterate over the feed entries (blog posts)
for entry in feed.entries[:3]:  # Limiting to 3 posts
    # Extract the title, link, and potential image URL from the post
    title = entry.title
    link = entry.link

    # Use regex to extract image from content (if available)
    content = entry.summary
    image_match = re.search(r'<img.*?src="(.*?)"', content)
    image_url = image_match.group(1) if image_match else None

    # Build the Markdown block for this post
    markdown_content += f"- **[{title}]({link})**\n"
    if image_url:
        markdown_content += f"  \n![{title}]({image_url})\n\n"

# Save the output to README.md
with open("README.md", "r") as file:
    readme_content = file.read()

# Replace the blog post section
new_content = re.sub(
    r"(?s)(<!-- BLOG-POST-LIST:START -->)(.*?)(<!-- BLOG-POST-LIST:END -->)",
    f"\\1\n{markdown_content}\n\\3",
    readme_content
)

# Write the updated README
with open("README.md", "w") as file:
    file.write(new_content)
