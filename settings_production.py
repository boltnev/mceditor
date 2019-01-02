from settings import *

DEBUG=False
ALLOWED_HOSTS = ("130.193.58.163",)
MAPS_DST = '/opt/minecraft/world/world/data/'

INSTALL_MAP_SCRIPT = os.path.join(BASE_DIR, 'install_new_map.sh')
