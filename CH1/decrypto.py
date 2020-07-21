import crypt


def main():
    passfile = open('passwords.txt')
    for line in passfile.readlines():
        print(line)



if __name__ == '__main__':
    main()
