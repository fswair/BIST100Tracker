from mentodb import Mento, MentoConnection
from BIST100Tracker.models import ShareModel, FilterModel

connection = MentoConnection("./database/database.db")
mento = Mento(connection)

mento.create("shares", model=ShareModel)
mento.create("filters", model=FilterModel)