import feedparser
import re

# Medium RSS Feed URL
FEED_URL = "https://medium.com/feed/@karollismarmokas"

# Fetch and parse the feed
feed = feedparser.parse(FEED_URL)

# Markdown formatted string for updating README
markdown_content = ""

# Helper function to clean and truncate the title
def clean_title(title):
    return title if len(title) <= 60 else title[:57] + "..."

# Helper function to clean the URL by removing unnecessary parameters
def clean_url(url):
    # Use regex to clean unnecessary Medium parameters (remove ? and everything after)
    return re.sub(r'\?.*', '', url)

# Iterate over the feed entries (blog posts)
for index, entry in enumerate(feed.entries[:3]):  # Limiting to 3 posts
    # Extract the cleaned title and URL
    title = clean_title(entry.title)
    link = clean_url(entry.link)

    # For the first post (latest), also extract the image
    if index == 0:
        # Use regex to extract image from content (if available)
        content = entry.summary
        image_match = re.search(r'<img.*?src="(.*?)"', content)
        image_url = image_match.group(1) if image_match else None

        # Build the Markdown block for the latest post with a clickable title
        markdown_content += f"- **[{title}]({link})**\n"
        
        # Display the image after the title if available, and control the size
        if image_url:
            markdown_content += f'<img src="{image_url}" alt="{title}" width="300"/>\n\n'
    else:
        # For other posts, only show the title and cleaned URL
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
