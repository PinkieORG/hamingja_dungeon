
class Dungeon:
    def __init__(self, content: str, name: str = "new_dungeon"):
        self.name = name
        self.content = content

    def __str__(self):
        return self.content

    def save_as(self, output_file: str):
        with open(output_file, "w+") as f:
            f.write(self.content)

    def save(self, output_dir: str):
        self.save_as(output_dir + '//' + self.name + '.txt')

