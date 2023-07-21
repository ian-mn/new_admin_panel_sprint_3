select 
	ids.id,
	ids.rating as imdb_rating,
    array_agg(DISTINCT genre.name) as genre,
	ids.title,
	ids.description,
	array_agg(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'director') as director,
    array_agg(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'actor') as actors_names,
    array_agg(DISTINCT person.full_name) FILTER (WHERE person_film_work.role = 'writer') as writers_names,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', person.id,
               'name', person.full_name
           )
       ) FILTER (WHERE person.id is not null and person_film_work.role = 'actor'),
       '[]'
    ) as actors,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', person.id,
               'name', person.full_name
           )
       ) FILTER (WHERE person.id is not null and person_film_work.role = 'writer'),
       '[]'
    ) as writers,
	max(ids.modified) as modified
from (
	select 
		film_work.id,
		film_work.rating,
		film_work.title,
		film_work.description,
		film_work.modified
	from content.film_work film_work
	where film_work.modified > 'etl_state'
	
	union
	
	select 
		film_work.id,
		film_work.rating,
		film_work.title,
		film_work.description,
		person.modified
	from content.film_work film_work
	LEFT JOIN content.person_film_work person_film_work ON person_film_work.film_work_id = film_work.id
	LEFT JOIN content.person person ON person.id = person_film_work.person_id
	where person.modified > 'etl_state'
	
	union 
	
	select 
		film_work.id,
		film_work.rating,
		film_work.title,
		film_work.description,
		genre.modified
	from content.film_work film_work
	LEFT JOIN content.genre_film_work genre_film_work ON genre_film_work.film_work_id = film_work.id
	LEFT JOIN content.genre genre ON genre.id = genre_film_work.genre_id
	where genre.modified > 'etl_state'
) as ids
LEFT JOIN content.person_film_work person_film_work ON person_film_work.film_work_id = ids.id
LEFT JOIN content.person person ON person.id = person_film_work.person_id
LEFT JOIN content.genre_film_work genre_film_work ON genre_film_work.film_work_id = ids.id
LEFT JOIN content.genre genre ON genre.id = genre_film_work.genre_id
group by 
	ids.id,
	ids.rating,
	ids.title,
	ids.description
ORDER BY modified;