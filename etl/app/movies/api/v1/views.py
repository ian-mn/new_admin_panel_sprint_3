from typing import Optional, Tuple

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import EmptyPage, Page
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork, PersonFilmWork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related("genres", "persons")
        queryset = queryset.values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
        ).annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.Role.ACTOR),
            ),
            directors=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.Role.DIRECTOR),
            ),
            writers=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.Role.WRITER),
            ),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )

        prev, next = self.__get_prev_and_next_page(page)

        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev,
            "next": next,
            "results": list(queryset),
        }
        return context

    def __get_prev_and_next_page(
        self, page: Page
    ) -> Tuple[Optional[int], Optional[int]]:
        """Returns tuple with previous and next page.

        Args:
            page (Page): Current Page.

        Returns:
            Tuple[Optional[int], Optional[int]]: If pages doesn`t exist returns None.
        """
        prev_page = page.number - 1
        if prev_page < 1:
            prev_page = None

        next_page = None
        try:
            next_page = page.next_page_number()
        except EmptyPage:
            pass

        return prev_page, next_page


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        return self.get_object()
