from setuptools import setup, find_packages # pip install setuptools
from io import open

setup(name="EridaGUI",
      version="0.1", # Версия твоего проекта. ВАЖНО: менять при каждом релизе
      description="Simple GUI",
      author="Tifaney",
      keywords="pypi-AgEIcHlwaS5vcmcCJDY2NTJmNTg5LWUzMDAtNDI1ZC05MDQ5LWRmOWU4ODJjNzIxMwACKlszLCI5ZTliOTdlOC1hYWM4LTRjM2EtYjY3MC00MWE5NmI2ODQ5NWMiXQAABiDv2PlQs58ra8Ht300qBvyJVRFHcTuDgE0QrSmbmaazFg", # Ключевые слова для упрощеннего поиска пакета на PyPi
      packages=find_packages() # Ищем пакеты, или можно передать название списком: ["package_name"]
      )