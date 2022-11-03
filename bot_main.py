# coding: utf8
from Files.keyboards_func import *
from Files.lateral_func import *
from Files.switch_func import *
from Files.main_func import *
from config_bot2 import *
from core_file import *

# -------------------------------------------------------------------------------- #

# کاراکتر
if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=GlobalValues().WEBHOOK_URL_PATH)
    app.on_startup.append(bot_run)
    app.on_shutdown.append(bot_off)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(GlobalValues().WEBHOOK_SSL_CERT, GlobalValues().WEBHOOK_SSL_PRIV)
    web.run_app(app, host="0.0.0.0", port=GlobalValues().port, ssl_context=context)
