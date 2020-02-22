from pydiet.services import services
from pydiet.user_interface.ui import UI
import pydiet.data.repository_service as repo
import pydiet.ingredients.ingredient_service as ingredient_service
import pydiet.utility_service as utility_service

# Initialise services
services.add('repo', repo)
services.add('ingredient', ingredient_service)
services.add('ui', UI())
services.add('utils', utility_service)

# Show the UI main menu.
services.ui.run()