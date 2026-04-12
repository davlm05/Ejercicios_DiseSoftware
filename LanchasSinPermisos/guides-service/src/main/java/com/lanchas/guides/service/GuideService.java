package com.lanchas.guides.service;

import com.lanchas.guides.model.Guide;
import com.lanchas.guides.repository.GuideRepository;
import jakarta.inject.Singleton;

import java.util.List;
import java.util.Optional;

@Singleton
public class GuideService {

    private final GuideRepository guideRepository;

    public GuideService(GuideRepository guideRepository) {
        this.guideRepository = guideRepository;
    }

    public Guide createGuide(Guide guide) {
        if (guide.getActive() == null) {
            guide.setActive(true);
        }
        if (guide.getExperience() == null) {
            guide.setExperience(0);
        }
        return guideRepository.save(guide);
    }

    public List<Guide> listActiveGuides() {
        return guideRepository.findByActive(true);
    }

    public Optional<Guide> findById(Long id) {
        return guideRepository.findById(id);
    }
}
