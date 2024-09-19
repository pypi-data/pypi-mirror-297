import tgram
import random
from .type_ import Type_

from typing import List, Optional


class InlineQueryResultCachedAudio(Type_):
    """
    Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.

    Telegram Documentation: https://core.telegram.org/bots/api#inlinequeryresultcachedaudio

    :param type: Type of the result, must be audio
    :type type: :obj:`str`

    :param id: Unique identifier for this result, 1-64 bytes
    :type id: :obj:`str`

    :param audio_file_id: A valid file identifier for the audio file
    :type audio_file_id: :obj:`str`

    :param caption: Optional. Caption, 0-1024 characters after entities parsing
    :type caption: :obj:`str`

    :param parse_mode: Optional. Mode for parsing entities in the audio caption. See formatting options for more
        details.
    :type parse_mode: :obj:`str`

    :param caption_entities: Optional. List of special entities that appear in the caption, which can be specified
        instead of parse_mode
    :type caption_entities: :obj:`list` of :class:`tgram.types.MessageEntity`

    :param reply_markup: Optional. Inline keyboard attached to the message
    :type reply_markup: :class:`tgram.types.InlineKeyboardMarkup`

    :param input_message_content: Optional. Content of the message to be sent instead of the audio
    :type input_message_content: :class:`tgram.types.InputMessageContent`

    :return: Instance of the class
    :rtype: :class:`tgram.types.InlineQueryResultCachedAudio`
    """

    def __init__(
        self,
        audio_file_id: "str" = None,
        caption: "str" = None,
        parse_mode: "str" = None,
        caption_entities: List["tgram.types.MessageEntity"] = None,
        reply_markup: "tgram.types.InlineKeyboardMarkup" = None,
        input_message_content: "tgram.types.InputMessageContent" = None,
        me: "tgram.TgBot" = None,
        json: "dict" = None,
    ):
        super().__init__(me=me, json=json)
        self.type = "cachedaudio"
        self.id = random.randint(10000, 99999)
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    @staticmethod
    def _parse(
        me: "tgram.TgBot" = None, d: dict = None, force: bool = None
    ) -> Optional["tgram.types.InlineQueryResultCachedAudio"]:
        return (
            InlineQueryResultCachedAudio(
                me=me,
                json=d,
                audio_file_id=d.get("audio_file_id"),
                caption=d.get("caption"),
                parse_mode=d.get("parse_mode"),
                caption_entities=[
                    tgram.types.MessageEntity._parse(me=me, d=i)
                    for i in d.get("caption_entities")
                ]
                if d.get("caption_entities")
                else None,
                reply_markup=tgram.types.InlineKeyboardMarkup._parse(
                    me=me, d=d.get("reply_markup")
                ),
                input_message_content=tgram.types.InputMessageContent._parse(
                    me=me, d=d.get("input_message_content")
                ),
            )
            if d and (force or me and __class__.__name__ not in me._custom_types)
            else None
            if not d
            else Type_._custom_parse(
                __class__._parse(me=me, d=d, force=True),
                me._custom_types.get(__class__.__name__),
            )
        )
