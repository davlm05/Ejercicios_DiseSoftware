package com.lanchas.guides.controller;

import com.lanchas.guides.model.Guide;
import com.lanchas.guides.service.GuideService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.*;

import java.util.List;

@Controller("/guides")
public class GuideController {

    private final GuideService guideService;

    public GuideController(GuideService guideService) {
        this.guideService = guideService;
    }

    @Post
    public HttpResponse<Guide> createGuide(@Body Guide guide) {
        Guide created = guideService.createGuide(guide);
        return HttpResponse.created(created);
    }

    @Get
    public List<Guide> listGuides() {
        return guideService.listActiveGuides();
    }

    @Get("/{id}")
    public HttpResponse<Guide> getGuide(Long id) {
        return guideService.findById(id)
                .map(HttpResponse::ok)
                .orElse(HttpResponse.notFound());
    }
}
