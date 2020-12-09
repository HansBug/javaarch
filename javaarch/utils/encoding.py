from typing import Optional

import chardet

_DEFAULT_ENCODING = 'utf-8'
_ENCODING_LIST = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']


def auto_decode(data: bytes, encoding: Optional[str] = None) -> str:
    """
    Auto decode binary data to string
    :param data: original binary data
    :param encoding: given encoding (if given, it will only use this encoding format,
                     auto decoding will not be triggered)
    :return: auto decoded string
    """
    if encoding:
        return data.decode(encoding)
    else:
        auto_encoding = chardet.detect(data)['encoding']
        if auto_encoding and auto_encoding not in _ENCODING_LIST:
            _list = _ENCODING_LIST + [auto_encoding]
        else:
            _list = _ENCODING_LIST

        last_err = None
        for enc in _list:
            try:
                return data.decode(encoding=enc)
            except UnicodeDecodeError as err:
                last_err = err

        raise last_err
