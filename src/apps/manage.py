import argparse


def runserver():
    from app import api
    import uvicorn
    uvicorn.run(
        app=api,
        host="0.0.0.0",
        port=9080,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )


# コマンドライン引数パーサー
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# サブコマンド: runserver, WEBアプリケーション起動
parser_runserver = subparsers.add_parser("runserver")
parser_runserver.set_defaults(handler=runserver)


if __name__ == "__main__":
    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler()
    else:
        parser.print_help()
