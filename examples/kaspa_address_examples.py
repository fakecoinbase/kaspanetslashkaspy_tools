from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress

def kaspa_address_demo(prefix):
    addr = KaspaAddress()
    kaspa_str_address = addr.get_address(prefix=prefix)
    print(kaspa_str_address)

def make_list_of_addresses(count=1, prefix='kaspadev'):
    return [KaspaAddress().get_address(prefix=prefix) for i in range(count)]

if __name__ == '__main__':
    kaspa_address_demo('kaspadev')
    print(make_list_of_addresses(count=5, prefix='kaspadev'))

