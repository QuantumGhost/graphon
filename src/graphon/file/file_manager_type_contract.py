from graphon.nodes.protocols import FileManagerProtocol

from .file_manager import FileManager


def _assert_file_manager(file_manager: FileManager) -> FileManagerProtocol:
    return file_manager
