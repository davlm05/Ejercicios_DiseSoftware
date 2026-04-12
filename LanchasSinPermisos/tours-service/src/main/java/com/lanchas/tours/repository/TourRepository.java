package com.lanchas.tours.repository;

import com.lanchas.tours.model.Tour;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;

import java.util.List;

@JdbcRepository(dialect = Dialect.H2)
public interface TourRepository extends CrudRepository<Tour, Long> {

    List<Tour> findByAvailable(Boolean available);
}
