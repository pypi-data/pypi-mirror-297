from pathlib import Path

from dotenv import load_dotenv

from forum import create_forum_from_config

load_dotenv()


def main(config: Path):
    forum = create_forum_from_config(config)

    res = forum.ama({"user_query": "What is the meaning of life?"})
    print(res)


if __name__ == "__main__":
    main(Path(__file__).parent / "diskurs.yml")
