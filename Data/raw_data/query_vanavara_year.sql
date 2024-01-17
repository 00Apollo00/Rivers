SELECT public.rivers_post.date, public.rivers_post.code_post, public.rivers_post.level_w, snow.snow_height, snow.degree_coverage ,temperature_precipitation.tmean
,  post_9387
FROM public.rivers_post

	INNER JOIN  snow ON rivers_post.date =  snow.date AND snow.vmo_index = 24908
	INNER JOIN temperature_precipitation ON rivers_post.date = temperature_precipitation.date AND temperature_precipitation.vmo_index = 24908
	INNER JOIN /*public.rivers_post AS post_9387*/ 
		(SELECT public.rivers_post.level_w as post_9387, public.rivers_post.date as date_9387
	 		FROM public.rivers_post 
	 			WHERE  public.rivers_post.code_post=9387  )n2				
		ON ( public.rivers_post.date = n2.date_9387 )			
		WHERE public.rivers_post.date BETWEEN '2008-01-01' AND '2008-12-31'
ORDER BY date ASC 