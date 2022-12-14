from bs4 import BeautifulSoup
import time
import os
import sys
import undetected_chromedriver as uc


one_interval = 60
values = [1000, 1, 3, 5, 10]
names = ["total gain", "last 1 min"]
names.extend([f"last {x} mins" for x in values[2:]])
driver = uc.Chrome(driver_executable_path="/home/eglis/Downloads/chromedriver_linux64/chromedriver", use_subprocess=True)
link = "https://ninjalegends.net/clan_ranking.php?curr_page=1"
driver.get(link)
time.sleep(4)

def get_json(link):
    driver.get(link)
    time.sleep(0.5)
    webp = driver.page_source
    soup = BeautifulSoup(webp, "html.parser")
    return soup.find_all("td")

def get_reps():
    ranks = get_json(link)
    clans = {}
    for i in range(0, len(ranks), 4):
        name = ranks[i].text
        rep = ranks[i+3].text
        clans[name] = int(rep)
    return clans

def table(initial_rep, total_rep, changes):
    sorted_names = list(dict(sorted(total_rep.items(), key=lambda item: item[1], reverse=True)).keys())
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')
    print('|{0:3s} | {1:20s} | {2:10s} | {3:8s} | {4:9s} | {5:6s} | {6:6s} | {7:7s} | {8:7s}'.format("Pos", "Clan Name", "initialRep", "totalRep", "totalGain", f"last {values[1]}", f"last {values[2]}", f"last {values[3]}", f"last {values[4]}"))
    line = "-" * 102
    print(line , sep="", end = "\n")
    for i in range(len(sorted_names)):
        char_name = sorted_names[i]
        print('|{0:3s} | {1:20s} | {2:10d} | {3:8d} | {4:9d} | {5:6d} | {6:6d} | {7:7d} | {8:7d}'.format(f"{i+1}", char_name, initial_rep[char_name], total_rep[char_name], changes["total gain"][char_name], changes[f"last {values[1]} min"][char_name], changes[f"last {values[2]} mins"][char_name], changes[f"last {values[3]} mins"][char_name], changes[f"last {values[4]} mins"][char_name]))
    sys.stdout.flush()

def update_burnlist(burnlist, old_burnlist, burntime, changes):
    change = {}
    for item in burnlist:
        if item not in old_burnlist.keys():
            old_burnlist[item] = 0
            for i in values:
                burntime[i][item] = 0
            for i in names:
                changes[i][item] = 0
        change[item] = burnlist[item] - old_burnlist[item]
    return change, burntime, changes

if __name__ == "__main__":
    start = time.time()
    start_clans = get_reps()
    old_burntime = {}
    for i in values:
        old_burntime[i] = start_clans.copy()
    change = {}
    for name in names:
        change[name] = {k: 0 for k in old_burntime[values[0]]}
    counter = 0
    while True:
        time.sleep(one_interval - (time.time() - start))
        start = time.time()
        counter += 1
        try:
            burnlist = get_reps()
        except:
            burnlist = old_burntime
        for i in range(len(values)):
            if counter % values[i] == 0 or i == 0:
                change_i, old_burntime, change = update_burnlist(burnlist, old_burntime[values[i]], old_burntime, change)
                change[names[i]] = change_i
                if i != 0:
                    old_burntime[values[i]] = burnlist
        table(old_burntime[values[0]], burnlist, change)