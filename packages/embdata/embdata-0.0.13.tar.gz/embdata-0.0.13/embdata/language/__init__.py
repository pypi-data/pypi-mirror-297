
class Language(str):  # noqa: SLOT000
  def embed(self):
    return self + " is embedded"

  def tokenize(self) -> None:
    # TODO: use sentence transformers to tokenize the language
    pass
