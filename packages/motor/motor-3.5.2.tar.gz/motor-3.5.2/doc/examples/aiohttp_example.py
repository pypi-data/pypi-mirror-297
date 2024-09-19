# These comments let tutorial-asyncio.rst include this code in sections.
# -- setup-start --
from aiohttp import web

from motor.motor_asyncio import AsyncIOMotorClient


async def setup_db():
    db = AsyncIOMotorClient().test
    await db.pages.drop()
    html = "<html><body>{}</body></html>"
    await db.pages.insert_one({"_id": "page-one", "body": html.format("Hello!")})

    await db.pages.insert_one({"_id": "page-two", "body": html.format("Goodbye.")})

    return db


# -- setup-end --


# -- handler-start --
async def page_handler(request):
    # If the visitor gets "/pages/page-one", then page_name is "page-one".
    page_name = request.match_info.get("page_name")

    # Retrieve the long-lived database handle.
    db = request.app["db"]

    # Find the page by its unique id.
    document = await db.pages.find_one(page_name)

    if not document:
        return web.HTTPNotFound(text=f"No page named {page_name!r}")

    return web.Response(body=document["body"].encode(), content_type="text/html")


# -- handler-end --


# -- main-start --
async def init_connection():
    db = await setup_db()
    app = web.Application()
    app["db"] = db
    # Route requests to the page_handler() coroutine.
    app.router.add_get("/pages/{page_name}", page_handler)
    return app


def main():
    app = init_connection()
    web.run_app(app)


if __name__ == "__main__":
    main()
# -- main-end --
