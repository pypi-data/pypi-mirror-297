from twisted.internet.task import react
from _utils import print_response

import treq


async def main(reactor):
    resp = await treq.get("https://httpbin.org/cookies/set?hello=world")

    jar = resp.cookies()
    [cookie] = treq.cookies.search(jar, domain="httpbin.org", name="hello")
    print("The server set our hello cookie to: {}".format(cookie.value))

    await treq.get("https://httpbin.org/cookies", cookies=jar).addCallback(
        print_response
    )


react(main)
