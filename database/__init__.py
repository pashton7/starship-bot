
import aiosqlite

class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_log(
        self, user_id: int, server_id: int, moderator_id: int, moderation_type: str, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM moderations WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO moderations(id, user_id, server_id, moderator_id, moderation_type, reason) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    moderation_type,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id
    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, moderation_type, reason, strftime('%s', created_at), id FROM moderations WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list