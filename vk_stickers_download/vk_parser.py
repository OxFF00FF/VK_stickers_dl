from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests


def vk_stickers_dl(workers: int = 1):
    # https://vk.com/sticker/1-1-512
    # https://vk.com/sticker/1-21920-512

    out_dir = Path(__file__).parent.parent / 'data' / 'stickers'
    out_dir.mkdir(exist_ok=True, parents=True)
    print(f"Output Dir: {out_dir}")

    def download_sticker(i: int):
        url = f'https://vk.com/sticker/1-{i}-512'
        file_path = out_dir / f'{i}.png'

        try:
            with requests.Session() as session:
                response = session.get(url, timeout=10)
                response.raise_for_status()

                file_path.write_bytes(response.content)

            print(f'{i}: {url} OK')

        except requests.RequestException as e:
            print(f'{i}: ERROR: {e}')

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(download_sticker, range(1, 30001))


if __name__ == '__main__':
    vk_stickers_dl()
