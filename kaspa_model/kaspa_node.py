"""
A definition of a "node", a running instance of kaspad program.
Includes add relevant data: ip address, port number, passwords etc.
"""

class KaspaNode:
    def __init__(self, *, conn_name=None, ip_addr:str=None, port_number:int=None, tls:bool=None,
                 username:str=None, password:str=None, cert_file_path=None):
        """
        Initializes a new KaspaNode instance.
        :param ip_addr: Ip address, dotted decimal notation as a string. example: '127.0.0.1'
                        or domain name as str Example: kaspad-0.daglabs.com
        :param port_number: Port number as an integer. Example: 16615
        :param tls: Use tls?  True/False
        :param username: User name as a string. Example:  'mike'
        :param password: password as a string.  Example: '73mnklU%h409'
        :param cert_file_path: full path name: '~/kaspanet/automation_testing/cert_files/rpc.cert'
        """
        self._conn_name = conn_name
        self._ip_addr = ip_addr
        self._port_number = str(port_number)
        self._tls=tls
        if tls:
            self._protocol = 'https://'
        else:
            self._protocol = 'http://'
        self._username = username
        self._password = password
        self._cert_file_path = cert_file_path

    @property
    def cert_file_path(self):
        return self._cert_file_path

    @property
    def updated_url(self):
        ret_url = self._protocol + self._username + ':' + self._password + '@' + \
                  self._ip_addr + ':' + self._port_number

        return ret_url

    def __str__(self):
        show_dictionary = {}
        show_dictionary['protocol'] = self._protocol
        show_dictionary['username'] = self._username
        show_dictionary['password'] = self._password
        show_dictionary['ip_or_dns'] = self._ip_addr
        show_dictionary['port'] = self._port_number
        show_dictionary['cert_file'] = self._cert_file_path
        return self._conn_name + ':' +  str(show_dictionary)


if __name__ == '__main__':
    # test it
    node1 = KaspaNode(conn_name=None, ip_addr='127.0.0.1', port_number=16615, tls=True,
                      username='user', password='pass',
                      cert_file_path='~/kaspanet/automation_testing/cert_files/rpc.cert')
    print(str(node1))