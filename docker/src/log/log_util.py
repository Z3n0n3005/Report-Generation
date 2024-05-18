import time

def log(*contents):
    with open('log.txt', 'a', encoding="utf-8") as f:
        result = ""
        for content in contents:
            # print(str(content))
            result += str(content) + " "

        # print('[', time.strftime("%Y%m%d-%H:%M:%S"), ']', result)

        print('[', time.strftime("%Y%m%d-%H:%M:%S"), ']', result , file=f)
        
if __name__ == "__main__":
    name = 3
    log("text", name)
