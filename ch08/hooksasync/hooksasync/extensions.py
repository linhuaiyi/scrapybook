from scrapy import log, signals
from scrapy.exceptions import DropItem


class HooksasyncExtension(object):
    @classmethod
    def from_crawler(cls, crawler):
        log.msg("HooksasyncExtension from_crawler")
        return cls(crawler)

    def __init__(self, crawler):
        log.msg("HooksasyncExtension Constructor called")

        # connect the extension object to signals
        cs = crawler.signals.connect
        cs(self.engine_started, signal=signals.engine_started)
        cs(self.engine_stopped, signal=signals.engine_stopped)
        cs(self.spider_opened, signal=signals.spider_opened)
        cs(self.spider_idle, signal=signals.spider_idle)
        cs(self.spider_closed, signal=signals.spider_closed)
        cs(self.spider_error, signal=signals.spider_error)
        cs(self.request_scheduled, signal=signals.request_scheduled)
        cs(self.response_received, signal=signals.response_received)
        cs(self.response_downloaded, signal=signals.response_downloaded)
        cs(self.item_scraped, signal=signals.item_scraped)
        cs(self.item_dropped, signal=signals.item_dropped)

    def engine_started(self):
        log.msg("HooksasyncExtension, signals.engine_started fired")

    def engine_stopped(self):
        log.msg("HooksasyncExtension, signals.engine_stopped fired")

    def spider_opened(self, spider):
        log.msg("HooksasyncExtension, signals.spider_opened fired")

    def spider_idle(self, spider):
        log.msg("HooksasyncExtension, signals.spider_idle fired")

    def spider_closed(self, spider, reason):
        log.msg("HooksasyncExtension, signals.spider_closed fired")

    def spider_error(self, failure, response, spider):
        log.msg("HooksasyncExtension, signals.spider_error fired")

    def request_scheduled(self, request, spider):
        log.msg("HooksasyncExtension, signals.request_scheduled fired")

    def response_received(self, response, request, spider):
        log.msg("HooksasyncExtension, signals.response_received fired")

    def response_downloaded(self, response, request, spider):
        log.msg("HooksasyncExtension, signals.response_downloaded fired")

    def item_scraped(self, item, response, spider):
        log.msg("HooksasyncExtension, signals.item_scraped fired")

    def item_dropped(self, item, spider, exception):
        log.msg("HooksasyncExtension, signals.item_dropped fired")

    @classmethod
    def from_settings(cls, settings):
        log.msg("HooksasyncExtension from_settings")
        # This is never called - but would be called if from_crawler()
        # didn't exist. from_crawler() can access the settings via
        # crawler.settings but also has access to everything that
        # crawler object provides like signals, stats and the ability
        # to schedule new requests with crawler.engine.download()


class HooksasyncDownloaderMiddleware(object):
    """ Downloader middlewares *are* middlewares and as a result can do
    everything any middleware can do (see HooksasyncExtension).
    The main thing that makes them different are the process_*() methods"""

    @classmethod
    def from_crawler(cls, crawler):
        log.msg("HooksasyncDownloaderMiddleware from_crawler")
        # Here the constructor is actually called and the class returned
        return cls(crawler)

    def __init__(self, crawler):
        log.msg("HooksasyncDownloaderMiddleware Constructor called")

    def process_request(self, request, spider):
        log.msg(("HooksasyncDownloaderMiddleware process_request "
                "called for %s") % request.url)

    def process_response(self, request, response, spider):
        log.msg(("HooksasyncDownloaderMiddleware process_response "
                "called for %s") % request.url)
        return response

    def process_exception(self, request, exception, spider):
        log.msg(("HooksasyncDownloaderMiddleware process_exception "
                "called for %s") % request.url)


class HooksasyncSpiderMiddleware(object):
    """ Spider middlewares *are* middlewares and as a result can do
    everything any middleware can do (see HooksasyncExtension).
    The main thing that makes them different are the process_*() methods"""

    @classmethod
    def from_crawler(cls, crawler):
        log.msg("HooksasyncSpiderMiddleware from_crawler")
        # Here the constructor is actually called and the class returned
        return cls(crawler)

    def __init__(self, crawler):
        log.msg("HooksasyncSpiderMiddleware Constructor called")

    def process_spider_input(self, response, spider):
        log.msg(("HooksasyncSpiderMiddleware process_spider_input "
                "called for %s") % response.url)

    def process_spider_output(self, response, result, spider):
        log.msg(("HooksasyncSpiderMiddleware process_spider_output "
                "called for %s") % response.url)
        return result

    def process_spider_exception(self, response, exception, spider):
        log.msg(("HooksasyncSpiderMiddleware process_spider_exception "
                "called for %s") % response.url)

    def process_start_requests(self, start_requests, spider):
        log.msg("HooksasyncSpiderMiddleware process_start_requests called")
        return start_requests


class HooksasyncPipeline(object):
    """ Pipelines *are* middlewares and as a result can do
    everything any middlewares can do (see HooksasyncExtension).
    The main thing that makes them different is that they have
    the process_item() method"""

    @classmethod
    def from_crawler(cls, crawler):
        log.msg("HooksasyncPipeline from_crawler")
        # Here the constructor is actually called and the class returned
        return cls(crawler)

    def __init__(self, crawler):
        log.msg("HooksasyncPipeline Constructor called")

    def process_item(self, item, spider):
        if item['name'] == "Hello 1":
            raise DropItem("Not good")
        log.msg(("HooksasyncPipeline process_item() called for "
                "item: %s") % item['name'])
        return item

    # This function overrides the default for Item Pipelines
    def open_spider(self, spider):
        log.msg("HooksasyncPipeline spider_opened")

    # This function overrides the default for Item Pipelines
    def close_spider(self, spider):
        log.msg("HooksasyncPipeline spider_closed")
