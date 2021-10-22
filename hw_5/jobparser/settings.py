SPIDER_MODULES = ['jobparser.spiders']
NEWSPIDER_MODULE = 'jobparser.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = False
LOG_LEVEL = 'DEBUG'
LOG_FILE = 'log.txt'
ITEM_PIPELINES ={'jobparser.pipeline.JobparserPipeline' : 100}

