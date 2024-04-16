from pathlib import Path
from random import randint

current = Path.cwd()
structure = Path("structure")
target_directory = current.joinpath(structure).resolve()


def create_folder_and_files():
    """ Creates folder structure in current directory and if it exists recreates it.
    Creates randomly from 3 to 5 .txt, .jpg and .zip files.
    Writes a random integer number from 1 to 10 into each .txt file."""
    structure.mkdir(exist_ok=True)
    for suffix in ("txt", "jpg", "zip"):
        files = [f"file{i}.{suffix}" for i in range(randint(3, 5))]
        for file in files:
            f = structure.joinpath(file)
            f.touch()
            if suffix == "txt":
                f.write_text(str(randint(1, 10)))


def count_files():
    txt_ans = 0
    zip_ans = 0
    jpeg_ans = 0
    sum_ans = 0
    for file in target_directory.iterdir():
        match file.suffix.lower():
            case ".txt":
                txt_ans += 1
                sum_ans += int(file.read_text())
            case ".zip":
                zip_ans += 1
            case ".jpg" | ".jpeg":
                jpeg_ans += 1
    return txt_ans, zip_ans, jpeg_ans, sum_ans


if __name__ == '__main__':
    create_folder_and_files()
    txt_ans, zip_ans, jpeg_ans, sum_ans = count_files()
    print(txt_ans, zip_ans, jpeg_ans, sum_ans)
