import snoop


def my_watch(source, value):
    return "caught you {}".format(source), value


snoop.install(watch_extras=my_watch)


@snoop.snoop
def main():
    l = []
    for i in range(10):
        if i % 3:
            l.append(i ** 2)
            print(i ** 2)
        else:
            x = 2

    print("ok!")


if __name__ == "__main__":
    main()
