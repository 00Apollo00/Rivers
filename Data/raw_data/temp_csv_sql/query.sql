SELECT public.river_post_test.date, public.river_post_test.code_post, public.river_post_test.level_w, snow.snow_height, snow.degree_coverage ,temperature_precipitation.tmean
                            ,  post_9387
                            FROM public.river_post_test

                                INNER JOIN  snow ON river_post_test.date =  snow.date AND snow.vmo_index = 24908
                                INNER JOIN temperature_precipitation ON river_post_test.date = temperature_precipitation.date AND temperature_precipitation.vmo_index = 24908
                                INNER JOIN /*public.river_post AS post_9387*/ 
                                    (SELECT public.river_post_test.level_w as post_9387, public.river_post_test.date as date_9387
                                        FROM public.river_post_test
                                            WHERE  public.river_post_test.code_post=9387  )n2
                                    ON ( public.river_post_test.date = n2.date_9387 )
                                    WHERE  public.river_post_test.code_post <> 9387
                            ORDER BY date ASC