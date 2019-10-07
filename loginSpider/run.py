from scrapy import cmdline


name = 'login_spider'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
