import re

from pydantic import ValidationError
from ruyaml import YAML

from lopt.errors import NoCodeFoundError, ParseModelError
from lopt.models import Language, ModelT


def parse_multi_line(s: str, *, lang: Language) -> str | None:
    if match := re.search(rf"```(?:{re.escape(lang)})?(.+)```", s, re.DOTALL):
        return match[1]

    return None


def parse_inlne(s: str) -> str | None:
    if match := re.search(r"`(.+)`", s):
        return match[1]

    return None


def parse(s: str, *, lang: Language) -> str:
    if multi_line := parse_multi_line(s, lang=lang):
        return multi_line

    if inline := parse_inlne(s):
        return inline

    raise NoCodeFoundError(data=s, lang=lang)


def parse_str(s: str, *, lang: Language, model: type[ModelT]) -> ModelT:
    if lang == "json":
        return model.model_validate_json(s)

    yaml = YAML(typ="safe")
    obj = yaml.load(s)  # pyright: ignore[reportUnknownMemberType]

    return model.model_validate(obj)


def parse_model(
    s: str,
    *,
    lang: Language,
    model: type[ModelT],
    ignore_errors: bool = True,
) -> ModelT | None:
    try:
        data_str = parse(s, lang=lang)
    except NoCodeFoundError:
        data_str = s.strip("`")

    if data_str:
        try:
            return parse_str(data_str, lang=lang, model=model)

        except ValidationError as error:
            if not ignore_errors:
                raise ParseModelError(model=model, data=data_str) from error

            return None

    if ignore_errors:
        return None

    msg = "Data string is empty or no code found"
    raise ParseModelError(msg, model=model, data=s)
