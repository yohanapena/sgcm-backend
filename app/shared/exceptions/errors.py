class SGCMError(Exception):
    def __init__(self, detail: str = "Error del sistema SGCM"):
        self.detail = detail
        super().__init__(detail)


class SGCMNotFoundError(SGCMError):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(detail)


class SGCMConflictError(SGCMError):
    def __init__(self, detail: str = "Conflicto en el recurso"):
        super().__init__(detail)


class SGCMValidationError(SGCMError):
    def __init__(self, detail: str = "Validación fallida"):
        super().__init__(detail)


class SGCMAuthError(SGCMError):
    def __init__(self, detail: str = "Error de autenticación"):
        super().__init__(detail)
