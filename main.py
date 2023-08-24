from utils import BIST, Shares, Filter, get, sleep

bist = BIST()

@bist.on_filter
async def notify(share: Shares, filter: Filter):
    print("%s hissesi için %s fiyat hedefine ulaşıldı." % (share.stock, filter.price_target))
    
@bist.on_filter
async def telegram_notify(share: Shares, filter: Filter):
    req = get("https://api.telegram.org/bot<your_api_token>/sendMessage?chat_id=<your_id>&text=%s" % ("%s hissesi için %s fiyat hedefine ulaşıldı." % (share.stock, filter.price_target)))
    await sleep(3)
    
bist.run()