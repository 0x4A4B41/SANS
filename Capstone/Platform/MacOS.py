try:
    import objc
    objc.loadBundle ('CoreWLAN', globals(),
                     bundle_path='/System/Library/Frameworks/CoreWLAN.framework')

    class MacOS:
        GUEST_NETWORKS = defaults.GUEST_NETWORKS
        GUEST_PSKS = defaults.GUEST_PSKS

        def __init__(self):
            self.RegisterMetadataForSelector('scanForNetworksWithName:error:', 2)
            self.RegisterMetadataForSelector('setPower:error', 2)
            self.RegisterMetadataForSelector('associateToNetwork:password:forceBSSID:remember:error', 5)
            del self.RegisterMetadataForSelector

        def RegisterMetadataForSelector(self, selector, error_arg_num):
            objc.registerMetaDataForSelector(
                'CWInterface', selector,
                {'arguments': {error_arg_num + 1: {'type_modifier': 'o'}}})

except ImportError:
    print("error importing MacOS libs")
    raise

