import datetime
import time


def main():
    for i in ["today", "weekly", "monthly"]:
        execute(i)

def execute(i):
    dt_now = datetime.datetime.now()
    current_date = dt_now.strftime('%Y-%m-%d_%H-%M-%S-%f')
    data = i + "_trend.txt"
    o = open(data, "r")
    lines = o.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    n = 0
    no = 0
    while n < len(lines):
        one = lines[n]
        two = lines[n+1]
        three = lines[n+2]
        four = lines[n+3]
        five = lines[n+4]
        six = lines[n+5]
        no = no + 1


        if three == "new":
            n = n + 6
            user = one
            title = two
            new = True
            time = five
            like = six
        else:
            n = n + 5
            user = one
            title = two
            new = False
            time = four
            like = five

        result = "{" + "id: " + str(no) + ", user: " + """ + user + """ + ", title: " + """ + title + """ + ", new: " + str(new) + ", time: " + """ + time + """ + ", like: " + str(like) + "}"
        print(result)


if __name__ == "__main__":
    main()