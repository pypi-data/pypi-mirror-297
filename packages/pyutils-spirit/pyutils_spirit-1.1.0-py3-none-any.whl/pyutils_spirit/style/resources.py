# @Coding: UTF-8
# @Time: 2024/9/22 0:27
# @Author: xieyang_ls
# @Filename: resources.py
from time import sleep

from pyutils_spirit.style.color import RESET


class Resources:
    __spirit_banner = """
     ░█████████              ░███              ░█████         ░███████████
    ░███░░░░░███             ░░░               ░░███          ░█░░░███░░░█
    ░███    ░░░   ░███████  ░████  ░████████    ░███          ░   ░███  ░
    ░░█████████  ░░███░░███ ░░███  ░░███░░███   ░███              ░███
     ░░░░░░░░███  ░███ ░███  ░███   ░███ ░░░    ░███              ░███
     ███    ░███  ░███ ░███  ░███   ░███        ░███              ░███
    ░░█████████   ░███████  ░█████ ░█████      ░█████ ░█████████ ░█████
                  ░███
                  ░███
                 ░█████
     :: SpirI_T Utils ::                                          (v1.1.0)
                                                     
    """

    __websocket_banner = """
    ░█████  ░███  ░█████         ░█████      ░█████████                      ░█████                 ░█████
    ░░███   ░███  ░░███          ░░███       ███░░░░░███                     ░░███                  ░░███
     ░███   ░███   ░███  ░██████  ░███████  ░███    ░░░   ░██████   ░██████   ░███░█████  ░██████  ░███████
     ░███   ░███   ░███ ░███░░███ ░███░░███ ░░█████████  ░███░░███ ░███░░███  ░███░░███  ░███░░███ ░░░███░
     ░░███  █████  ███  ░███████  ░███ ░███  ░░░░░░░░███ ░███ ░███ ░███ ░░░   ░██████░   ░███████    ░███
      ░░░█████░█████░   ░███░░░   ░███ ░███  ███    ░███ ░███ ░███ ░███  ███  ░███░░███  ░███░░░     ░███ ███
        ░░███ ░░███     ░░██████  ████████  ░░█████████  ░░██████  ░░██████   ████ █████ ░░██████    ░░█████
     :: WebSocket Server ::                                                                           (v1.1.0)
     
    """

    def set_spirit_banner(self, spirit_banner):
        self.__spirit_banner = spirit_banner

    def set_websocket_banner(self, websocket_banner):
        self.__websocket_banner = websocket_banner

    def draw_spirit_banner(self, timeout: float = 0.2, color: str = RESET):
        for text_line in self.__spirit_banner.splitlines():
            print(f"{color}{text_line}{RESET}")
            sleep(timeout)

    def draw_websocket_banner(self, timeout: float = 0.2, color: str = RESET):
        for text_line in self.__websocket_banner.splitlines():
            print(f"{color}{text_line}{RESET}")
            sleep(timeout)


set_spirit_banner = Resources.set_spirit_banner

set_websocket_banner = Resources.set_websocket_banner

draw_spirit_banner = Resources.draw_spirit_banner

draw_websocket_banner = Resources.draw_websocket_banner
