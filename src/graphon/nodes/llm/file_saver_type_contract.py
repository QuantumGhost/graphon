from .file_saver import FileSaverImpl, LLMFileSaver


def _assert_file_saver(file_saver: FileSaverImpl) -> LLMFileSaver:
    return file_saver
