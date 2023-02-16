from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    bank_card: str
    openai_key: str
    use_redis: bool
    bot_name: str


@dataclass
class Miscellaneous:
    add_admin_cmd: str = None
    other_params = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            bank_card=env.str("BANK_CARD"),
            openai_key=env.str("OPENAI_API_KEY"),
            use_redis=env.bool("USE_REDIS"),
            bot_name=env.str("BOT_NAME")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            add_admin_cmd=env.str("ADD_ADMIN_CMD")
        )
    )