BOT_NAME = "sheego_spider"

SPIDER_MODULES = ["sheego.spiders"]
NEWSPIDER_MODULE = "sheego.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Playwright Settings
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

DOWNLOADER_MIDDLEWARES = {
    "sheego.middlewares.RotateAgentMiddleware": 540,
    "sheego.middlewares.ShowHeadersMiddleware": 545,
}

SPIDER_MIDDLEWARES = {
   "sheego.middlewares.FilterKeywordMiddleware": 543,
}


# Enable Image Pipeline
ITEM_PIPELINES = {"sheego.pipelines.SheegoImagePipeline": 100,
                  "sheego.pipelines.SheegoPricePipeline": 200,
                  "sheego.pipelines.DuplicatesPipeline": 300,
                  "sheego.pipelines.SavingToMySQLPipeline": 400,
                  }


# Define the folder to store downloaded images
IMAGES_STORE = "images"

# # Define the fields for image URLs and results
# IMAGES_URLS_FIELD = "image_urls"
# IMAGES_RESULT_FIELD = "images"

# # Define thumbnail sizes
# IMAGES_THUMBS = {
#     "small": (50, 50),
#     "big": (270, 270),
# }

# IMAGES_MIN_HEIGHT = 50
# IMAGES_MIN_WIDTH = 50
FEED_EXPORT_ENCODING = 'utf-8'