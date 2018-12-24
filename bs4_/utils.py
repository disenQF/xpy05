def retrieve_charset(content_type):  # 提取content_type和字符串
    charset = None

    # ''.index(substr)如果没有查找到则会抛出ValueError
    # ''.find(substr) 如果没有查找到则会返回-1，不会抛出异常
    if content_type.find(';') > 0:
        content_type, charset = tuple(content_type.split(';'))
        charset = charset.split('=')[-1]  # 获取charset=utf-8 中字符集

    return content_type, charset


def decode_html(bytes, content_type):
    # 将字节数组转成content_type中指定的字符集的字符串
    ctype, charset = retrieve_charset(content_type)
    if charset:
        return bytes.decode(charset)

    return bytes.decode()
