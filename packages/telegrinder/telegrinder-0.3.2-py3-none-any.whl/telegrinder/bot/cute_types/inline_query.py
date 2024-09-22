import typing

from fntypes.result import Result

from telegrinder.api.api import API, APIError
from telegrinder.bot.cute_types.base import BaseCute, compose_method_params, shortcut
from telegrinder.model import get_params
from telegrinder.types.objects import *


class InlineQueryCute(BaseCute[InlineQuery], InlineQuery, kw_only=True):
    api: API

    @property
    def from_user(self) -> User:
        return self.from_

    @shortcut("answer_inline_query", custom_params={"results"})
    async def answer(
        self,
        results: InlineQueryResult | list[InlineQueryResult],
        inline_query_id: str,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: InlineQueryResultsButton | None = None,
        **other: typing.Any,
    ) -> Result[bool, APIError]:
        """Shortcut `API.answer_inline_query()`, see the [documentation](https://core.telegram.org/bots/api#answerinlinequery)

        Use this method to send answers to an inline query. On success, True is returned.
        No more than 50 results per query are allowed.
        :param inline_query_id: Unique identifier for the answered query.

        :param results: A JSON-serialized array of results for the inline query.

        :param cache_time: The maximum amount of time in seconds that the result of the inline querymay be cached on the server. Defaults to 300.

        :param is_personal: Pass True if results may be cached on the server side only for the user thatsent the query. By default, results may be returned to any user who sendsthe same query.

        :param next_offset: Pass the offset that a client should send in the next query with the same textto receive more results. Pass an empty string if there are no more resultsor if you don't support pagination. Offset length can't exceed 64 bytes.
        :param button: A JSON-serialized object describing a button to be shown above inline queryresults."""

        params = compose_method_params(
            get_params(locals()),
            self,
            default_params={("inline_query_id", "id")},
        )
        params["results"] = [results] if not isinstance(results, list) else results
        return await self.ctx_api.answer_inline_query(**params)


__all__ = ("InlineQueryCute",)
