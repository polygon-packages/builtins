# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

import io
import sys
import asyncio
from functools import wraps


@polygon.on(prefix=">")
async def python(e):
    await e.edit("`Hmm, nice code..`")
    reply = await e.get_reply_message()
    try:
        code = e.text[1:] or reply.text
    except (IndexError, AttributeError):
        code = ""
    if not code.strip():
        return await e.edit("`No code? no output!`")
    stdout, stderr = await execute(code, e)
    formatted_stderr = (
        str(stderr)
        .split("__code_wrapper__\n")[-1]
        .strip()
    )
    output = (
        f"**Code**:\n```{code}```"
        f"\n\n**stderr**:\n```{formatted_stderr}```"
        f"\n\n**stdout**:\n```{stdout}```"
    )
    if len(output) > db.get("TelegramLimit"):
            await polygon.send_file(
                e.chat_id,
                utility.buffer(output, name="python.txt"),
                force_document=True,
                caption=f"`{code}`",
                reply_to=reply,
            )
            return await e.delete()
    await e.edit(output)


def redirect_console_output(fn):
    """ Makes a function always return console output (ignores returned output) """

    def set_out():
        defaults = (sys.stdout, sys.stderr)
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        return defaults

    def reset_out(defaults):
        output = (sys.stdout.getvalue() or None, sys.stderr.getvalue() or None)
        sys.stdout, sys.stderr = defaults
        return output

    if asyncio.iscoroutinefunction(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            defaults = set_out()
            await fn(*args, **kwargs)
            return reset_out(defaults)
    else:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            defaults = set_out()
            fn(*args, **kwargs)
            return reset_out(defaults)

    return wrapper

@redirect_console_output
async def execute(code, *args):
    fn = "__code_wrapper__"
    formatted_code = f"async def {fn}(e, *args):" + "".join(
        [f"\n {l}" for l in code.split("\n")]
    )
    exec(formatted_code)
    try:
        await locals()[fn](*args)
    except BaseException:
        sys.stderr.write(utility.get_traceback())
