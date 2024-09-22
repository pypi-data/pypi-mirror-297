from lopt.models import Language, ModelT


class LoptError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class NoCodeFoundError(LoptError):
    def __init__(
        self,
        msg: str = "No code found",
        *,
        lang: Language,
        data: str,
    ) -> None:
        super().__init__(msg)
        self.lang = lang
        self.data = data

    def __str__(self) -> str:
        return f"{self.msg}, lang: {self.lang}, data: {self.data}"


class ParseModelError(LoptError):
    def __init__(
        self,
        msg: str = "Failed to parse model",
        *,
        model: type[ModelT],
        data: str,
    ) -> None:
        super().__init__(msg)
        self.model = model
        self.data = data

    def __str__(self) -> str:
        return f"{self.msg}, model: {self.model.__name__}, data: {self.data}"
