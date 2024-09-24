from os import listdir
from os.path import isdir, join
from threading import Event

from telegram.client import Telegram


def upload(
    phone: str,
    input_dir: str,
    privacy: str,
    users: list[str] | None,
    active_period: str,
    save_to_profile: bool,
    protected_content: bool,
    tdlib: str | None,
    cache: str | None,
    start: int,
    end: int | None,
) -> None:
    telegram = Telegram(
        api_id=2092395,
        api_hash="38e26914cf0fda6356fda8f9d28f3bb9",
        database_encryption_key="just a secret",
        tdlib_verbosity=0,
        library_path=tdlib,
        files_directory=cache,
        phone=phone,
    )
    telegram.login()
    me = int(telegram.call_method("getMe", block=True).update["id"])  # type:ignore

    done = Event()
    telegram.add_update_handler("updateSavedMessagesTopic", lambda *_: done.set())
    telegram.call_method("loadSavedMessagesTopics", {"limit": 1}, block=True)
    done.wait()

    if users is not None:
        user_ids = []
        for u in users:
            if u.isdigit():
                user_ids.append(int(u))
                continue

            try:
                user_ids.append(
                    telegram.call_method(  # type: ignore
                        "searchPublicChat",
                        {"username": u.strip().removeprefix("@")},
                        block=True,
                    ).update["id"]
                )
            except Exception:
                print(f"An error occurred while getting user id ({u}).")
    else:
        user_ids = None

    if not isdir(input_dir):
        print("Input folder does not exists")
        exit(1)

    queue: set[int] = set()
    done = Event()

    def wait_uploading(file: dict[str, object]) -> None:
        if (
            file["file"]["id"] in queue  # type: ignore
            and not file["file"]["remote"]["is_uploading_active"]  # type:ignore
        ):
            queue.remove(file["file"]["id"])  # type: ignore

            print(f" - Story uploaded. {len(queue)} left.")
            if len(queue) == 0:
                done.set()

    telegram.add_update_handler("updateFile", wait_uploading)

    print("Start uploading")
    for i in range(start, (end + 1) if end is not None else len(listdir(input_dir))):
        print(f" - Adding story to the uploading queue. (VIDEO-ID: {i})")
        queue.add(
            telegram.call_method(  # type: ignore
                "sendStory",
                {
                    "chat_id": me,
                    "content": {
                        "@type": "inputStoryContentVideo",
                        "video": {
                            "@type": "inputFileLocal",
                            "path": join(input_dir, f"{i}.mp4"),
                        },
                    },
                    "areas": None,
                    "caption": None,
                    "privacy_settings": {
                        "everyone": {
                            "@type": "storyPrivacySettingsEveryone",
                            "except_user_ids": user_ids,
                        },
                        "contacts": {
                            "@type": "storyPrivacySettingsContacts",
                            "except_user_ids": user_ids,
                        },
                        "selected": {
                            "@type": "storyPrivacySettingsSelectedUsers",
                            "user_ids": user_ids,
                        },
                        "friends": {
                            "@type": "storyPrivacySettingsCloseFriends",
                        },
                    }[privacy],
                    "active_period": {
                        "6h": 21600,
                        "12h": 43200,
                        "24h": 86400,
                        "48h": 172800,
                    }[active_period],
                    "is_posted_to_chat_page": save_to_profile,
                    "protect_content": protected_content,
                },
                block=True,
            ).update["content"]["video"]["video"]["id"]
        )

    done.wait()
    print("Done")
