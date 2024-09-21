import os
from datetime import date, time, datetime
import datetime
from pathlib import Path
import random


def main():
    current_directory = Path.cwd()
    print("Current Dir: ", current_directory)

    total_day = int(input("Enter total number of days: "))
    commit_frequency = int(input("Enter commit frequency (commits per day): "))
    repo_link = input("Enter repo link: ")

    tl = total_day  # Time in days
    ctr = 1

    now = datetime.now()

    f = open(f"{current_directory}/commit.txt", "w")
    os.system("git config user.name")
    os.system("git config user.email")
    os.system("git init")

    pointer = 0

    while tl > 0:
        ct = random.randint(1, commit_frequency)
        while ct > 0:
            f = open("commit.txt", "a+")
            l_date = now + datetime.timedelta(days=-pointer)
            formatdate = l_date.strftime("%Y-%m-%d")
            f.write(f"gitgen commit {ctr}: {formatdate}\n")
            f.close()
            os.system("git add .")
            os.system(f"git commit --date=\"{formatdate} 12:15:10\" -m \"gitgen commit {ctr}\"")
            print(f"gitgen commit {ctr}: {formatdate}")
            ct-=1
            ctr+=1
        pointer+=1
        tl-=1

    os.system(f"git remote add origin {repo_link}")
    os.system("git branch -M main")
    os.system("git push -u origin main -f")

if __name__ == "__main__":
    main()
