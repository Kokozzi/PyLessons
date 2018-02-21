# Run with command:
# `scrapy crawl user_posts -o <filename.json>`

import scrapy

# Create spider class
class UserPostsSpider(scrapy.Spider):
    name = "user_posts"
    # URL to habrahabr's user page
    start_urls = [
        'https://habrahabr.ru/users/pcdesign/posts/',
        # 'https://habrahabr.ru/users/olegbunin/posts/',
    ]

    # Parse user page for posts' links
    def parse(self, response):
        # Extract list of links to posts from user page
        posts_links = response.css('a.post__title_link::attr("href")').extract()
        # Iterate over each post
        for link in posts_links:
            # Parse data from each post page with help of `parse_post` function
            yield response.follow(link, self.parse_post)

        # Get link to next page with user posts
        next_page = response.css('a.arrows-pagination__item-link_next::attr("href")').extract_first()
        if next_page is not None:
            # If next page exists - move there and repeat parsing
            yield response.follow(next_page, self.parse)

    # Parser for habr post page
    def parse_post(self, response):
        # Return dict with author nickname, post title and post content
        yield {
            'author': response.css("a.user-info__nickname::text").extract_first(),
            'title': response.css("span.post__title-text::text").extract_first(),
            "content": response.css("div.post__text").extract_first(),
        }