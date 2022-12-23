# coding: utf8
from whisperbot.switch_func import bot_run, bot_off
from core_file import (
    get_new_configured_app,
    GlobalValues,
    rds,
    ssl,
    web,
    dp,
    db
)
import sys
# -------------------------------------------------------------------------------- #
# کاراکتر
if __name__ == "__main__":
    if len(sys.argv)>1:
        matching = sys.argv[1]
        if matching == "reset":
            rds.delete(db)
        elif matching == "set-support-gp":
            rds.hdel(db, "supchat")
        elif matching == "set-logs-ch":
            rds.hdel(db, "logchat")
        elif matching == "set-linky-ch":
            rds.hdel(db, "linkyCH")
    app = get_new_configured_app(dispatcher=dp, path=GlobalValues().WEBHOOK_URL_PATH)
    app.on_startup.append(bot_run)
    app.on_shutdown.append(bot_off)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(GlobalValues().WEBHOOK_SSL_CERT, GlobalValues().WEBHOOK_SSL_PRIV)
    web.run_app(app, host="0.0.0.0", port=GlobalValues().port, ssl_context=context)