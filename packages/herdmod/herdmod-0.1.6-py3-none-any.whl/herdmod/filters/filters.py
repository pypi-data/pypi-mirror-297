import pyroherd
import pyrogram


def dice(ctx, message):
    return hasattr(message, 'dice') and message.dice


pyroherd.filters.dice = dice
pyrogram.filters.dice = dice