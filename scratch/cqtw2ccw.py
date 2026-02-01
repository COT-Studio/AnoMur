

from zipfile import ZipFile
from json import loads, dumps


def tw2ccw(twPathNoExt: str) -> str:
    ccwPathNoExt = twPathNoExt.removesuffix("tw") + "ccw"

    with ZipFile(twPathNoExt + ".sb3") as twFile:
        with ZipFile(ccwPathNoExt + ".sb3", mode="w") as ccwFile:
            # 把 twFile 的内容全部拷贝到 ccwFile 中，除了 twFile/project.json 这个文件，该文件需要先解析、修改、再序列化，然后放入 ccwFile 中。
            for info in twFile.infolist():
                if info.filename == "project.json":
                    with twFile.open(info) as projectFile:
                        projectData: dict = loads(projectFile.read().decode("utf-8"))
                    projectData.pop("extensionURLs")
                    ccwFile.writestr("project.json", dumps(projectData).encode("utf-8"))
                else:
                    with twFile.open(info) as sourceFile:
                        ccwFile.writestr(info, sourceFile.read())

    return ccwPathNoExt + ".sb3"


def main(argv: list[str]):
    if len(argv) != 2:
        raise Exception("参数数量错误\n")

    outPath: str = tw2ccw(argv[1].removesuffix(".sb3"))

    print(f"cqtw2ccw 运行完毕，输出到 {outPath}.sb3")


if __name__ == "__main__":
    from sys import argv
    main(argv)
