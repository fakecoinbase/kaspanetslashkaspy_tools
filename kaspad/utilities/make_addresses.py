from kaspy_tools.kaspa_model.kaspa_address import KaspaAddress

def make_addresses(count):
    ret_addresses = {}
    for i in range(count):
        addr = KaspaAddress()
        ret_addresses[addr.get_address(prefix='kaspadev')] = addr

    return ret_addresses