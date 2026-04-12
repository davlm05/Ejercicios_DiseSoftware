package com.lanchas.guides.repository;

import com.lanchas.guides.model.Guide;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;

import java.util.List;

@JdbcRepository(dialect = Dialect.H2)
public interface GuideRepository extends CrudRepository<Guide, Long> {

    List<Guide> findByActive(Boolean active);
}
