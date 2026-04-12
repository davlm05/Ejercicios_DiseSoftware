package com.lanchas.tours.service;

import com.lanchas.tours.model.Tour;
import com.lanchas.tours.repository.TourRepository;
import jakarta.inject.Singleton;

import java.util.List;
import java.util.Optional;

@Singleton
public class TourService {

    private final TourRepository tourRepository;

    public TourService(TourRepository tourRepository) {
        this.tourRepository = tourRepository;
    }

    public Tour createTour(Tour tour) {
        if (tour.getAvailable() == null) {
            tour.setAvailable(true);
        }
        if (tour.getMaxCapacity() == null) {
            tour.setMaxCapacity(10);
        }
        return tourRepository.save(tour);
    }

    public List<Tour> listAvailableTours() {
        return tourRepository.findByAvailable(true);
    }

    public Optional<Tour> findById(Long id) {
        return tourRepository.findById(id);
    }
}
