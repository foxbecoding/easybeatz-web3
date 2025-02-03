from .album_project_service import AlbumProjectService

class AlbumFormService(AlbumProjectService):
    def __init__(self, request_data) -> None:
        super().__init__(request_data)
        self._set_album_form_data()

    def is_valid(self) -> bool:
        return super()._is_album_form_data_valid()
