class ProviderError(RuntimeError):
    pass


class ProviderConfigurationError(ProviderError):
    pass


class ProviderNetworkDisabled(ProviderError):
    pass
