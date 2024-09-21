import watcher.sdk

base_url = "https://sensecap.seeed.cc/openapi/"
user = "1ARRTN6MS250ZMZ2"
pwd = "72FB5396127A46FF89D95B8F7C93DC1ACD54752706C344E1B02CD55DBF9B2C1C"
eui = "2CF7F1C96270003D"
result = watcher.sdk.llm_chat("why human want to create robot?", base_url, user, pwd, eui)
print(result.get("data"))
