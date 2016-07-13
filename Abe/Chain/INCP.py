class Dash(X11Chain):
    def __init__(chain, **kwargs):
        chain.name = 'Inception'
        chain.code3 = 'INCP'
        chain.address_version = '\x66'
        chain.script_addr_vers = '\x70'
        chain.magic = '\x49\x4e\x43\x50"'
        X11PosChain.__init__(chain, **kwargs)

    datadir_conf_file_name = 'inception.conf'
