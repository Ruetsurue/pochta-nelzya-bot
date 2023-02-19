import logging
import os
import pytz

from dotenv import load_dotenv
from typing import TypeVar
from telebot.types import Message

import pochta_nelzya.models as m

OUTPUT_DATE_FORMAT = '%a %d.%m.%Y %H:%M:%S %z'
MODEL_TYPES = TypeVar('MODEL_TYPES', m.FeedDogModel, m.WalkDogModel)

load_dotenv()


def format_time(utc_time_at):
    tz = pytz.timezone(os.getenv('TZ'))
    local_time_at = utc_time_at.astimezone(tz).strftime(OUTPUT_DATE_FORMAT)
    logging.debug(f'format_time: {local_time_at}')
    return local_time_at


async def get_all_records_for_n_days(model: MODEL_TYPES, msg_template: tuple[str, str], for_days=1, show_all=False):
    try:
        for_days = int(for_days)
    except ValueError:
        logging.error("Could not convert num_days")

    if show_all:
        records: list[model] = await model.get_all_records()
    else:
        records: list[model] = await model.get_last_n_days(for_days)
    records = [record.as_dict() for record in records]
    msg_header, msg_record = msg_template
    response_lines = [msg_header]

    for record in records:
        record['time_at'] = format_time(record['time_at'])
        line = msg_record.format(**record)
        response_lines.append(line)

    response = '\n\n'.join(response_lines)
    return response


def get_message_author(message: Message) -> str:
    """
    Get message author. If username is set, it will be returned. Otherwise returns first name + last name (if set)
    :param message:
    :return:
    """
    if message.from_user.username:
        username = message.from_user.username
        return f"@{username}"

    return message.from_user.full_name
