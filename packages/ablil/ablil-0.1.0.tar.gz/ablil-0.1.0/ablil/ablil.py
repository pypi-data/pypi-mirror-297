class Ablil:
    def __init__(self, username):
        self.username = username

    def run(self):
        print(f"welcome {self.username}")

if __name__ == '__main__':
    ablil = Ablil('ablil')
    ablil.run()