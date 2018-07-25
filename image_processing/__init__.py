import io
import logging
import PIL
import time


def make_thumbnail(self, body, target_size):
    with io.BytesIO(body) as fp:
        with Image.open(fp) as img:
            logging.info('beginning image resizing')

            start = time.perf_counter()
            wpercent = (target_size / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)

            with io.BytesIO() as fp_ret:
                img.save(fp_ret, 'JPEG', **params)
                fp_ret.seek(0)
                end = time.perf_counter()
                logging.info(f'created thumbnail in {end-start} seconds')
                return fp_ret.read()
