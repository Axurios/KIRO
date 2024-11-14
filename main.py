import gui

if __name__ == "__main__":
    print("ok")
    gui.test()


def swap(sequence, i, j):
    sequence[i], sequence[j] = sequence[j], sequence[i]