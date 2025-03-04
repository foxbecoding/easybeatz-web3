import pytest
from genres.models import Genre

@pytest.fixture
def default_genre(db):
    """Fixture to create a test genre."""
    return Genre.objects.create(
        name="Test Genre",
    )
