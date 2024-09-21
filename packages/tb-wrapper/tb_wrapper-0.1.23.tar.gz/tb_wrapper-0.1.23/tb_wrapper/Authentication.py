from tb_wrapper.MainController import MainController


def authentication(tb_url=None, token=None):
    try:
        MainController(tb_url=tb_url, token=token)
    except Exception as e:
        raise
