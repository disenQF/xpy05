from lxml import etree

def parse_xml():
    xml_parse = etree.parse('ips.xml')
    ips = xml_parse.xpath('//ip')
    for ip_selector in ips:
        # print(dir(ip_selector))
        # port = ip_selector.xpath('./@port')[0]
        # ip = ip_selector.xpath('./text()')[0]
        port = ip_selector.get('port')  # 读取属性
        ip = ip_selector.text  # 读取文本
        print(ip, port)


def parse_html():
    with open('xc.html') as f:
        html_parse = etree.HTML(f.read())
        data_tr = html_parse.xpath('//table[@id="ip_list"]/tr[position()>1]')
        for tr in data_tr:
            tr_data = tr.xpath('./td/text()')
            print(''.join(tr_data[0:2]), tr_data[5])


if __name__ == '__main__':
    parse_html()