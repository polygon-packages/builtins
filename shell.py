# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

import io


@polygon.on(prefix="$")
async def shell(e):
    await e.edit("`Evaluating this command..`")
    cmd = e.text[1:]
    reply = await e.get_reply_message()
    stdout, stderr = polygon.shell(cmd)
    output = (
        f"**Query:** \
            \n`{cmd}` \
            \n\n**stderr:** \
            \n`{stderr}` \
            \n\n**stdout:** \
            \n `{stdout}`"
    )
    if len(output) > db.get("TelegramLimit"):
        await polygon.send_file(
            e.chat_id,
            utility.buffer(output, name="shell.txt"),
            force_document=True,
            caption=f"`{cmd}`",
            reply_to=reply
        )
        return await e.delete()
    await e.edit(output)
