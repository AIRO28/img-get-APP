# coding:utf-8
import sys
import conachan

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Please enter a search term and the number of retrievals!")
        sys.exit(1)
    keyword = sys.argv[1]
    get_num = int(sys.argv[2])
    cona = conachan.Conachan()
    cona.search_conachan(keyword, get_num)
    exit(0)