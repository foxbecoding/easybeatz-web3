import pytest
from moods.models import Mood

@pytest.fixture
def default_mood(db):
    """Fixture to create a test mood."""
    return Mood.objects.create(
        name="Chill",
    )
