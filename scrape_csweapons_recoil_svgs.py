#!/usr/bin/env python

from pathlib import Path
import re
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

URL_REGULAR = r'https://www.csweapons.com/recoil?weapons=Desert%20Eagle,R8%20Revolver,Dual%20Berettas,Five-Seven,Glock-18,P2000,USP-S,P250,CZ75-Auto,Tec-9,MAG-7,Nova,Sawed-Off,XM1014,PP-Bizon,MAC-10,MP7,MP5-SD,MP9,P90,UMP-45,AK-47,AUG,FAMAS,Galil%20AR,M4A4,M4A1-S,SG%20553,M249,Negev,AWP,G3SG1,SCAR-20,SSG%2008&shots=150'
URL_ALTFIRE = r'https://www.csweapons.com/recoil?weapons=R8%20Revolver,Glock-18,USP-S,AUG,FAMAS,M4A1-S,SG%20553,AWP,G3SG1,SCAR-20,SSG%2008&shots=30&alt-modes=true'

_DRIVER = None


def lazy_driver():
    global _DRIVER
    if not _DRIVER:
        _DRIVER = init_silent_driver()
    return _DRIVER


def init_silent_driver() -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(options=options)


def read_or_download(cached_file: Path | str, url: str) -> str:
    cached_path = Path(cached_file)
    if cached_path.exists():
        return cached_path.read_text()
    else:
        print(f'+++ Downloading {url}')
        driver = lazy_driver()
        driver.get(url)
        sleep(5)
        with open(cached_path, "w") as f:
            f.write(driver.page_source)
        return driver.page_source


def filter_relevant_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.body.find(id='app')


def get_spray_patterns(soup: BeautifulSoup):
    divs = soup.find_all('div', ['cs-recoil'])
    sprays = {}
    for d in divs:
        print(d.text)
        spray = get_spray_pattern_from_div(d)
        if not spray:
            continue
        name = re.match(r'\s*(.*?)\s*\d+/.*', d.text).group(1)
        sprays[name] = spray
    return sprays


def get_spray_pattern_from_div(div: BeautifulSoup):
    shots = div.find_all('circle')
    coords = []
    for shot in shots:
        pitch = to_cs_angle(shot['cy'])
        yaw = - to_cs_angle(shot['cx'])
        coords.append((pitch, yaw))
    return coords


def to_cs_angle(x):
    # angle -12 is about -60 y coords (reference: pitch of highest ak shot)
    return 12 * (float(x) / 60)


def spray_to_csv(spray: list) -> str:
    csv = ''
    for s in spray:
        # pitch,yaw
        csv += f'{s[0]:.3f},{s[1]:.3f}\n'
    return csv


def main():
    html_regular = read_or_download('csweapons_com_regular.html', URL_REGULAR)
    html_altfire = read_or_download('csweapons_com_altfire.html', URL_ALTFIRE)
    reg = filter_relevant_soup(html_regular)
    alt = filter_relevant_soup(html_altfire)
    reg_sprays = get_spray_patterns(reg)
    alt_sprays = {(k + ' Alt'): v for k, v in get_spray_patterns(alt).items()}
    sprays = reg_sprays | alt_sprays
    out = Path('out/')
    out.mkdir(exist_ok=True)
    for name, spray in sprays.items():
        path = out / (name.replace(' ', '_') + '.csv')
        csv = spray_to_csv(spray)
        with open(path, 'w') as f:
            f.write(csv)


if __name__ == '__main__':
    main()
