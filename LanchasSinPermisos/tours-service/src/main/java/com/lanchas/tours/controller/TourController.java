package com.lanchas.tours.controller;

import com.lanchas.tours.model.Tour;
import com.lanchas.tours.service.TourService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.*;

import java.util.List;

@Controller("/tours")
public class TourController {

    private final TourService tourService;

    public TourController(TourService tourService) {
        this.tourService = tourService;
    }

    @Post
    public HttpResponse<Tour> createTour(@Body Tour tour) {
        Tour created = tourService.createTour(tour);
        return HttpResponse.created(created);
    }

    @Get
    public List<Tour> listTours() {
        return tourService.listAvailableTours();
    }

    @Get("/{id}")
    public HttpResponse<Tour> getTour(Long id) {
        return tourService.findById(id)
                .map(HttpResponse::ok)
                .orElse(HttpResponse.notFound());
    }
}
